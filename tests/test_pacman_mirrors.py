#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import pacman_mirrors


class TestPacmanMirrors(unittest.TestCase):
    def setUp(self):
        pass

    @patch("os.getuid")
    def test_run(self, mock_os_getuid):
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv", ["pacman-mirrors", "-g", "-m", "random", "-d" "data/mirrors"]):
            pm = pacman_mirrors.PacmanMirrors()
            pm.command_line_parse()
            pm.load_server_lists()

    @patch("os.getuid")
    def test_run_country(self, mock_os_getuid):
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv", ["pacman-mirrors", "-g", "-c", "Germany", "-m", "random", "-d" "data/mirrors"]):
            pm = pacman_mirrors.PacmanMirrors()
            pm.command_line_parse()
            pm.load_server_lists()
            assert pm.config["only_country"] == ["Germany"]

    @patch("os.getuid")
    @patch.object(pacman_mirrors.PacmanMirrors, "get_geoip_country")
    def test_geoip_country_available(self, mock_geoip, mock_os_getuid):
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "France"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors", "-g", "--geoip", "-m", "random", "-d" "data/mirrors"]):
            pm = pacman_mirrors.PacmanMirrors()
            pm.command_line_parse()
            pm.load_server_lists()
            assert pm.config["only_country"] == ["France"]

    @patch("os.getuid")
    @patch.object(pacman_mirrors.PacmanMirrors, "get_geoip_country")
    def test_geoip_country_not_available(self, mock_geoip, mock_os_getuid):
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "Antarctica"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors", "-g", "--geoip", "-m", "random", "-d" "data/mirrors"]):
            pm = pacman_mirrors.PacmanMirrors()
            pm.config["only_country"] = []
            pm.command_line_parse()
            pm.load_server_lists()
            assert pm.config["only_country"] == pm.available_countries

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
