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
from pacman_mirrors.miscfn import MiscFn


class TestArgCountryList(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    def test_arg_country_list(self, mock_os_getuid):
        """Geoip mirror country IS avaiable"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c Denmark,Norway,Sweden"]):
            app = PacmanMirrors()
            app.config = ConfigFn.build_config()
            app.config["config_file"] = "conf/pacman-mirrors.conf"
            app.command_line_parse()
            # MiscFn.debug("test_arg_country_list",
            #              "config[only_country)",
            #              app.config["only_country"])
            assert app.config["only_country"] == ["Denmark", "Norway", "Sweden"]
            # app.load_all_mirrors()
            # assert app.selected_countries == "France"

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
