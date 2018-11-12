#!/usr/bin/env python
"""

"""
import argparse
import os
import sys
from glob import iglob


def main(parser):
    """
    Main method
    :param parser:
    :return:
    """

    regex = '**/*.*'
    for folder in parser.folders:
        for filepath in iglob(os.path.join(folder, regex), recursive=True):
            print(filepath)


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
    return parser.parse_args(*args, **kwargs)


if __name__ == '__main__':
    parser = parse_args(sys.argv[1:])
    main(parser)
