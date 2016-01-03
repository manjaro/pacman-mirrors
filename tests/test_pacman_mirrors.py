#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest

from pacman_mirrors import pacman_mirrors


class TestPacmanMirrors(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
