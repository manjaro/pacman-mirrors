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
            # app.config_file = "conf/pacman-mirrors.conf"
            app.config = app.config_init()
            # app.command_line_parse()
            # app.load_server_lists()

    # @patch.object(pacman_mirrors.PacmanMirrors, "get_mirror_branch_timestamp")
    # def test_get_mirror_timestamp(self, mock_timestamp):
    #     """Extract timestamp from input"""
    #     mock_timestamp.return_value = "2017-02-06T07:18:43Z"
    #     app = pacman_mirrors.PacmanMirrors()
    #     mock_data = "date=2017-02-06T07:18:43Z"
    #     assert app.get_mirror_branch_timestamp(
    #         mock_data) == "2017-02-06T07:18:43Z"

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
