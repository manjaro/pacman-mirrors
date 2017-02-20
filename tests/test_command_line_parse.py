#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.pacman_mirrors import PacmanMirrors


class TestCommandLineParse(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    def test_args_branch_unstable(self, mock_os_getuid):
        """TEST: config[branch] from arg -b unstable"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-b", "unstable"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.config["branch"] == "unstable"

    @patch("os.getuid")
    def test_args_branch_testing(self, mock_os_getuid):
        """TEST: config[branch] from arg -b testing"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-b", "testing"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.config["branch"] == "testing"

    @patch("os.getuid")
    def test_args_method(self, mock_os_getuid):
        """TEST: config[method] from arg -m random"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-m", "random"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.config["method"] == "random"

    @patch("os.getuid")
    def test_args_mirrordir(self, mock_os_getuid):
        """TEST: config[mirror_dir] from arg -d /another/dir"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-d", "/another/dir/"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.config["mirror_dir"] == "/another/dir/"

    @patch("os.getuid")
    def test_args_mirrorlist(self, mock_os_getuid):
        """TEST: config[mirror_list] from arg -o /another/list"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-o", "/another/list"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.config["mirror_list"] == "/another/list"

    @patch("os.getuid")
    def test_args_onlycountry(self, mock_os_getuid):
        """TEST: config[only_country] from arg -c France,Germany"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "France,Germany"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.config["only_country"] == ["France", "Germany"]

    @patch("os.getuid")
    def test_args_geoip(self, mock_os_getuid):
        """TEST: self.geoip from arg --geoip"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.geoip is True

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
