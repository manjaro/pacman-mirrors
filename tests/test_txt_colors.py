#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import txt


class TestTextColors(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    def test_txt_err_color(self):
        """TEST: txt ERR_CLR"""
        assert txt.ERR_CLR is not None

    def test_txt_inf_color(self):
        """TEST: txt INF_CLR"""
        assert txt.INF_CLR is not None

    def test_txt_wrn_color(self):
        """TEST: txt WRN_COLOR"""
        assert txt.WRN_CLR is not None

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
