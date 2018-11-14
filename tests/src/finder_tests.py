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
        self.assertEqual(parser.audio, False)
        self.assertEqual(parser.text, False)
        self.assertEqual(parser.video, False)

        # Multiple readable folders are provided
        dummy_folders = [self.dummy_folder, os.path.join(self.dummy_folder, 'data')]
        parser = parse_args(dummy_folders)
        self.assertEqual(parser.folders, dummy_folders)
        self.assertEqual(parser.audio, False)
        self.assertEqual(parser.text, False)
        self.assertEqual(parser.video, False)

    def test_parse_args__audio(self):
        """
        Check argument 'audio' parsing
        """

        # No folders are provided
        args = ['-a']
        self.assertRaises(SystemExit, parse_args, args)

        # Audio files set
        args = [self.dummy_folder, '-a']
        parser = parse_args(args)
        self.assertEqual(parser.folders, args[0:1])
        self.assertEqual(parser.audio, True)

    def test_parse_args__text(self):
        """Check argument 'text' parsing"""

        # No folders are provided
        args = ['-t']
        self.assertRaises(SystemExit, parse_args, args)

        # Text files set
        args = [self.dummy_folder, '-t']
        parser = parse_args(args)
        self.assertEqual(parser.folders, args[0:1])
        self.assertEqual(parser.text, True)

    def test_parse_args__video(self):
        """Check argument 'video' parsing"""

        # No folders are provided
        args = ['-v']
        self.assertRaises(SystemExit, parse_args, args)

        # Video files set
        args = [self.dummy_folder, '-v']
        parser = parse_args(args)
        self.assertEqual(parser.folders, args[0:1])
        self.assertEqual(parser.video, True)


if __name__ == '__main__':
    main()
