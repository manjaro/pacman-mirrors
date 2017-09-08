#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest

from pacman_mirrors.constants import txt


class TestTextInteractiveMessages(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    # interactive messages
    def test_txt_interactive_title(self):
        """TEST: txt INTERACTIVE TITLE"""
        assert txt.I_TITLE is not None

    def test_txt_interactive_title_random(self):
        """TEST: txt INTERACTIVE TITLE RANDOM"""
        assert txt.I_TITLE_RANDOM is not None

    def test_txt_interactive_list_title(self):
        """TEST: txt INTERACTIVE LIST TITLE"""
        assert txt.I_LIST_TITLE is not None

    def test_txt_interactive_use(self):
        """TEST: txt INTERACTIVE USE"""
        assert txt.I_USE is not None

    def test_txt_interactive_country(self):
        """TEST: txt INTERACTIVE COUNTRY"""
        assert txt.I_COUNTRY is not None

    def test_txt_interactive_response(self):
        """TEST: txt INTERACTIVE RESPONSE"""
        assert txt.I_RESPONSE is not None

    def test_txt_interactive_last_sync(self):
        """TEST: txt INTERACTIVE LAST SYNC"""
        assert txt.I_LAST_SYNC is not None

    def test_txt_interactive_url(self):
        """TEST: txt INTERACTIVE URL"""
        assert txt.I_URL is not None

    def test_txt_interactive_cancel(self):
        """TEST: txt INTERACTIVE CANCEL"""
        assert txt.I_CANCEL is not None

    def test_txt_interactive_confirm(self):
        """TEST: txt INTERACTIVE CONFIRM"""
        assert txt.I_CONFIRM is not None

    def test_txt_interactive_confirm_selection(self):
        """TEST: txt INTERACTIVE CONFIRM SELECTION"""
        assert txt.I_CONFIRM_SELECTION is not None

    def test_txt_interactive_use_these_mirrors(self):
        """TEST: txt INTERACTIVE USE THESE MIRRORS"""
        assert txt.I_USE_THESE_MIRRORS is not None

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
