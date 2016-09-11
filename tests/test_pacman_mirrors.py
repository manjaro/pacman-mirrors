#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest import mock
from unittest.mock import patch

from pacman_mirrors import pacman_mirrors


class TestPacmanMirrors(unittest.TestCase):
    def setUp(self):
        pass

    @patch("os.getuid")
    def test_run(self, mock_os_getuid):
        mock_os_getuid.return_value = 0
        with unittest.mock.patch('sys.argv', ["pacman-mirrors", "-g", "-m", "random"]):
            pm = pacman_mirrors.PacmanMirrors()
            pm.run()

    @patch("os.getuid")
    def test_run_country(self, mock_os_getuid):
        mock_os_getuid.return_value = 0
        with unittest.mock.patch('sys.argv', ["pacman-mirrors", "-g", "-c", "Germany", "-m", "random"]):
            pm = pacman_mirrors.PacmanMirrors()
            pm.run()
            assert pm.only_country == ["Germany"]

    @patch("os.getuid")
    @patch.object(pacman_mirrors.PacmanMirrors, 'get_geoip_country')
    def test_geoip_country_available(self, mock_geoip, mock_os_getuid):
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "France"
        with unittest.mock.patch('sys.argv',
                                 ["pacman-mirrors", "-g", "--geoip", "-m", "random"]):
            pm = pacman_mirrors.PacmanMirrors()
            pm.run()
            assert pm.only_country == ["France"]

    @patch("os.getuid")
    @patch.object(pacman_mirrors.PacmanMirrors, 'get_geoip_country')
    def test_geoip_country_not_available(self, mock_geoip, mock_os_getuid):
        mock_os_getuid.return_value = 0
        mock_geoip.return_value = "testetestes"
        with unittest.mock.patch('sys.argv',
                                 ["pacman-mirrors", "-g", "--geoip", "-m", "random"]):
            pm = pacman_mirrors.PacmanMirrors()
            pm.only_country = []
            pm.run()
            assert pm.only_country == pm.available_countries

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
