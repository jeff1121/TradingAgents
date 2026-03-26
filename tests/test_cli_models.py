"""CLI models 的單元測試。"""

import unittest

from cli.models import AnalystType


class TestAnalystType(unittest.TestCase):
    def test_values(self):
        self.assertEqual(AnalystType.MARKET, "market")
        self.assertEqual(AnalystType.SOCIAL, "social")
        self.assertEqual(AnalystType.NEWS, "news")
        self.assertEqual(AnalystType.FUNDAMENTALS, "fundamentals")

    def test_is_str_enum(self):
        self.assertIsInstance(AnalystType.MARKET, str)

    def test_all_members(self):
        members = list(AnalystType)
        self.assertEqual(len(members), 4)

    def test_from_value(self):
        self.assertEqual(AnalystType("market"), AnalystType.MARKET)
        self.assertEqual(AnalystType("fundamentals"), AnalystType.FUNDAMENTALS)

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            AnalystType("invalid")


if __name__ == "__main__":
    unittest.main()
