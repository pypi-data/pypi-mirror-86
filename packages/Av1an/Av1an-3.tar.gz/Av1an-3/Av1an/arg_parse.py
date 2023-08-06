#!/bin/env python
import argparse
from pathlib import Path

from Av1an.commandtypes import Command


class Args(object):

    # noinspection PyTypeChecker
    def __init__(self, initial_data):
        # Input/Output/Temp
        self.input: Path = None
        self.temp: Path = None
        self.output_file: Path = None
        self.mkvmerge: bool = None

        # Splitting
        self.chunk_method: str = None
        self.scenes: Path = None
        self.split_method: str = None
        self.extra_split: int = None
        self.min_scene_len: int = None

        # PySceneDetect split
        self.threshold: float = None

        # AOM Keyframe split
        self.reuse_first_pass: bool = None

        # Encoding
        self.passes = None
        self.video_params: Command = None
        self.encoder: str = None
        self.workers: int = None

        # FFmpeg params
        self.ffmpeg_pipe: Command = None
        self.ffmpeg: str = None
        self.audio_params = None
        self.pix_format: Command = None

        # Misc
        self.logging = None
        self.resume: bool = None
        self.no_check: bool = None
        self.keep: bool = None
        self.force: bool = None

        # Vmaf
        self.vmaf: bool = None
        self.vmaf_path: str = None
        self.vmaf_res: str = None

        # Target Vmaf
        self.target_quality: int = None
        self.probes: int = None
        self.min_q: int = None
        self.max_q: int = None
        self.vmaf_plots: bool = None
        self.probing_rate: int = None
        self.n_threads: int = None
        self.vmaf_filter: str = None

        # VVC
        self.vvc_conf: Path = None
        self.video_dimensions = (None, None)
        self.video_framerate = None

        for key in initial_data:
            setattr(self, key, initial_data[key])

        # Inner
        self.counter = None

        # Vapoursynth
        self.is_vs: bool = None

        self.frames: int = 0


def arg_parsing():
    """Command line parsing"""
    parser = argparse.ArgumentParser()

    # Input/Output/Temp
    io_group = parser.add_argument_group('Input and Output')
    io_group.add_argument('--input', '-i', nargs='+', type=Path, help='Input File')
    io_group.add_argument('--temp', type=Path, default=None, help='Set temp folder path')
    io_group.add_argument('--output_file', '-o', type=Path, default=None, help='Specify output file')
    io_group.add_argument('--mkvmerge', help='Use mkvmerge instead of ffmpeg to concatenate', action='store_true')

    io_group.add_argument('--logging', '-log', type=str, default=None, help='Enable logging')
    io_group.add_argument('--resume', '-r', help='Resuming previous session', action='store_true')
    io_group.add_argument('--keep', help='Keep temporally folder after encode', action='store_true')
    io_group.add_argument('--force', help="Force encoding if input args seen as invalid", action='store_true')

    # Splitting
    split_group = parser.add_argument_group('Splitting')
    split_group.add_argument('--chunk_method', '-cm', type=str, default=None, help='Method for creating chunks',
                             choices=['select', 'vs_ffms2', 'vs_lsmash', 'hybrid'])
    split_group.add_argument('--scenes', '-s', type=str, default=None, help='File location for scenes')
    split_group.add_argument('--split_method', type=str, default='pyscene', help='Specify splitting method',
                             choices=['pyscene', 'aom_keyframes'])
    split_group.add_argument('--extra_split', '-xs', type=int, default=0,
                             help='Number of frames after which make split')

    # PySceneDetect split
    split_group.add_argument('--threshold', '-tr', type=float, default=35, help='PySceneDetect Threshold')
    split_group.add_argument('--min_scene_len', type=int, default=120, help='Minimum number of frames in a split')

    # AOM Keyframe split
    split_group.add_argument('--reuse_first_pass', help='Reuse the first pass from aom_keyframes split on the chunks',
                             action='store_true')

    # Encoding
    encode_group = parser.add_argument_group('Encoding')
    encode_group.add_argument('--passes', '-p', type=int, default=None, help='Specify encoding passes', choices=[1, 2])
    encode_group.add_argument('--video_params', '-v', type=str, default=None, help='encoding settings')
    encode_group.add_argument('--encoder', '-enc', type=str, default='aom', help='Choosing encoder',
                              choices=['aom', 'svt_av1', 'svt_vp9', 'rav1e', 'vpx', 'x265', 'x264', 'vvc'])
    encode_group.add_argument('--workers', '-w', type=int, default=0, help='Number of workers')
    encode_group.add_argument('--no_check', '-n', help='Do not check encodings', action='store_true')

    # VVC
    encode_group.add_argument('--vvc_conf', type=Path, default=None, help='Path to VVC confing file')

    # FFmpeg params
    ffmpeg_group = parser.add_argument_group('FFmpeg')
    ffmpeg_group.add_argument('--ffmpeg', '-ff', type=str, default='', help='FFmpeg commands')
    ffmpeg_group.add_argument('--audio_params', '-a', type=str, default='-c:a copy', help='FFmpeg audio settings')
    ffmpeg_group.add_argument('--pix_format', '-fmt', type=str, default='yuv420p10le', help='FFmpeg pixel format')

    # Vmaf
    vmaf_group = parser.add_argument_group('VMAF')
    vmaf_group.add_argument('--vmaf', help='Calculating vmaf after encode', action='store_true')
    vmaf_group.add_argument('--vmaf_path', type=Path, default=None, help='Path to vmaf models')
    vmaf_group.add_argument('--vmaf_res', type=str, default="1920x1080", help='Resolution used in vmaf calculation')
    vmaf_group.add_argument('--n_threads', type=int, default=None, help='Threads for vmaf calculation')

    # Target Quality
    tq_group = parser.add_argument_group('Target Quality')
    tq_group.add_argument('--target_quality', type=float, help='Value of Vmaf to target')
    tq_group.add_argument('--target_quality_method', type=str, default='per_frame', help='Method selection for target quality')
    tq_group.add_argument('--probes', type=int, default=4, help='Number of probes to make for target_quality')
    tq_group.add_argument('--min_q', type=int, default=None, help='Min q for target_quality')
    tq_group.add_argument('--max_q', type=int, default=None, help='Max q for target_quality')
    tq_group.add_argument('--vmaf_plots', help='Make plots of probes in temp folder', action='store_true')
    tq_group.add_argument('--probing_rate', type=int, default=4, help='Framerate for probes, 0 - original')
    tq_group.add_argument('--vmaf_filter', type=str, default=None, help='Filter applied to source at vmaf calcualation, use if you crop source')
    arg = Args(vars(parser.parse_args()))

    if arg.input == None:
        parser.print_help()
        exit()

    return arg
