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
from pacman_mirrors.configfn import ConfigFn
from pacman_mirrors.filefn import FileFn


class TestPacmanMirrors(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    def test_run(self, mock_os_getuid):
        """TEST: pacman-mirrors -qc all -m random"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-qc", "all",
                                  "-m", "random"]):
            app = PacmanMirrors()
            app.config = ConfigFn.build_config()
            app.command_line_parse()
            FileFn.dir_must_exist(app.config["mirror_dir"])
            app.network = HttpFn.update_mirrors()
            app.load_all_mirrors()
            # actual generation
            if app.fasttrack:
                app.build_fasttrack_mirror_list(app.fasttrack)
            else:
                if app.interactive:
                    app.build_interactive_mirror_list()
                else:
                    app.build_common_mirror_list()

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
