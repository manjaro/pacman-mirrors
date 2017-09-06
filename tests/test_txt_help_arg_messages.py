#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors import txt


class TestTextHelpArgMessages(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    def test_txt_help_arg_api_get_branch(self):
        """TEST: txt HELP ARG API GET BRANCH"""
        assert txt.HLP_ARG_API_GET_BRANCH is not None

    def test_txt_help_arg_api_prefix(self):
        """TEST: txt HELP ARG API PREFIX"""
        assert txt.HLP_ARG_API_PREFIX is not None

    def test_txt_help_arg_api_protocols(self):
        """TEST: txt HELP ARG API PROTOCOLS"""
        assert txt.HLP_ARG_API_PROTOCOLS is not None

    def test_txt_help_arg_api_re_branch(self):
        """TEST: txt HELP ARG API REBRANCH"""
        assert txt.HLP_ARG_API_RE_BRANCH is not None

    def test_txt_help_arg_api_set_branch(self):
        """TEST: txt HELP ARG API SET BRANCH"""
        assert txt.HLP_ARG_API_SET_BRANCH is not None

    def test_txt_help_arg_api_url(self):
        """TEST: txt HELP ARG API URL"""
        assert txt.HLP_ARG_API_URL is not None

    def test_txt_help_arg_branch(self):
        """TEST: txt HELP ARG BRANCH"""
        assert txt.HLP_ARG_BRANCH is not None

    def test_txt_help_arg_country(self):
        """TEST: txt HELP ARG COUNTRY"""
        assert txt.HLP_ARG_COUNTRY is not None

    def test_txt_help_arg_default(self):
        """TEST: txt HELP ARG DEFAULT"""
        assert txt.HLP_ARG_DEFAULT is not None

    def test_txt_help_arg_fasttrack(self):
        """TEST: txt HELP ARG FASTTRACK"""
        assert txt.HLP_ARG_FASTTRACK is not None

    def test_txt_help_arg_generate(self):
        """TEST: txt HELP ARG GENERATE"""
        assert txt.HLP_ARG_GENERATE is not None

    def test_txt_help_arg_geoip(self):
        """TEST: txt HELP ARG GEOIP"""
        assert txt.HLP_ARG_GEOIP is not None

    def test_txt_help_arg_list(self):
        """TEST: txt HELP ARG LIST"""
        assert txt.HLP_ARG_LIST is not None

    def test_txt_help_arg_method(self):
        """TEST: txt HELP ARG METHOD"""
        assert txt.HLP_ARG_METHOD is not None

    def test_txt_help_arg_mirrorlist(self):
        """TEST: txt HELP ARG MIRRORLIST"""
        assert txt.HLP_ARG_NO_MIRRORLIST is not None

    def test_txt_help_arg_quiet(self):
        """TEST: txt HELP ARG QUIET"""
        assert txt.HLP_ARG_QUIET is not None

    def test_txt_help_arg_sync(self):
        """TEST: txt HELP ARG SYNC"""
        assert txt.HLP_ARG_SYNC is not None

    def test_txt_help_arg_timeout(self):
        """TEST: txt HELP ARG TIMEOUT"""
        assert txt.HLP_ARG_TIMEOUT is not None

    def test_txt_help_arg_version(self):
        """TEST: txt HELP ARG VERSION"""
        assert txt.HLP_ARG_VERSION is not None

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
