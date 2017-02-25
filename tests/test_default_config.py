#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.pacman_mirrors import PacmanMirrors
from pacman_mirrors.configfn import ConfigFn


class TestDefaultConfig(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    def test_default_branch(self, mock_os_getuid):
        """TEST: config[branch] = stable"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            app.config = ConfigFn.build_config(app.configfile)
            assert app.config["branch"] == "stable"

    @patch("os.getuid")
    def test_default_method(self, mock_os_getuid):
        """TEST: config[method] = rank"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            app.config = ConfigFn.build_config(app.configfile)
            assert app.config["method"] == "rank"

    # @patch("os.getuid")
    # def test_default_mirrordir(self, mock_os_getuid):
    #     """TEST: config[mirror_dir] = mock/"""
    #     mock_os_getuid.return_value = 0
    #     with unittest.mock.patch("sys.argv",
    #                              ["pacman-mirrors",
    #                               "-g"]):
    #         app = PacmanMirrors()
    #         app.configfile = "conf/pacman-mirrors.conf"
    #         app.config = ConfigFn.build_config(app.configfile)
    #         assert app.config["mirror_dir"] == "mock/var/"

    # @patch("os.getuid")
    # def test_default_mirrorfile(self, mock_os_getuid):
    #     """TEST: config[mirror_file] = mock/mirrors.json"""
    #     mock_os_getuid.return_value = 0
    #     with unittest.mock.patch("sys.argv",
    #                              ["pacman-mirrors",
    #                               "-g"]):
    #         app = PacmanMirrors()
    #         app.configfile = "conf/pacman-mirrors.conf"
    #         app.config = ConfigFn.build_config(app.configfile)
    #         assert app.config["mirror_file"] == "mock/var/mirrors.json"

    # @patch("os.getuid")
    # def test_default_mirrorlist(self, mock_os_getuid):
    #     """TEST: config[mirror_list] = mock/mirrorlist"""
    #     mock_os_getuid.return_value = 0
    #     with unittest.mock.patch("sys.argv",
    #                              ["pacman-mirrors",
    #                               "-g"]):
    #         app = PacmanMirrors()
    #         app.configfile = "conf/pacman-mirrors.conf"
    #         app.config = ConfigFn.build_config(app.configfile)
    #         app.config["mirror_list"] = "mock/etc/mirrorlist"
    #         assert app.config["mirror_list"] == "mock/etc/mirrorlist"

    @patch("os.getuid")
    def test_default_noupdate(self, mock_os_getuid):
        """TEST: config[no_update] = False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            app.config = ConfigFn.build_config(app.configfile)
            assert app.config["no_update"] is False

    # @patch("os.getuid")
    # def test_default_onlycountry(self, mock_os_getuid):
    #     """TEST: config[only_country] = []"""
    #     mock_os_getuid.return_value = 0
    #     with unittest.mock.patch("sys.argv",
    #                              ["pacman-mirrors",
    #                               "-g"]):
    #         app = PacmanMirrors()
    #         app.config = {}
    #         app.config = ConfigFn.build_config(app.configfile)
    #         assert app.config["only_country"] == []

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
