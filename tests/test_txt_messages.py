#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest

from pacman_mirrors.constants import txt


class TestTextMessages(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    def test_txt_msg_api_conf_rebranch(self):
        """TEST: txt API CONF REBRANCH"""
        assert txt.API_CONF_RE_BRANCH is not None

    def test_txt_msg_api_conf_protocols(self):
        """TEST: txt API CONF PROTOCOLS"""
        assert txt.API_CONF_PROTOCOLS is not None

    def test_txt_msg_api_mirrorlist_rebranch(self):
        """TEST: txt API MIRRORLIST REBRANCH"""
        assert txt.API_MIRRORLIST_RE_BRANCH is not None

    def test_txt_msg_available_countries(self):
        """TEST: txt AVAAILABLE COUNTRIES"""
        assert txt.AVAILABLE_COUNTRIES is not None

    def test_txt_msg_download_file(self):
        """TEST: txt DOWNLOAD FILE"""
        assert txt.CANNOT_DOWNLOAD_FILE is not None

    def test_txt_msg_cannot_read_file(self):
        """TEST: txt CANNOT READ FILE"""
        assert txt.CANNOT_READ_FILE is not None

    def test_txt_msg_cannot_write_file(self):
        """TEST: txt CANNOT WRITE FILE"""
        assert txt.CANNOT_WRITE_FILE is not None

    def test_txt_msg_convert_custom_mirror_file(self):
        """TEST: txt CONVERT CUSTOM MIRROR FILE"""
        assert txt.CONVERT_CUSTOM_MIRROR_FILE is not None

    def test_txt_msg_custom_mirror_file(self):
        """TEST: txt CUSTOM MIRROR FILE"""
        assert txt.CUSTOM_MIRROR_FILE is not None

    def test_txt_msg_custom_mirror_file_saved(self):
        """TEST: txt CUSTOM MIRROR FILE SAVED"""
        assert txt.CUSTOM_MIRROR_FILE_SAVED is not None

    def test_txt_msg_custom_mirror_list(self):
        """TEST: txt CUSTOM MIRROR LIST"""
        assert txt.CUSTOM_MIRROR_LIST is not None

    def test_txt_msg_does_not_exist(self):
        """TEST: txt DOES NOT EXIST"""
        assert txt.DOES_NOT_EXIST is not None

    def test_txt_msg_downloading_mirror_file(self):
        """TEST: txt DOWNLOADING MIRROR FILE"""
        assert txt.DOWNLOADING_MIRROR_FILE is not None

    def test_txt_msg_falling_back(self):
        """TEST: txt FALLING BACK"""
        assert txt.FALLING_BACK is not None

    def test_txt_msg_is_missing(self):
        """TEST: txt IS MISSING"""
        assert txt.IS_MISSING is not None

    def test_txt_msg_mirror_file(self):
        """TEST: txt MIRROR FILE"""
        assert txt.MIRROR_FILE is not None

    def test_txt_msg_mirror_list_saved(self):
        """TEST: txt MIRROR LIST SAVED"""
        assert txt.MIRROR_LIST_SAVED is not None

    def test_txt_msg_mirror_ranking_na(self):
        """TEST: txt MIRROR RANKING NA"""
        assert txt.MIRROR_RANKING_NA is not None

    def test_txt_msg_must_be_root(self):
        """TEST: txt MUST BE ROOT"""
        assert txt.MUST_BE_ROOT is not None

    def test_txt_msg_internet_down(self):
        """TEST: txt INTERNET DOWN"""
        assert txt.INTERNET_DOWN is not None

    def test_txt_msg_internet_alternative(self):
        """TEST: txt INTERNET ALTERNATIVE"""
        assert txt.INTERNET_ALTERNATIVE is not None

    def test_txt_msg_no_change(self):
        """TEST: txt NO CHANGE"""
        assert txt.NO_CHANGE is not None

    def test_txt_msg_no_selection(self):
        """TEST: txt NO SELECTION"""
        assert txt.NO_SELECTION is not None

    def test_txt_msg_option(self):
        """TEST: txt OPTION"""
        assert txt.OPTION is not None

    def test_txt_msg_writing_mirror_list(self):
        """TEST: txt WRITING MIRROR LIST"""
        assert txt.WRITING_MIRROR_LIST is not None

    def test_txt_msg_query_mirrors(self):
        """TEST: txt QUERY MIRRORS"""
        assert txt.QUERY_MIRRORS is not None

    def test_txt_msg_randomizing_servers(self):
        """TEST: txt RANDOMIZING SERVERS"""
        assert txt.RANDOMIZING_SERVERS is not None

    def test_txt_msg_reset_custom_config(self):
        """TEST: txt RESET CUSTOM CONFIG"""
        assert txt.RESET_CUSTOM_CONFIG is not None

    def test_txt_msg_takes_time(self):
        """TEST: txt TAKES TIME"""
        assert txt.TAKES_TIME is not None

    def test_txt_msg_unknown_country(self):
        """TEST: txt UNKNOWN COUNTRY"""
        assert txt.UNKNOWN_COUNTRY is not None

    def test_txt_msg_using_all_mirrors(self):
        """TEST: txt USING ALL MIRRORS"""
        assert txt.USING_ALL_MIRRORS is not None

    def test_txt_msg_using_custom_file(self):
        """TEST: txt USING CUSTOM FILE"""
        assert txt.USING_CUSTOM_FILE is not None

    def test_txt_msg_using_default_file(self):
        """TEST: txt USING DEFAULT FILE"""
        assert txt.USING_DEFAULT_FILE is not None

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
