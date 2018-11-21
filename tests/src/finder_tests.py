#!/usr/bin/env python
"""
How to run:
python -m unittest discover tests -v
"""

import os
from unittest import main, TestCase
from src.finder import main, match_file_properties, parse_args
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

        for arg in ['-a', '--audio']:
            # No folders are provided
            args = [arg]
            self.assertRaises(SystemExit, parse_args, args)

            # Audio files set
            args = [self.dummy_folder, arg]
            parser = parse_args(args)
            self.assertEqual(parser.folders, args[0:1])
            self.assertEqual(parser.audio, True)

    def test_parse_args__text(self):
        """Check argument 'text' parsing"""

        for arg in ['-t', '--text']:
            # No folders are provided
            args = [arg]
            self.assertRaises(SystemExit, parse_args, args)

            # Text files set
            args = [self.dummy_folder, arg]
            parser = parse_args(args)
            self.assertEqual(parser.folders, args[0:1])
            self.assertEqual(parser.text, True)

    def test_parse_args__video(self):
        """Check argument 'video' parsing"""

        for arg in ['-v', '--video']:
            # No folders are provided
            args = [arg]
            self.assertRaises(SystemExit, parse_args, args)

            # Video files set
            args = [self.dummy_folder, arg]
            parser = parse_args(args)
            self.assertEqual(parser.folders, args[0:1])
            self.assertEqual(parser.video, True)

    def test_parse_args__extensions(self):
        """Check argument 'extensions' parsing"""

        # Single extension
        for ext in ['-e', '--extensions']:
            args = [self.dummy_folder, ext, 'mp3']
            parser = parse_args(args)
            self.assertEqual(parser.folders, args[0:1])
            self.assertEqual(parser.extensions, ['mp3'])

        # Multiple extensions
        for ext in ['-e', '--extensions']:
            args = [self.dummy_folder, ext, 'mp3', 'mp4']
            parser = parse_args(args)
            self.assertEqual(parser.folders, args[0:1])
            self.assertEqual(parser.extensions, ['mp3', 'mp4'])


class FilePropertiesTestCase(TestCase):
    tests_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_match_file_properties__pdf_has_text_track(self):
        """
        PDF file contains 'text' track
        :return:
        """

        filepath = os.path.join(self.tests_folder, 'data', 'text', 'dummy.pdf')
        args = [self.tests_folder, '-t']
        parser = parse_args(args)
        self.assertTrue(match_file_properties(filepath, parser))

    def test_match_file_properties__movie_has_video_and_audio_tracks(self):
        """
        Movie file contains both 'video' and 'audio' tracks
        :return:
        """

        filepath = os.path.join(self.tests_folder, 'data', 'video', 'big_buck_bunny_720p_1mb.mp4')
        args = [self.tests_folder, '-va']
        parser = parse_args(args)
        self.assertTrue(match_file_properties(filepath, parser))

    def test_match_file_properties__movie_does_not_have_both_video_and_text_tracks(self):
        """
        Movie file does not contains both 'video' and 'text' tracks
        :return:
        """

        filepath = os.path.join(self.tests_folder, 'data', 'video', 'big_buck_bunny_720p_1mb.mp4')
        args = [self.tests_folder, '-vt']
        parser = parse_args(args)
        self.assertFalse(match_file_properties(filepath, parser))


class FileFinderTestCase(TestCase):
    dummy_folder = os.path.dirname(os.path.abspath(__file__))
    tests_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_main_only_folders(self):
        """
        Search with only folders
        :return:
        """

        # Single path
        args = [os.path.join(self.tests_folder, 'data', 'text')]
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            [os.path.join(self.tests_folder, 'data', 'text', 'dummy.pdf')]
        )

        # Multiple paths
        args = [
            os.path.join(self.tests_folder, 'data', 'text'),
            os.path.join(self.tests_folder, 'data', 'video'),
        ]
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            [
                os.path.join(self.tests_folder, 'data', 'text', 'dummy.pdf'),
                os.path.join(self.tests_folder, 'data', 'video', 'big_buck_bunny_720p_1mb.mp4')
            ]
        )

    def test_main_only_audio_tracks(self):
        """
        Search with folders + audio track
        :return:
        """

        # Main folder + audio types
        args = [os.path.join(self.tests_folder, 'data'), '-a']
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            [
                os.path.join(self.tests_folder, 'data', 'audio', 'crowd-cheering.mp3'),
                os.path.join(self.tests_folder, 'data', 'video', 'big_buck_bunny_720p_1mb.mp4')
            ]
        )

        # Video folder + audio types
        args = [os.path.join(self.tests_folder, 'data', 'video'), '-a']
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            [
                os.path.join(self.tests_folder, 'data', 'video', 'big_buck_bunny_720p_1mb.mp4')
            ]
        )

        # Text folder + audio types
        args = [os.path.join(self.tests_folder, 'data', 'text'), '-a']
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            []
        )

    def test_main_only_video_tracks(self):
        """
        Search with folders + video track
        :return:
        """

        # Main folder + video types
        args = [os.path.join(self.tests_folder, 'data'), '-v']
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            [
                os.path.join(self.tests_folder, 'data', 'video', 'big_buck_bunny_720p_1mb.mp4')
            ]
        )

        # Text folder + video types
        args = [os.path.join(self.tests_folder, 'data', 'text'), '-v']
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            []
        )

    def test_main_only_text_tracks(self):
        """
        Search with folders + text track
        :return:
        """

        # Main folder + text types
        args = [os.path.join(self.tests_folder, 'data'), '-t']
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            [
                os.path.join(self.tests_folder, 'data', 'text', 'dummy.pdf')
            ]
        )

        # Video folder + text types
        args = [os.path.join(self.tests_folder, 'data', 'video'), '-t']
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            []
        )

    def test_main_multiple_track_types(self):
        """
        Search with folders + multiple track types
        :return:
        """

        # Main folder + audio/video types
        args = [os.path.join(self.tests_folder, 'data'), '-av']
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            [
                os.path.join(self.tests_folder, 'data', 'video', 'big_buck_bunny_720p_1mb.mp4')
            ]
        )

        # Main folder + audio/video types
        args = [os.path.join(self.tests_folder, 'data'), '-at']
        parser = parse_args(args)
        self.assertEqual(
            main(parser),
            []
        )


if __name__ == '__main__':
    main()
