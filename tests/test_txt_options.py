#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import txt


class TestTextOptions(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    # options
    def test_txt_opt_random(self):
        """TEST: txt OPT_RANDOM"""
        assert txt.OPT_RANDOM is not None  # == " '-m/--method random' "

    def test_txt_opt_country(self):
        """TEST: txt OPT_COUNTRY"""
        assert txt.OPT_COUNTRY is not None  # == " 'c/--country' "

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
