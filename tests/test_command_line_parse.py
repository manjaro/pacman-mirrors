#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.pacman_mirrors import PacmanMirrors
from pacman_mirrors import configfn
from . import mock_configuration as conf


class TestCommandLineParse(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_branch_unstable(self, mock_build_config, mock_os_getuid):
        """TEST: CLI config[branch] from ARG '-b unstable'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-b", "unstable"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.config["branch"] == "unstable"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_branch_testing(self, mock_build_config, mock_os_getuid):
        """TEST: CLI config[branch] from ARG '-b testing'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-b", "testing"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.config["branch"] == "testing"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_method(self, mock_build_config, mock_os_getuid):
        """TEST: CLI config[method] from ARG '-m random'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-m", "random"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.config["method"] == "random"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_mirrordir(self, mock_build_config, mock_os_getuid):
        """TEST: CLI config[mirror_dir] from ARG '-d /another/dir'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-d", "/another/dir/"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.config["mirror_dir"] == "/another/dir/"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_mirrorlist(self, mock_build_config, mock_os_getuid):
        """TEST: CLI config[mirror_list] from ARG '-o /another/list'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-o", "/another/list"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.config["mirror_list"] == "/another/list"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_onlycountry(self, mock_build_config, mock_os_getuid):
        """TEST: CLI config[only_country] from ARG '-c France,Germany'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "France,Germany"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.config["only_country"] == ["France", "Germany"]

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_custom_country(self, mock_build_config, mock_os_getuid):
        """TEST: CLI custom is True from ARG '-c Denmark'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c Denmark"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.custom is True

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_geoip(self, mock_build_config, mock_os_getuid):
        """TEST: CLI geoip is True from ARG '--geoip'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.geoip is True

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_fasttrack(self, mock_build_config, mock_os_getuid):
        """TEST: CLI fasttrack is 5 from ARG '-f 5'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f 5"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.fasttrack == 5

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_interactive(self, mock_build_config, mock_os_getuid):
        """TEST: CLI interactive is true from ARG '-i'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-i"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.interactive is True

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_max_wait_time(self, mock_build_config, mock_os_getuid):
        """TEST: CLI max_wait_time is 5 from ARG '-t 5'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-t 5"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.max_wait_time == 5

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_arg_quiet(self, mock_build_config, mock_os_getuid):
        """TEST: CLI quiet is True from ARG '-q'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = conf.test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-q"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            app.command_line_parse()
            assert app.quiet is True

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
