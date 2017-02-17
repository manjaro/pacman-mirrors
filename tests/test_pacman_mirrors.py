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
                                 ["pacman-mirrors",
                                  "-m", "random"]):
            app = pacman_mirrors.PacmanMirrors()
            # if os.path.isfile(O_CUST_FILE):
            #     app.CustomFn.convert_to_json()
            # else:
            #     app.FileFn.check_directory(MIRROR_DIR)
            # app.manjaro_online = app.HttpFn.manjaro_online_update()
            app.config = app.load_conf()
            app.command_line_parse()
            app.load_mirror_file()
            app.validate_custom_config()
            app.validate_country_selection()
            app.gen_server_lists()
            if app.interactive:
                app.gen_mirror_list_interactive()
            else:
                app.gen_mirror_list_common()

    @patch.object(pacman_mirrors.HttpFn, "get_geoip_country")
    def test_get_geoip_country(self, mock_geoip):
        """Geoip country IS available"""
        mock_geoip.return_value = "France"
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = pacman_mirrors.PacmanMirrors()
            app.config = app.load_conf()
            app.command_line_parse()
            app.load_mirror_file()
            app.validate_custom_config()
            app.validate_country_selection()
            app.gen_server_lists()
            assert app.only_country == ["France"]

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
