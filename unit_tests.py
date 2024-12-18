import unittest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from modules.file_manager import KyivTimezoneFormatter
from modules.keyboards import modify_language

from datetime import datetime, timezone
from unittest.mock import Mock
import pytz  # For timezone handling

# Define the Kyiv timezone
KYIV_TZ = pytz.timezone('Europe/Kyiv')

# Create an instance of class to call the funcion later
formatter = KyivTimezoneFormatter()

class TestFormatTime(unittest.TestCase):
    def setUp(self):
        # Common setup: Create a mock record object
        self.mock_record = Mock()
        # Fixed UTC timestamp: 2024-06-17 12:00:00 UTC
        self.mock_record.created = 1718625600.0  # Unix timestamp

    def test_format_time_default(self):
        """Test formatTime with the default date format."""
        expected_time = datetime.fromtimestamp(1718625600.0, tz=timezone.utc).astimezone(KYIV_TZ)
        result = formatter.formatTime(self.mock_record)
        expected_str = expected_time.strftime("%Y-%m-%d %H:%M:%S %z")
        self.assertEqual(result, expected_str)

    def test_format_time_custom_datefmt(self):
        """Test formatTime with a custom date format."""
        custom_datefmt = "%d-%m-%Y %H:%M"
        expected_time = datetime.fromtimestamp(1718625600.0, tz=timezone.utc).astimezone(KYIV_TZ)
        result = formatter.formatTime(self.mock_record, datefmt=custom_datefmt)
        expected_str = expected_time.strftime(custom_datefmt)
        self.assertEqual(result, expected_str)

    def test_format_time_with_different_timestamps(self):
        """Test formatTime with different timestamps."""
        timestamps = [
            1718625600.0,  # 2024-06-17 12:00:00 UTC
            1718701200.0,  # 2024-06-18 08:00:00 UTC
            1718787600.0,  # 2024-06-19 08:00:00 UTC
        ]
        for ts in timestamps:
            with self.subTest(timestamp=ts):
                self.mock_record.created = ts
                expected_time = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(KYIV_TZ)
                result = formatter.formatTime(self.mock_record)
                expected_str = expected_time.strftime("%Y-%m-%d %H:%M:%S %z")
                self.assertEqual(result, expected_str)

class TestLinkFunctions(unittest.TestCase):

    def test_modify_language(self):
        """
        Test modify_language to ensure it adds or replaces the language parameter correctly.
        """
        # Test cases with inputs and expected outputs
        test_cases = [
            ("https://x.com/user/status/123", "ua", "https://x.com/user/status/123/ua"),
            ("https://x.com/user/status/123/sk", "ua", "https://x.com/user/status/123/ua"),
            ("https://x.com/user/status/123/en", "sk", "https://x.com/user/status/123/sk"),
            ("https://x.com/user/status/123", "sk", "https://x.com/user/status/123/sk"),
        ]

        for link, lang, expected in test_cases:
            with self.subTest(link=link, lang=lang):
                result = modify_language(link, lang)
                self.assertEqual(result, expected)

    def test_modify_language_edge_cases(self):
        """
        Test modify_language for edge cases like empty links or invalid inputs.
        """
        # Test empty link
        self.assertEqual(modify_language("", "ua"), "")

        # Test invalid language
        self.assertEqual(modify_language("https://x.com/user/status/123", ""), "https://x.com/user/status/123")

        # Test link with existing unknown modifiers
        self.assertEqual(modify_language("https://x.com/user/status/123/xx", "ua"), "https://x.com/user/status/123/ua")

if __name__ == "__main__":
    unittest.main()