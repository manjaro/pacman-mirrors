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
    """Pacman Mirrors Test suite"""
    def setUp(self):
        pass

    @patch("os.getuid")
    def test_run(self, mock_os_getuid):
        """Run pacman-mirrors"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g",
                                  "-m", "random",
                                  "-d", "data/mirrors"]):
            app = pacman_mirrors.PacmanMirrors()
            app.command_line_parse()
            app.load_server_lists()

    @patch("os.getuid")
    def test_run_country(self, mock_os_getuid):
        """Single country via commandline"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g",
                                  "-c", "Germany",
                                  "-m", "random",
                                  "-d", "data/mirrors"]):
            app = pacman_mirrors.PacmanMirrors()
            app.command_line_parse()
            app.load_server_lists()
            assert app.config["only_country"] == ["Germany"]

    @patch("os.getuid")
    @patch.object(pacman_mirrors.PacmanMirrors, "get_geoip_country")
    def test_geoip_is_available(self, mock_geoip, mock_os_getuid):
        """Geoip mirror country is avaiable"""
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "France"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g",
                                  "--geoip",
                                  "-m", "random",
                                  "-d", "data/mirrors"]):
            app = pacman_mirrors.PacmanMirrors()
            app.command_line_parse()
            app.load_server_lists()
            assert app.config["only_country"] == ["France"]

    @patch("os.getuid")
    @patch.object(pacman_mirrors.PacmanMirrors, "get_geoip_country")
    def test_geoip_not_available(self, mock_geoip, mock_os_getuid):
        """Geoip mirror country is not available"""
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "Antarctica"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g",
                                  "--geoip",
                                  "-m", "random",
                                  "-d", "data/mirrors"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config["only_country"] = []
            app.command_line_parse()
            app.load_server_lists()
            assert app.config["only_country"] == app.available_countries

    @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_response_time")
    def test_resp_time_calc(self, mock_calc):
        """Calculate mirror response time"""
        mock_calc.return_value = "0.067"
        app = pacman_mirrors.PacmanMirrors()
        assert app.get_mirror_response_time(
            "1486371026.6549892", "1486371026.7216527") == "0.067"

    @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_branch_last_sync")
    def test_last_sync_calc(self, mock_calc):
        """Calculate mirror last_sync offset"""
        mock_calc.return_value = "20:19"
        app = pacman_mirrors.PacmanMirrors()
        assert app.get_mirror_branch_last_sync(
            "2017-02-06 09:50:26.544456", "2017-02-05 13:31:09") == "20:19"

    @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_url")
    def test_get_mirror_url(self, mock_url):
        """Extract mirror url from input"""
        mock_url.return_value = "http://mirror.domain.tld"
        app = pacman_mirrors.PacmanMirrors()
        assert app.get_mirror_url(
            "Server = http://mirror.domain.tld") == "http://mirror.domain.tld"

    @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_country")
    def test_get_mirror_country(self, mock_country):
        """Extract mirror country from input"""
        mock_country.return_value = "France"
        app = pacman_mirrors.PacmanMirrors()
        assert app.get_mirror_country(
            "## Country       : France") == "France"
        assert app.get_mirror_country(
            "## Location      : France") == "France"
        assert app.get_mirror_country(
            "[France]") == "France"

    @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_branch_timestamp")
    def test_get_mirror_timestamp(self, mock_timestamp):
        """Extract timestamp from input"""
        mock_timestamp.return_value = "2017-02-06T07:18:43Z"
        mock_data = "###\n### BoxIt branch state file\n###\n\n# Unique hash code representing current branch state.\n# This hash code changes as soon as anything changes in this branch.\nstate=9a255e4d625f6d3ad2643a3ff1421ad02e731938\n\n# Date and time of the last branch change.\ndate=2017-02-06T07:18:43Z"

        app = pacman_mirrors.PacmanMirrors()

        assert app.get_mirror_branch_timestamp(mock_data) == "2017-02-06T07:18:43Z"

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
