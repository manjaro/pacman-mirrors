#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import txt


class TestTextMessageTypes(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    def test_txt_msg_type_error(self):
        """TEST: txt MESSAGE TYPE ERROR"""
        assert txt.ERROR is not None

    def test_txt_msg_type_info(self):
        """TEST: txt MESSAGE TYPE INFO"""
        assert txt.INFO is not None

    def test_txt_msg_type_warn(self):
        """TEST: txt MESSAGE TYPE WARN"""
        assert txt.WARN is not None

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
