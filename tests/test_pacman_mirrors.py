#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.httpfn import HttpFn
from pacman_mirrors.pacman_mirrors import PacmanMirrors


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
                                  "-g",
                                  "-c", "all",
                                  "-m", "random"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
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
    def test_run_country(self, mock_os_getuid):
        """Single country from argument -c"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g",
                                  "-c", "Germany"]):
            app = PacmanMirrors()
            app.config = app.build_config()
            app.command_line_parse()
            app.network = HttpFn.update_mirrors()
            app.load_all_mirrors()

            assert app.config["only_country"] == ["Germany"]

    # @patch("os.getuid")
    # @patch.object(HttpFn, "get_geoip_country")
    # def test_geoip_is_available(self, mock_geoip, mock_os_getuid):
    #     """Geoip mirror country IS avaiable"""
    #     mock_os_getuid.return_value = 0
    #     mock_geoip.return_value = "France"
    #     with unittest.mock.patch("sys.argv",
    #                              ["pacman-mirrors",
    #                               "--geoip"]):
    #         app = PacmanMirrors()
    #         app.config = app.build_config()
    #         app.command_line_parse()
    #         app.load_all_mirrors()
    #
    #         assert app.selected_countries == ["France"]
    #
    # @patch("os.getuid")
    # @patch.object(HttpFn, "get_geoip_country")
    # def test_geoip_not_available(self, mock_geoip, mock_os_getuid):
    #     """Geoip mirror country IS NOT available"""
    #     mock_os_getuid.return_value = 0
    #     mock_geoip.return_value = "Antarctica"
    #     with unittest.mock.patch("sys.argv",
    #                              ["pacman-mirrors",
    #                               "-g",
    #                               "--geoip"]):
    #         app = PacmanMirrors()
    #         app.config = app.build_config()
    #         app.command_line_parse()
    #         app.load_all_mirrors()
    #         app.config["only_country"] = []
    #
    #         assert app.config["only_country"] == app.mirrors.countrylist

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
