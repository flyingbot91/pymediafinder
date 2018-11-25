#!/usr/bin/env python
"""

"""
import argparse
import fnmatch
import os
import sys

from pymediainfo import MediaInfo


def main(parser):
    """
    Main method
    :param parser: (argparse.Namespace)
    :return: [str] List of filepaths.
    """

    filepaths = []

    regexes = ['*.*']
    if parser.extensions:
        regexes = ['*.%s' % extension for extension in parser.extensions]

    for folder in parser.folders:
        for regex in regexes:
            for root, dirs, files in os.walk(folder):
                for filename in fnmatch.filter(files, regex):
                    filepath = os.path.join(root, filename)
                    if any([parser.audio, parser.text, parser.video]):
                        # Parse only if the previous conditions are met.
                        if match_file_properties(filepath, parser):
                            filepaths.append(filepath)
                    else:
                        filepaths.append(filepath)

    return filepaths


def match_file_properties(filepath, parser):
    """

    :param filepath: (str) Fully qualified file path.
    :param parser: (argparse.Namespace)
    :return: (bool) True if <filepath> matches the requirements provided by <parser>. False otherwise.
    """

    desired_tracks = {
        'Video': parser.video,
        'Audio': parser.audio,
        'Text': parser.text
    }

    media_info = MediaInfo.parse(filepath)
    for track_name, is_required in desired_tracks.items():
        if is_required:
            for mtrack in media_info.tracks:
                if mtrack.track_type == track_name:
                    break
            else:
                return False

    return True


def parse_args(*args, **kwargs):
    """
    Parse sys.argv[1:]
    :param args:
    :param kwargs:
    :return:
    """

    parser = argparse.ArgumentParser(
        prog='pymediafinder',
        description='Search parameters',
        add_help=False,
    )
    parser.add_argument(
        '-V', '--version',
        action='store_true',
        help='Print version and exit'
    )
    parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='Print this help message and exit'
    )
    parser.add_argument(
        'folders',
        type=str,
        nargs='+',
        help='Folders where files will be searched'
    )
    parser.add_argument(
        '-e', '--extensions',
        type=str,
        nargs='+',
        help='File extensions to be included in the search'
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
