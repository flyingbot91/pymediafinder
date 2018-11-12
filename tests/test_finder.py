#!/usr/bin/env python
"""
How to run:
python -m unittest discover tests -v
"""

import os
from unittest import main, TestCase
from src.finder import parse_args
# from argparse import ArgumentError


class ArgParserTestCase(TestCase):
    dummy_folder = os.path.dirname(os.path.abspath(__file__))

    def test_parse_args__folders(self):
        """Check argument 'folders' parsing"""

        # No folders are provided
        dummy_folders = []
        # self.assertRaises(ArgumentError, parse_args, dummy_folders)
        self.assertRaises(SystemExit, parse_args, dummy_folders)

        # A single readable folder is provided
        dummy_folders = [self.dummy_folder]
        parser = parse_args(dummy_folders)
        self.assertEqual(parser.folders, dummy_folders)

        # Multiple readable folders are provided
        dummy_folders = [self.dummy_folder, os.path.join(self.dummy_folder, 'data')]
        parser = parse_args(dummy_folders)
        self.assertEqual(parser.folders, dummy_folders)

        # # Multiple folders are provided (some are not readable or do not exist)
        # self.fail()


if __name__ == '__main__':
    main()
