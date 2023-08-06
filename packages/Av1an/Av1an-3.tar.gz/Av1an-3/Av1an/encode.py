#!/usr/bin/env python3
import time
import json
from pathlib import Path
from typing import List
import sys
import concurrent
import concurrent.futures
import shutil

from Encoders import ENCODERS
from Av1an.arg_parse import Args
from Chunks.chunk import Chunk
from Chunks.chunk_queue import load_or_gen_chunk_queue
from Av1an.concat import concat_routine
from Av1an.resume import write_progress_file
from TargetQuality import per_shot_target_quality_routine
from Av1an.utils import frame_probe_fast, frame_probe, terminate, set_total_frame_count, get_total_frame_count
from Startup.file_validation import process_inputs
from Av1an.bar import Manager, tqdm_bar
from Startup.setup import determine_resources, outputs_filenames, setup
from Av1an.logger import log, set_log
from Av1an.ffmpeg import extract_audio
from Av1an.fp_reuse import segment_first_pass
from Av1an.split import split_routine, extra_splits
from VMAF.vmaf import plot_vmaf
from Av1an.vapoursynth import is_vapoursynth

# todo, saving and loading more info to the scenes data
def main_queue(args):
    # Todo: Redo Queue
    try:
        tm = time.time()

        args.queue = process_inputs(args.input)

        for file in args.queue:
            tm = time.time()
            args.input = file
            is_vs = is_vapoursynth(args.input)
            args.is_vs = is_vs
            args.chunk_method = 'vs_ffms2' if is_vs else args.chunk_method

            if len(args.queue) > 1:
                print(f'Encoding: {file}')
                args.output_file = None

            encode_file(args)

            print(f'Finished: {round(time.time() - tm, 1)}s\n')
    except KeyboardInterrupt:
        print('Encoding stopped')
        sys.exit()


def encode_file(args: Args):
    """
    Encodes a single video file on the local machine.

    :param args: The args for this encode
    :return: None
    """

    outputs_filenames(args)

        # set up temp dir and logging
    setup(args)
    set_log(args.logging, args.temp)

    # find split locations
    split_locations = split_routine(args, args.resume)

    # create a chunk queue
    chunk_queue = load_or_gen_chunk_queue(args, args.resume, split_locations)

    # things that need to be done only the first time
    if not args.resume:

        extract_audio(args.input, args.temp, args.audio_params)

        if args.reuse_first_pass:
            segment_first_pass(args.temp, split_locations)

    # do encoding loop
    args.workers = determine_resources(args.encoder, args.workers)
    startup(args, chunk_queue)
    encoding_loop(args, chunk_queue)

    # concat
    concat_routine(args)

    if args.vmaf or args.vmaf_plots:
        plot_vmaf(args.input, args.output_file, args, args.vmaf_path, args.vmaf_res)

    # Delete temp folders
    if not args.keep:
        shutil.rmtree(args.temp)

def startup(args: Args, chunk_queue: List[Chunk]):
    """
    If resuming, open done file and get file properties from there
    else get file properties and

    """
    done_path = args.temp / 'done.json'
    if args.resume and done_path.exists():
        log('Resuming...\n')
        with open(done_path) as done_file:
            data = json.load(done_file)

        set_total_frame_count(args,data['frames'])
        done = len(data['done'])
        initial = sum(data['done'].values())
        log(f'Resumed with {done} encoded clips done\n\n')
    else:
        initial = 0
        total = frame_probe_fast(args.input, args.is_vs)
        d = {'frames': total, 'done': {}}
        with open(done_path, 'w') as done_file:
            json.dump(d, done_file)
    clips = len(chunk_queue)
    args.workers = min(args.workers, clips)
    print(f'\rQueue: {clips} Workers: {args.workers} Passes: {args.passes}\n'
          f'Params: {" ".join(args.video_params)}')
    counter = Manager().Counter(get_total_frame_count(args), initial)
    args.counter = counter


def encoding_loop(args: Args, chunk_queue: List[Chunk]):
    """Creating process pool for encoders, creating progress bar."""
    if args.workers != 0:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_cmd = {executor.submit(encode, cmd, args): cmd for cmd in chunk_queue}
            for future in concurrent.futures.as_completed(future_cmd):
                try:
                    future.result()
                except Exception as exc:
                    _, _, exc_tb = sys.exc_info()
                    print(f'Encoding error {exc}\nAt line {exc_tb.tb_lineno}')
                    terminate()
    args.counter.close()


def encode(chunk: Chunk, args: Args):
    """
    Encodes a chunk.

    :param chunk: The chunk to encode
    :param args: The cli args
    :return: None
    """
    try:
        st_time = time.time()

        chunk_frames = chunk.frames

        log(f'Enc: {chunk.name}, {chunk_frames} fr\n\n')

        # Target Quality Mode
        if args.target_quality:
            per_shot_target_quality_routine(args, chunk)

        ENCODERS[args.encoder].on_before_chunk(args, chunk)

        # skip first pass if reusing
        start = 2 if args.reuse_first_pass and args.passes >= 2 else 1

        # Run all passes for this chunk
        for current_pass in range(start, args.passes + 1):
            tqdm_bar(args, chunk, args.encoder, args.counter, chunk_frames, args.passes, current_pass)

        ENCODERS[args.encoder].on_after_chunk(args, chunk)

        # get the number of encoded frames, if no check assume it worked and encoded same number of frames
        encoded_frames = chunk_frames if args.no_check else frame_check_output(chunk, chunk_frames)

        # write this chunk as done if it encoded correctly
        if encoded_frames == chunk_frames:
            write_progress_file(Path(args.temp / 'done.json'), chunk, encoded_frames)

        enc_time = round(time.time() - st_time, 2)
        log(f'Done: {chunk.name} Fr: {encoded_frames}\n'
            f'Fps: {round(encoded_frames / enc_time, 4)} Time: {enc_time} sec.\n\n')

    except Exception as e:
        _, _, exc_tb = sys.exc_info()
        print(f'Error in encoding loop {e}\nAt line {exc_tb.tb_lineno}')


def frame_check_output(chunk: Chunk, expected_frames: int) -> int:
    actual_frames = frame_probe(chunk.output_path)
    if actual_frames != expected_frames:
        print(f'Chunk #{chunk.name}: {actual_frames}/{expected_frames} fr')
    return actual_frames
