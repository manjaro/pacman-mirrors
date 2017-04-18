#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import httpfn
from pacman_mirrors.pacman_mirrors import PacmanMirrors
from pacman_mirrors import configfn
from . import mock_configuration as conf


class TestHttpFn(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(httpfn, "get_geoip_country")
    @patch.object(configfn, "build_config")
    def test_geoip_available(self, mock_build_config, mock_get_geoip_country, mock_os_getuid):
        """TEST: Geoip country IS avaiable"""
        mock_os_getuid.return_value = 0
        mock_get_geoip_country.return_value = "France"
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            app.command_line_parse()
            app.load_all_mirrors()
            assert app.selected_countries == "France"

    @patch("os.getuid")
    @patch.object(httpfn, "get_geoip_country")
    @patch.object(configfn, "build_config")
    def test_geoip_not_available(self, mock_build_config, mock_get_geoip_country, mock_os_getuid):
        """TEST: Geoip country IS NOT available"""
        mock_os_getuid.return_value = 0
        mock_get_geoip_country.return_value = "Antarctica"
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            app.command_line_parse()
            app.load_all_mirrors()
            assert app.selected_countries == app.mirrors.countrylist

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
