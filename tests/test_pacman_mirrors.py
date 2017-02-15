#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import pacman_mirrors


class TestPacmanMirrors(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        pass

    @patch("os.getuid")
    def test_run(self, mock_os_getuid):
        """Run pacman-mirrors"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config = app.config_init()

    @patch.object(
        pacman_mirrors.HttpFn, "get_geoip_country")
    def test_get_geoip_country(self, mock_geoip):
        """Geoip country IS available"""
        mock_countries = ["France", "Germany", "Denmark"]
        mock_geoip.return_value = "France"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = pacman_mirrors.PacmanMirrors()
        app.available_countries = mock_countries
        assert app.config["only_country"] == ["France"]

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
