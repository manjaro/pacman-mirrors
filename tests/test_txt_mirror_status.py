#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import txt


class TestTextMirrorStatus(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    # mirror status constants
    def test_txt_lastsync_ok(self):
        """TEST: txt LASTSYNC_OK"""
        assert txt.LASTSYNC_OK is not None

    def test_txt_lastsync_na(self):
        """TEST: txt LASTSYNC_NA"""
        assert txt.LASTSYNC_NA is not None

    def test_txt_server_bad(self):
        """TEST: txt SERVER_BAD"""
        assert txt.SERVER_BAD is not None

    def test_txt_server_res(self):
        """TEST: txt SERVER_RES"""
        assert txt.SERVER_RES is not None

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
