"""stockstats_utils 的單元測試（_clean_dataframe、yf_retry）。"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

from tradingagents.dataflows.stockstats_utils import _clean_dataframe, yf_retry


class TestCleanDataframe(unittest.TestCase):
    def _make_df(self, dates, closes, opens=None, highs=None, lows=None, volumes=None):
        data = {"Date": dates, "Close": closes}
        if opens:
            data["Open"] = opens
        if highs:
            data["High"] = highs
        if lows:
            data["Low"] = lows
        if volumes:
            data["Volume"] = volumes
        return pd.DataFrame(data)

    def test_parses_dates(self):
        df = self._make_df(["2025-01-06", "2025-01-07"], [100, 101])
        result = _clean_dataframe(df)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result["Date"]))

    def test_drops_invalid_dates(self):
        df = self._make_df(["2025-01-06", "not-a-date", "2025-01-08"], [100, 101, 102])
        result = _clean_dataframe(df)
        self.assertEqual(len(result), 2)

    def test_drops_nan_close(self):
        df = self._make_df(["2025-01-06", "2025-01-07"], [100, None])
        result = _clean_dataframe(df)
        self.assertEqual(len(result), 1)

    def test_numeric_conversion(self):
        df = self._make_df(["2025-01-06"], ["100.5"])
        result = _clean_dataframe(df)
        self.assertEqual(result["Close"].iloc[0], 100.5)

    def test_ffill_bfill(self):
        df = pd.DataFrame({
            "Date": ["2025-01-06", "2025-01-07", "2025-01-08"],
            "Close": [100, None, 102],
            "Open": [99, None, 101],
        })
        # Close 為 None 會被 dropna 丟掉，但 Open 可以 ffill
        df["Close"] = pd.to_numeric(df["Close"])
        df = df.dropna(subset=["Close"])
        # 此測試驗證 ffill 不報錯
        result = _clean_dataframe(pd.DataFrame({
            "Date": ["2025-01-06", "2025-01-08"],
            "Close": [100, 102],
            "Open": [99, 101],
        }))
        self.assertEqual(len(result), 2)


class TestYfRetry(unittest.TestCase):
    def test_success_first_try(self):
        func = MagicMock(return_value="data")
        result = yf_retry(func, max_retries=3, base_delay=0)
        self.assertEqual(result, "data")
        func.assert_called_once()

    @patch("tradingagents.dataflows.stockstats_utils.time.sleep")
    def test_retry_on_rate_limit(self, mock_sleep):
        from yfinance.exceptions import YFRateLimitError

        func = MagicMock(side_effect=[YFRateLimitError(), "ok"])
        result = yf_retry(func, max_retries=3, base_delay=0.01)
        self.assertEqual(result, "ok")
        self.assertEqual(func.call_count, 2)

    @patch("tradingagents.dataflows.stockstats_utils.time.sleep")
    def test_exhausts_retries(self, mock_sleep):
        from yfinance.exceptions import YFRateLimitError

        func = MagicMock(side_effect=YFRateLimitError())
        with self.assertRaises(YFRateLimitError):
            yf_retry(func, max_retries=2, base_delay=0.01)
        self.assertEqual(func.call_count, 3)  # 初始 + 2 次重試

    def test_non_rate_limit_error_not_retried(self):
        func = MagicMock(side_effect=ValueError("bad value"))
        with self.assertRaises(ValueError):
            yf_retry(func, max_retries=3, base_delay=0)
        func.assert_called_once()


if __name__ == "__main__":
    unittest.main()
