#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest

from pacman_mirrors.constants import txt


class TestTextConstants(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    def test_txt_houston(self):
        """TEST: txt HOUSTON"""
        assert txt.HOUSTON is not None

    def test_txt_override_opt(self):
        """TEST: txt OVERRIDE_OPT"""
        assert txt.OVERRIDE_OPT is not None

    def test_txt_repo_server(self):
        """TEST: txt REPO_SERVER"""
        assert txt.REPO_SERVER is not None

    def test_txt_reset_custom_file(self):
        """TEST: txt RESET_CUSTOM_FILE"""
        assert txt.MODIFY_CUSTOM is not None

    def test_txt_prefix_tip(self):
        """TEST: txt PREFIX_TIP"""
        assert txt.PREFIX_TIP is not None

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
