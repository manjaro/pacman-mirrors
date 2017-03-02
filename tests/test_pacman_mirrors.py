#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import configfn
from pacman_mirrors import filefn
from pacman_mirrors import httpfn
from pacman_mirrors.pacman_mirrors import PacmanMirrors
from . import test_configuration as conf


class TestPacmanMirrors(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_run(self, mock_build_config, mock_os_getuid):
        """TEST: pacman-mirrors -qc all -m random"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = {
            "branch": "stable",
            "config_file": conf.CONFIG_FILE,
            "custom_file": conf.CUSTOM_FILE,
            "method": "rank",
            "mirror_dir": conf.MIRROR_DIR,
            "mirror_file": conf.MIRROR_FILE,
            "mirror_list": conf.MIRROR_LIST,
            "no_update": False,
            "only_country": [],
        }
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "all",
                                  "-m", "random"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            filefn.dir_must_exist(conf.MIRROR_DIR)
            app.command_line_parse()
            app.load_all_mirrors()
            app.network = httpfn.update_mirrors()
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
