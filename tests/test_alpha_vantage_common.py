"""alpha_vantage_common 的單元測試。"""

import unittest

from tradingagents.dataflows.alpha_vantage_common import (
    AlphaVantageRateLimitError,
    format_datetime_for_api,
)


class TestAlphaVantageRateLimitError(unittest.TestCase):
    def test_is_exception(self):
        self.assertTrue(issubclass(AlphaVantageRateLimitError, Exception))

    def test_can_raise_and_catch(self):
        with self.assertRaises(AlphaVantageRateLimitError):
            raise AlphaVantageRateLimitError("rate limited")

    def test_message(self):
        try:
            raise AlphaVantageRateLimitError("too many requests")
        except AlphaVantageRateLimitError as e:
            self.assertIn("too many requests", str(e))


class TestFormatDatetimeForApi(unittest.TestCase):
    def test_date_string(self):
        result = format_datetime_for_api("2025-01-15")
        self.assertEqual(result, "20250115T0000")

    def test_already_formatted(self):
        result = format_datetime_for_api("20250115T0930")
        self.assertEqual(result, "20250115T0930")

    def test_datetime_with_time(self):
        result = format_datetime_for_api("2025-01-15 09:30")
        self.assertEqual(result, "20250115T0930")


if __name__ == "__main__":
    unittest.main()
