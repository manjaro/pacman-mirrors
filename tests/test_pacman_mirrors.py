#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import pacman_mirrors
from pacman_mirrors.configuration import MIRROR_DIR


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
                                  "-m", "random"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config = app.load_conf()
            app.command_line_parse()
            app.FileFn.dir_must_exist(MIRROR_DIR)
            app.manjaro_online = app.HttpFn.manjaro_online_update()
            app.load_mirror_file()
            app.validate_custom_config()
            app.validate_country_selection()
            app.gen_server_lists()
            if app.interactive:
                app.gen_mirror_list_interactive()
            else:
                app.gen_mirror_list_common()

    @patch("os.getuid")
    def test_run_country(self, mock_os_getuid):
        """Single country via commandline"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "Germany"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config = app.load_conf()
            app.command_line_parse()
            app.FileFn.dir_must_exist(MIRROR_DIR)
            app.manjaro_online = app.HttpFn.manjaro_online_update()
            app.load_mirror_file()
            app.validate_custom_config()
            app.validate_country_selection()
            assert app.only_country == ["Germany"]

    @patch("os.getuid")
    @patch.object(pacman_mirrors.HttpFn, "get_geoip_country")
    def test_get_geoip_country(self, mock_geoip, mock_os_getuid):
        """Geoip country IS available"""
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "France"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config = app.load_conf()
            app.command_line_parse()
            app.FileFn.dir_must_exist(MIRROR_DIR)
            app.manjaro_online = app.HttpFn.manjaro_online_update()
            app.load_mirror_file()
            app.validate_custom_config()
            app.validate_country_selection()
            assert app.only_country == ["France"]

    @patch("os.getuid")
    @patch.object(pacman_mirrors.HttpFn, "get_geoip_country")
    def test_get_geoip_country(self, mock_geoip, mock_os_getuid):
        """Geoip country IS NOT available"""
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "Antartica"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config = app.load_conf()
            app.command_line_parse()
            app.FileFn.dir_must_exist(MIRROR_DIR)
            app.manjaro_online = app.HttpFn.manjaro_online_update()
            app.load_mirror_file()
            app.validate_custom_config()
            app.validate_country_selection()
            assert app.only_country == app.mirrors.countrylist

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
