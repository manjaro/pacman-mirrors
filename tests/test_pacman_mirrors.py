#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import pacman_mirrors
from pacman_mirrors.validfn import ValidFn


class TestPacmanMirrors(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    def test_run(self, mock_os_getuid):
        """Run pacman-mirrors"""
        mock_os_getuid.return_value = 0

        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--quiet",
                                  "-m", "random"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config = app.load_conf()
            app.command_line_parse()
            app.load_mirror_file()
            app.validate_custom_config()
            app.validate_country_selection()
            app.gen_server_lists()
            if app.interactive:
                app.gen_mirror_list_interactive()
            else:
                app.gen_mirror_list_common()

    @patch("os.getuid")
    def test_country_commandline(self, mock_os_getuid):
        """Single country from argument"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "Germany"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config = app.load_conf()
            app.command_line_parse()
            app.load_mirror_file()
            app.validate_custom_config()
            app.validate_country_selection()
            assert app.only_country == ["Germany"]

    @patch("os.getuid")
    @patch.object(pacman_mirrors.HttpFn, "get_geoip_country")
    def test_get_geoip_country(self, mock_os_getuid, mock_geoip):
        """Geoip country IS available"""
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "France"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config = app.load_conf()
            app.command_line_parse()
            app.load_mirror_file()
            app.validate_custom_config()
            app.validate_country_selection()
            assert app.only_country == ["France"]

    @patch("os.getuid")
    @patch.object(pacman_mirrors.HttpFn, "get_geoip_country")
    def test_get_geoip_country(self, mock_os_getuid, mock_geoip):
        """Geoip country IS NOT available"""
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "Antartica"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config = app.load_conf()
            app.command_line_parse()
            app.load_mirror_file()
            app.validate_custom_config()
            app.validate_country_selection()
            assert app.only_country == app.mirrors.countrylist

    @patch("os.getuid")
    @patch.object(pacman_mirrors.ValidFn, "is_custom_config_valid")
    def test_valid_country_list(self, mock_os_getuid, mock_custom_valid):
        """Custom config IS valid"""
        mock_os_getuid.return_value = 0
        mock_custom_valid.returvalue = True
        mock_only_in = ["Custom"]
        mock_list_in = ["Denmark", "France", "Austria"]
        mock_geoip_in = False
        mock_result = ([], True)
        app = pacman_mirrors.PacmanMirrors()
        assert app.ValidFn.get_valid_country_list(
            mock_only_in, mock_list_in, mock_geoip_in) == mock_result

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
