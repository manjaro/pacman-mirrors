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
            app.config_file = "conf/pacman-mirrors.conf"
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
            app.config_file = "conf/pacman-mirrors.conf"
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
            app.config_file = "conf/pacman-mirrors.conf"
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
            app.config_file = "conf/pacman-mirrors.conf"
            app.config["only_country"] = []
            app.command_line_parse()
            app.load_server_lists()
            assert app.config["only_country"] == app.available_countries

    @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_response_time")
    def test_resp_time_calc(self, mock_calc):
        """Calculate mirror response time"""
        app = pacman_mirrors.PacmanMirrors()
        app.config_file = "conf/pacman-mirrors.conf"
        mock_calc.return_value = "0.067"
        assert app.get_mirror_response_time(
            "1486371026.6549892", "1486371026.7216527") == "0.067"
        mock_calc.return_value = "0.047"
        assert app.get_mirror_response_time(
            "1486371026.7686312", "1486371026.8155131") == "0.047"
        mock_calc.return_value = "0.156"
        assert app.get_mirror_response_time(
            "1486371026.815664", "1486371026.9718077") == "0.156"

    @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_branch_last_sync")
    def test_last_sync_calc(self, mock_calc):
        """Calculate mirror last_sync offset"""
        app = pacman_mirrors.PacmanMirrors()
        app.config_file = "conf/pacman-mirrors.conf"
        mock_calc.return_value = "2189:29"
        assert app.get_mirror_branch_last_sync(
            "2017-02-06 11:39:14.610344", "2016-11-07 06:09:51") == "2189:29"
        mock_calc.return_value = "22:08"
        assert app.get_mirror_branch_last_sync(
            "2017-02-06 11:39:14.866841", "2017-02-05 13:31:09") == "22:08"
        mock_calc.return_value = "04:20"
        assert app.get_mirror_branch_last_sync(
            "2017-02-06 11:39:23.523478", "2017-02-06 07:18:43") == "04:20"

    @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_url")
    def test_get_mirror_url(self, mock_url):
        """Extract mirror url from input"""
        mock_url.return_value = "http://mirror.domain.tld"
        app = pacman_mirrors.PacmanMirrors()
        app.config_file = "conf/pacman-mirrors.conf"
        mock_data = "Server = http://mirror.domain.tld"
        assert app.get_mirror_url(mock_data) == "http://mirror.domain.tld"

    @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_country")
    def test_get_mirror_country(self, mock_country):
        """Extract mirror country from input"""
        mock_country.return_value = "France"
        app = pacman_mirrors.PacmanMirrors()
        app.config_file = "conf/pacman-mirrors.conf"
        mock_data = "## Country       : France"
        assert app.get_mirror_country(mock_data) == "France"
        mock_data = "## Location      : France"
        assert app.get_mirror_country(mock_data) == "France"
        mock_data = "[France]"
        assert app.get_mirror_country(mock_data) == "France"

    @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_branch_timestamp")
    def test_get_mirror_timestamp(self, mock_timestamp):
        """Extract timestamp from input"""
        mock_timestamp.return_value = "2017-02-06T07:18:43Z"
        app = pacman_mirrors.PacmanMirrors()
        app.config_file = "conf/pacman-mirrors.conf"
        mock_data = "date=2017-02-06T07:18:43Z"
        assert app.get_mirror_branch_timestamp(mock_data) == "2017-02-06T07:18:43Z"

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
