#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import txt


class TestTextErrorTypes(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    def test_txt_error_type_timeout(self):
        """TEST: txt ERROR TYPE TIMEOUT"""
        assert txt.TIMEOUT is not None

    def test_txt_error_type_http_exception(self):
        """TEST: txt ERROR TYPE HTTP EXCEPTION"""
        assert txt.HTTP_EXCEPTION is not None

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
