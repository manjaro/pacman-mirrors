#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""
import os
import unittest
from unittest.mock import patch

from pacman_mirrors import configfn
from pacman_mirrors import filefn
from pacman_mirrors import httpfn
from pacman_mirrors.pacman_mirrors import PacmanMirrors
from . import mock_configuration as conf


class TestPacmanMirrors(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_full_run_random(self, mock_build_config, mock_os_getuid):
        """TEST: pacman-mirrors -c all -m random"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = {
            "branch": "stable",
            "branches": conf.BRANCHES,
            "config_file": conf.CONFIG_FILE,
            "custom_file": conf.CUSTOM_FILE,
            "fallback_file": conf.FALLBACK,
            "method": "rank",
            "mirror_dir": conf.MIRROR_DIR,
            "mirror_file": conf.MIRROR_FILE,
            "mirror_list": conf.MIRROR_LIST,
            "no_update": False,
            "only_country": [],
            "repo_arch": conf.REPO_ARCH,
            "status_file": conf.STATUS_FILE,
            "ssl": False,
            "url_mirrors_json": conf.URL_MIRROR_JSON,
            "url_status_json": conf.URL_STATUS_JSON
        }
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "all",
                                  "-m", "random"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            filefn.dir_must_exist(app.config["mirror_dir"])
            app.command_line_parse()
            app.load_all_mirrors()
            # network check
            app.network = httpfn.ping_host("google.com", 3)
            # all methods is available
            if app.network:
                httpfn.update_mirrors(app.config)
                # actual generation
                if app.fasttrack:
                    app.build_fasttrack_mirror_list(app.fasttrack)
                else:
                    if app.interactive:
                        app.build_interactive_mirror_list()
                    else:
                        app.build_common_mirror_list()

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_full_run_fasttrack(self, mock_build_config, mock_os_getuid):
        """TEST: pacman-mirrors -f 5"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = {
            "branch": "stable",
            "branches": conf.BRANCHES,
            "config_file": conf.CONFIG_FILE,
            "custom_file": conf.CUSTOM_FILE,
            "fallback_file": conf.FALLBACK,
            "method": "rank",
            "mirror_dir": conf.MIRROR_DIR,
            "mirror_file": conf.MIRROR_FILE,
            "mirror_list": conf.MIRROR_LIST,
            "no_update": False,
            "only_country": [],
            "repo_arch": conf.REPO_ARCH,
            "status_file": conf.STATUS_FILE,
            "ssl": False,
            "url_mirrors_json": conf.URL_MIRROR_JSON,
            "url_status_json": conf.URL_STATUS_JSON
        }
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f", "5"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            filefn.dir_must_exist(app.config["mirror_dir"])
            app.command_line_parse()
            app.load_all_mirrors()
            # network check
            app.network = httpfn.is_connected("https://manjaro.org", 2)
            # all methods is available
            if app.network:
                httpfn.update_mirrors(app.config)
                app.load_all_mirrors()
                # actual generation
                if app.fasttrack:
                    app.build_fasttrack_mirror_list(app.fasttrack)
                else:
                    if app.interactive:
                        app.build_interactive_mirror_list()
                    else:
                        app.build_common_mirror_list()

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_full_run_rank(self, mock_build_config, mock_os_getuid):
        """TEST: pacman-mirrors -c all -m random"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = {
            "branch": "stable",
            "branches": conf.BRANCHES,
            "config_file": conf.CONFIG_FILE,
            "custom_file": conf.CUSTOM_FILE,
            "fallback_file": conf.FALLBACK,
            "method": "rank",
            "mirror_dir": conf.MIRROR_DIR,
            "mirror_file": conf.MIRROR_FILE,
            "mirror_list": conf.MIRROR_LIST,
            "no_update": False,
            "only_country": [],
            "repo_arch": conf.REPO_ARCH,
            "status_file": conf.STATUS_FILE,
            "ssl": False,
            "url_mirrors_json": conf.URL_MIRROR_JSON,
            "url_status_json": conf.URL_STATUS_JSON
        }
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "all"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            filefn.dir_must_exist(app.config["mirror_dir"])
            app.command_line_parse()
            # network check
            app.network = httpfn.is_connected("https://manjaro.org", 2)
            # all methods is available
            if app.network:
                httpfn.update_mirrors(app.config)
                # actual generation
                app.load_all_mirrors()
                if app.fasttrack:
                    app.build_fasttrack_mirror_list(app.fasttrack)
                else:
                    if app.interactive:
                        app.build_interactive_mirror_list()
                    else:
                        app.build_common_mirror_list()

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
