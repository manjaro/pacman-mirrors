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
        assert txt.HOUSTON == "Houston?! We have a problem."

    def test_txt_override_opt(self):
        """TEST: txt OVERRIDE_OPT"""
        assert txt.OVERRIDE_OPT == "--country --interactive --method --geoip"

    def test_txt_repo_server(self):
        """TEST: txt REPO_SERVER"""
        assert txt.REPO_SERVER == "repo.manjaro.org"

    def test_txt_reset_tip(self):
        """TEST: txt RESET_TIP"""
        assert txt.RESET_TIP == "pacman-mirrors -c all"

    def test_txt_prefix_tip(self):
        """TEST: txt PREFIX_TIP"""
        assert txt.PREFIX_TIP == ": $mnt | /mnt/install"

    # options
    def test_txt_opt_random(self):
        """TEST: txt OPT_RANDOM"""
        assert txt.OPT_RANDOM == " '-m/--method random' "

    def test_txt_opt_country(self):
        """TEST: txt OPT_COUNTRY"""
        assert txt.OPT_COUNTRY == " 'c/--country' "

    # mirror status constants
    def test_txt_lastsync_ok(self):
        """TEST: txt LASTSYNC_OK"""
        assert txt.LASTSYNC_OK == "24:00"  # last syncronize in the past 24 hours

    def test_txt_lastsync_na(self):
        """TEST: txt LASTSYNC_NA"""
        assert txt.LASTSYNC_NA == "9800:00"  # last syncronization not available

    def test_txt_server_bad(self):
        """TEST: txt SERVER_BAD"""
        assert txt.SERVER_BAD == "9999:99"  # default last syncronization status

    def test_txt_server_res(self):
        """TEST: txt SERVER_RES"""
        assert txt.SERVER_RES == "99.99"  # default response status

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
