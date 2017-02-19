#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.mirrorfn import MirrorFn


class TestPacmanMirrors(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    # @patch.object(MirrorFn, "build_country_list")
    # def test_build_list(self, mock_country_list):
    #     """TEST: Build country list"""
    #     mock_onlycountry = ["all"]
    #     mock_countrylist = ["Denmark", "France", "Austria"]
    #     assert MirrorFn.build_country_list(
    #         mock_onlycountry, mock_countrylist) == ["Denmark", "France", "Austria"]

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
