#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import txt


class TestTextConstants(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    def test_txt_houston(self):
        """TEST: txt HOUSTON"""
        assert txt.HOUSTON is not None  # == "Houston?! We have a problem."

    def test_txt_override_opt(self):
        """TEST: txt OVERRIDE_OPT"""
        assert txt.OVERRIDE_OPT is not None  # == "--country --interactive --method --geoip"

    def test_txt_repo_server(self):
        """TEST: txt REPO_SERVER"""
        assert txt.REPO_SERVER is not None  # == "repo.manjaro.org"

    def test_txt_reset_tip(self):
        """TEST: txt RESET_TIP"""
        assert txt.RESET_TIP is not None  # == "pacman-mirrors -c all"

    def test_txt_prefix_tip(self):
        """TEST: txt PREFIX_TIP"""
        assert txt.PREFIX_TIP is not None  # == ": $mnt | /mnt/install"

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
