#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""
import unittest
from unittest.mock import patch

from pacman_mirrors.functions import fileFn, configFn
from pacman_mirrors.functions import httpFn
from pacman_mirrors.pacman_mirrors import PacmanMirrors
from . import mock_configuration as conf

test_conf = {
    "branch": "stable",
    "branches": conf.BRANCHES,
    "config_file": conf.CONFIG_FILE,
    "custom_file": conf.CUSTOM_FILE,
    "method": "rank",
    "work_dir": conf.WORK_DIR,
    "mirror_file": conf.MIRROR_FILE,
    "mirror_list": conf.MIRROR_LIST,
    "no_update": False,
    "country_pool": [],
    "protocols": [],
    "repo_arch": conf.REPO_ARCH,
    "status_file": conf.STATUS_FILE,
    "ssl_verify": True,
    "url_mirrors_json": conf.URL_MIRROR_JSON,
    "url_status_json": conf.URL_STATUS_JSON,
    "x32": False
}


class TestPacmanMirrors(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(configFn, "build_config")
    def test_full_run_fasttrack(self,
                                mock_build_config,
                                mock_os_getuid):
        """TEST: pacman-mirrors -f5"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f5"]):
            app = PacmanMirrors()
            app.config = configFn.build_config()
            fileFn.create_dir(test_conf["work_dir"])
            app.command_line_parse()
            httpFn.update_mirrors(app.config)
            app.load_all_mirrors()
            app.build_fasttrack_mirror_list(app.fasttrack)

    @patch("os.getuid")
    @patch.object(configFn, "build_config")
    def test_full_run_random(self,
                             mock_build_config,
                             mock_os_getuid):
        """TEST: pacman-mirrors -c all -m random"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "all",
                                  "-m", "random"]):
            app = PacmanMirrors()
            app.config = configFn.build_config()
            fileFn.create_dir(test_conf["work_dir"])
            app.command_line_parse()
            httpFn.update_mirrors(app.config)
            app.load_all_mirrors()
            app.build_common_mirror_list()

    @patch("os.getuid")
    @patch.object(configFn, "build_config")
    def test_full_run_rank(self,
                           mock_build_config,
                           mock_os_getuid):
        """TEST: pacman-mirrors -c all"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "all"]):
            app = PacmanMirrors()
            app.config = configFn.build_config()
            fileFn.create_dir(test_conf["work_dir"])
            app.command_line_parse()
            httpFn.update_mirrors(app.config)
            app.load_all_mirrors()
            app.build_common_mirror_list()

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
