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

test_conf = {
    "to_be_removed": conf.TO_BE_REMOVED,
    "branch": "stable",
    "branches": conf.BRANCHES,
    "config_file": conf.CONFIG_FILE,
    "custom_file": conf.CUSTOM_FILE,
    "method": "rank",
    "work_dir": conf.WORK_DIR,
    "mirror_file": conf.MIRROR_FILE,
    "mirror_list": conf.MIRROR_LIST,
    "no_update": False,
    "only_country": [],
    "protocols": [],
    "repo_arch": conf.REPO_ARCH,
    "status_file": conf.STATUS_FILE,
    "ssl_verify": True,
    "url_mirrors_json": conf.URL_MIRROR_JSON,
    "url_status_json": conf.URL_STATUS_JSON
}


class TestDefaultConfig(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_branch(self, mock_build_config, mock_os_getuid):
        """TEST: config[branch] = stable"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            assert app.config["branch"] == "stable"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_method(self, mock_build_config, mock_os_getuid):
        """TEST: config[method] = rank"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            assert app.config["method"] == "rank"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_mirrordir(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_dir] = tests/mock/var/"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            assert app.config["work_dir"] == "tests/mock/var/"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_mirrorfile(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_file] = tests/mock/usr/mirrors.json"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            assert app.config["mirror_file"] == "tests/mock/usr/mirrors.json"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_mirrorlist(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_list] = tests/mock/etc/mirrorlist"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            assert app.config["mirror_list"] == "tests/mock/etc/mirrorlist"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_noupdate(self, mock_build_config, mock_os_getuid):
        """TEST: config[no_update] = False"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            assert app.config["no_update"] is False

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_onlycountry(self, mock_build_config, mock_os_getuid):
        """TEST: config[only_country] = []"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            assert app.config["only_country"] == []

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
