#!/usr/bin/env python
"""

"""
import argparse
import sys


def parse_args(*args, **kwargs):
    parser = argparse.ArgumentParser(description='Search parameters')
    parser.add_argument(
        'folders',
        type=str,
        nargs='+',
        #default='.',
        help='Folders where files will be searched'
    )
    return parser.parse_args(*args, **kwargs)
