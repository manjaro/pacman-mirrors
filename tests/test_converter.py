
#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""


import unittest
from unittest.mock import patch

from pacman_mirrors import converter

MOCK_CUSTOM_DATA = "## Country       : Sweden\
## Response time : 0.033\
## Last sync     : 06:06h\
Server = http://ftp.lysator.liu.se/pub/manjaro/unstable/$repo/$arch\
\
## Country       : Denmark\
## Response time : 0.038\
## Last sync     : 06:06h\
Server = http://mirrors.dotsrc.org/manjaro/unstable/$repo/$arch\
\
## Country       : Netherlands\
## Response time : 0.038\
## Last sync     : 06:06h\
Server = http://ftp.snt.utwente.nl/pub/linux/manjaro/unstable/$repo/$arch"

MOCK_CUSTOM_RETURN = "{\
    \"Sweden\": {\
        \"http://ftp.lysator.liu.se/pub/manjaro/\": {\
            \"protocols\": [\"http\"]\
        }\
    },\
    \"Denmark\": {\
        \"http://mirrors.dotsrc.org/manjaro/unstable/$repo/$arch\": {\
            \"protocols\": [\"http\"]\
        }\
    },\
    \"Netherlands\": {\
        \"http://ftp.snt.utwente.nl/pub/linux/manjaro/unstable/$repo/$arch\": {\
            \"protocols\": [\"http\"]\
        }\
    }\
}"

class TestConverter(unittest.TestCase):
    """Converter Test suite"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch.object(converter.Converter, "convert_custom_to_json")
    def test_convert_to_json(self, mock_convert):
        """Convert Custom mirror to json"""
        app = converter.Converter()
        # mock_convert.return_value = MOCK_CUSTOM_RETURN
        print(convert_custom_to_json(MOCK_CUSTOM_DATA))
        assert convert_custom_to_json(MOCK_CUSTOM_DATA) == MOCK_CUSTOM_RETURN


if __name__ == "__main__":
    unittest.main()

