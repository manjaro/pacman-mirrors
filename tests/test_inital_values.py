#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.pacman_mirrors import PacmanMirrors


class TestInitialValues(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    def test_initial_custom(self, mock_os_getuid):
        """TEST: custom is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            assert app.custom is False

    @patch("os.getuid")
    def test_initial_fasttrack(self, mock_os_getuid):
        """TEST: fasttrack is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            assert app.fasttrack is None

    @patch("os.getuid")
    def test_initial_geoip(self, mock_os_getuid):
        """TEST: geoip is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            assert app.geoip is False

    @patch("os.getuid")
    def test_initial_interactive(self, mock_os_getuid):
        """TEST: interactive is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            assert app.interactive is False

    @patch("os.getuid")
    def test_initial_max_wait_time(self, mock_os_getuid):
        """TEST: max_wait_time = 2"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            assert app.max_wait_time == 2

    @patch("os.getuid")
    def test_initial_network(self, mock_os_getuid):
        """TEST: network is True"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            assert app.network is True

    @patch("os.getuid")
    def test_initial_nodisplay(self, mock_os_getuid):
        """TEST: no_display is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            assert app.no_display is False

    @patch("os.getuid")
    def test_initial_quiet(self, mock_os_getuid):
        """TEST: quiet is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            assert app.quiet is False

    @patch("os.getuid")
    def test_initial_selected_countries(self, mock_os_getuid):
        """TEST: selected_countries = []"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            app.configfile = "conf/pacman-mirrors.conf"
            assert app.selected_countries == []

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
