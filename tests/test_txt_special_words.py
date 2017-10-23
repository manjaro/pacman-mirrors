#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest

from pacman_mirrors.constants import txt


class TestTextSpecialWords(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    # special words
    def test_txt_special_word_path(self):
        """TEST: txt SPECIAL WORD PATH"""
        assert txt.PATH is not None

    def test_txt_special_word_file(self):
        """TEST: txt SPECIAL WORD FILE"""
        assert txt.FILE is not None

    def test_txt_special_word_seconds(self):
        """TEST: txt SPECIAL WORD SECONDS"""
        assert txt.SECONDS is not None

    def test_txt_special_word_number(self):
        """TEST: txt SPECIAL WORD NUMBER"""
        assert txt.NUMBER is not None

    def test_txt_special_word_usage(self):
        """TEST: txt SPECIAL WORD USAGE"""
        assert txt.USAGE is not None

    def test_txt_special_word_country(self):
        """TEST: txt SPECIAL WORD COUNTRY"""
        assert txt.COUNTRY is not None

    def test_txt_special_word_prefix(self):
        """TEST: txt SPECIAL WORD PREFIX"""
        assert txt.PREFIX is not None

    def test_txt_special_word_method(self):
        """TEST: txt SPECIAL WORD METHOD"""
        assert txt.METHOD is not None

    def test_txt_special_word_methods(self):
        """TEST: txt SPECIAL WORD METHODS"""
        assert txt.METHODS is not None

    def test_txt_special_word_branch(self):
        """TEST: txt SPECIAL WORD BRANCH"""
        assert txt.BRANCH is not None

    def test_txt_special_word_proto(self):
        """TEST: txt SPECIAL WORD PROTO"""
        assert txt.PROTO is not None

    def test_txt_special_word_misc(self):
        """TEST: txt SPECIAL WORD MISC"""
        assert txt.MISC is not None

    def test_txt_special_word_api(self):
        """TEST: txt SPECIAL WORD API"""
        assert txt.API is not None

    def test_txt_special_word_url(self):
        """TEST: txt SPECIAL WORD URL"""
        assert txt.URL is not None


    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
