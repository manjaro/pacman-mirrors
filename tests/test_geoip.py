#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.httpfn import HttpFn
from pacman_mirrors.pacman_mirrors import PacmanMirrors
from pacman_mirrors.configfn import ConfigFn


class TestGeoip(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(HttpFn, "get_geoip_country")
    def test_geoip_available(self, mock_geoip, mock_os_getuid):
        """TEST: Geoip country IS avaiable"""
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "France"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = ConfigFn.build_config()
            app.command_line_parse()
            app.load_all_mirrors()
            assert app.selected_countries == "France"

    @patch("os.getuid")
    @patch.object(HttpFn, "get_geoip_country")
    def test_geoip_not_available(self, mock_geoip, mock_os_getuid):
        """TEST: Geoip country IS NOT available"""
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "Antarctica"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = ConfigFn.build_config()
            app.command_line_parse()
            app.load_all_mirrors()
            assert app.selected_countries == app.mirrors.countrylist

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
