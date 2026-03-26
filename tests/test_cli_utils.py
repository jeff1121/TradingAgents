"""CLI utils 中 normalize_ticker_symbol 的單元測試。"""

import unittest

from cli.utils import normalize_ticker_symbol, ANALYST_ORDER, TICKER_INPUT_EXAMPLES


class TestNormalizeTickerSymbol(unittest.TestCase):
    def test_basic_uppercase(self):
        self.assertEqual(normalize_ticker_symbol("aapl"), "AAPL")

    def test_strips_whitespace(self):
        self.assertEqual(normalize_ticker_symbol("  spy  "), "SPY")

    def test_preserves_exchange_suffix(self):
        self.assertEqual(normalize_ticker_symbol("cnc.to"), "CNC.TO")

    def test_japanese_exchange(self):
        self.assertEqual(normalize_ticker_symbol("7203.t"), "7203.T")

    def test_hk_exchange(self):
        self.assertEqual(normalize_ticker_symbol("0700.hk"), "0700.HK")

    def test_london_exchange(self):
        self.assertEqual(normalize_ticker_symbol("bp.l"), "BP.L")

    def test_already_uppercase(self):
        self.assertEqual(normalize_ticker_symbol("MSFT"), "MSFT")

    def test_empty_string(self):
        self.assertEqual(normalize_ticker_symbol(""), "")


class TestConstants(unittest.TestCase):
    def test_analyst_order_has_four(self):
        self.assertEqual(len(ANALYST_ORDER), 4)

    def test_analyst_order_tuples(self):
        for name, type_ in ANALYST_ORDER:
            self.assertIsInstance(name, str)

    def test_ticker_examples_exist(self):
        self.assertIn("SPY", TICKER_INPUT_EXAMPLES)
        self.assertIn("CNC.TO", TICKER_INPUT_EXAMPLES)


if __name__ == "__main__":
    unittest.main()
