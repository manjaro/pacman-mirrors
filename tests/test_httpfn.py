#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.functions import httpFn, configFn
from pacman_mirrors.pacman_mirrors import PacmanMirrors
from . import mock_configuration as mock

test_conf = {
    "branch": "stable",
    "branches": mock.BRANCHES,
    "config_file": mock.CONFIG_FILE,
    "custom_file": mock.CUSTOM_FILE,
    "method": "rank",
    "mirror_file": mock.MIRROR_FILE,
    "mirror_list": mock.MIRROR_LIST,
    "no_update": False,
    "country_pool": [],
    "protocols": [],
    "repo_arch": mock.REPO_ARCH,
    "status_file": mock.STATUS_FILE,
    "ssl_verify": True,
    "url_mirrors_json": mock.URL_MIRROR_JSON,
    "url_status_json": mock.URL_STATUS_JSON,
    "work_dir": mock.WORK_DIR
}


class TestHttpFn(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(httpFn, "get_geoip_country")
    @patch.object(configFn, "build_config")
    def test_geoip_available(self,
                             mock_build_config,
                             mock_get_geoip_country,
                             mock_os_getuid):
        """TEST: geoip country IS avaiable"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        mock_get_geoip_country.return_value = ["Denmark"]
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = configFn.build_config()
            app.command_line_parse()
            app.load_all_mirrors()
            app.selected_countries = httpFn.get_geoip_country()
            assert app.selected_countries == ["Denmark"]

    @patch("os.getuid")
    @patch.object(httpFn, "get_geoip_country")
    @patch.object(configFn, "build_config")
    def test_geoip_not_available(self,
                                 mock_build_config,
                                 mock_get_geoip_country,
                                 mock_os_getuid):
        """TEST: geoip country IS NOT available"""
        mock_os_getuid.return_value = 0
        mock_get_geoip_country.return_value = "Antarctica"
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = configFn.build_config()
            app.command_line_parse()
            app.load_all_mirrors()
            assert app.selected_countries == app.mirrors.country_pool

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
