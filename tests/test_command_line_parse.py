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
    def test_args_custom_country(self, mock_os_getuid):
        """TEST: custom is True from arg -c Denmark"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c Denmark"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.custom is True

    @patch("os.getuid")
    def test_args_geoip(self, mock_os_getuid):
        """TEST: geoip True from arg --geoip"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.geoip is True

    @patch("os.getuid")
    def test_args_fasttrack(self, mock_os_getuid):
        """TEST: fasttrack is 5 from arg -f 5"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f 5"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.fasttrack == 5

    @patch("os.getuid")
    def test_args_interactive(self, mock_os_getuid):
        """TEST: interactive is true from arg -i"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-i"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.interactive is True

    @patch("os.getuid")
    def test_args_max_wait_time(self, mock_os_getuid):
        """TEST: max_wait_time is 5 from arg -t 5"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-t 5"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.max_wait_time == 5

    @patch("os.getuid")
    def test_args_quiet(self, mock_os_getuid):
        """TEST: quiet is True from arg -q"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-q"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            assert app.quiet is True

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
