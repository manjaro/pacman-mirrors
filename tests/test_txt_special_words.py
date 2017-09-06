#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import txt


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

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
