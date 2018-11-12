#!/usr/bin/env python
"""

"""
import argparse
import os
import sys

from glob import iglob
from pymediainfo import MediaInfo


def main(parser):
    """
    Main method
    :param parser:
    :return:
    """

    regex = '**/*.*'
    for folder in parser.folders:
        for filepath in iglob(os.path.join(folder, regex), recursive=True):
            if parser.audio or parser.text or parser.video:
                media_info = MediaInfo.parse(filepath)
                for track in media_info.tracks:
                    if parser.audio and track.track_type == 'Audio':
                        print("AUDIO:", filepath)
                    if parser.text and track.track_type == 'Text':
                        print("TEXT:", filepath)
                    if parser.video and track.track_type == 'Video':
                        print("VIDEO:", filepath)


def parse_args(*args, **kwargs):
    """
    Parse sys.argv[1:]
    :param args:
    :param kwargs:
    :return:
    """

    parser = argparse.ArgumentParser(description='Search parameters')
    parser.add_argument(
        'folders',
        type=str,
        nargs='+',
        #default='.',
        help='Folders where files will be searched'
    )
    parser.add_argument(
        '-a', '--audio',
        action='store_true',
        help='Look for files containing audio tracks'
    )
    parser.add_argument(
        '-v', '--video',
        action='store_true',
        help='Look for files containing video tracks'
    )
    parser.add_argument(
        '-t', '--text',
        action='store_true',
        help='Look for files containing text tracks'
    )
    return parser.parse_args(*args, **kwargs)


if __name__ == '__main__':
    parser = parse_args(sys.argv[1:])
    main(parser)
