"""dataflows 介面（供應商路由）的單元測試。"""

import unittest
from unittest.mock import patch, MagicMock

from tradingagents.dataflows.interface import (
    get_category_for_method,
    get_vendor,
    route_to_vendor,
    TOOLS_CATEGORIES,
    VENDOR_METHODS,
    VENDOR_LIST,
)
from tradingagents.dataflows.alpha_vantage_common import AlphaVantageRateLimitError


class TestGetCategoryForMethod(unittest.TestCase):
    def test_core_stock(self):
        self.assertEqual(get_category_for_method("get_stock_data"), "core_stock_apis")

    def test_technical(self):
        self.assertEqual(get_category_for_method("get_indicators"), "technical_indicators")

    def test_fundamental(self):
        self.assertEqual(get_category_for_method("get_fundamentals"), "fundamental_data")
        self.assertEqual(get_category_for_method("get_balance_sheet"), "fundamental_data")
        self.assertEqual(get_category_for_method("get_cashflow"), "fundamental_data")
        self.assertEqual(get_category_for_method("get_income_statement"), "fundamental_data")

    def test_news(self):
        self.assertEqual(get_category_for_method("get_news"), "news_data")
        self.assertEqual(get_category_for_method("get_global_news"), "news_data")
        self.assertEqual(get_category_for_method("get_insider_transactions"), "news_data")

    def test_unknown_method_raises(self):
        with self.assertRaises(ValueError):
            get_category_for_method("nonexistent_method")


class TestGetVendor(unittest.TestCase):
    @patch("tradingagents.dataflows.interface.get_config")
    def test_category_level_vendor(self, mock_cfg):
        mock_cfg.return_value = {
            "data_vendors": {"core_stock_apis": "yfinance"},
            "tool_vendors": {},
        }
        self.assertEqual(get_vendor("core_stock_apis"), "yfinance")

    @patch("tradingagents.dataflows.interface.get_config")
    def test_tool_level_override(self, mock_cfg):
        mock_cfg.return_value = {
            "data_vendors": {"core_stock_apis": "yfinance"},
            "tool_vendors": {"get_stock_data": "alpha_vantage"},
        }
        self.assertEqual(
            get_vendor("core_stock_apis", method="get_stock_data"),
            "alpha_vantage",
        )

    @patch("tradingagents.dataflows.interface.get_config")
    def test_no_tool_override_falls_back(self, mock_cfg):
        mock_cfg.return_value = {
            "data_vendors": {"core_stock_apis": "yfinance"},
            "tool_vendors": {},
        }
        self.assertEqual(get_vendor("core_stock_apis", method="get_stock_data"), "yfinance")


class TestRouteToVendor(unittest.TestCase):
    @patch("tradingagents.dataflows.interface.get_config")
    def test_routes_to_primary(self, mock_cfg):
        mock_cfg.return_value = {
            "data_vendors": {"core_stock_apis": "yfinance"},
            "tool_vendors": {},
        }
        mock_impl = MagicMock(return_value="yf_result")
        with patch.dict(
            "tradingagents.dataflows.interface.VENDOR_METHODS",
            {"get_stock_data": {"yfinance": mock_impl, "alpha_vantage": MagicMock()}},
        ):
            result = route_to_vendor("get_stock_data", "AAPL", "2025-01-01", "2025-01-31")
        self.assertEqual(result, "yf_result")
        mock_impl.assert_called_once_with("AAPL", "2025-01-01", "2025-01-31")

    @patch("tradingagents.dataflows.interface.get_config")
    def test_fallback_on_rate_limit(self, mock_cfg):
        mock_cfg.return_value = {
            "data_vendors": {"core_stock_apis": "alpha_vantage"},
            "tool_vendors": {},
        }
        av_impl = MagicMock(side_effect=AlphaVantageRateLimitError("rate limited"))
        yf_impl = MagicMock(return_value="fallback_result")
        with patch.dict(
            "tradingagents.dataflows.interface.VENDOR_METHODS",
            {"get_stock_data": {"alpha_vantage": av_impl, "yfinance": yf_impl}},
        ):
            result = route_to_vendor("get_stock_data", "AAPL", "2025-01-01", "2025-01-31")
        self.assertEqual(result, "fallback_result")

    @patch("tradingagents.dataflows.interface.get_config")
    def test_all_vendors_fail_raises(self, mock_cfg):
        mock_cfg.return_value = {
            "data_vendors": {"core_stock_apis": "alpha_vantage"},
            "tool_vendors": {},
        }
        av_impl = MagicMock(side_effect=AlphaVantageRateLimitError("rate limited"))
        yf_impl = MagicMock(side_effect=AlphaVantageRateLimitError("rate limited"))
        with patch.dict(
            "tradingagents.dataflows.interface.VENDOR_METHODS",
            {"get_stock_data": {"alpha_vantage": av_impl, "yfinance": yf_impl}},
        ):
            with self.assertRaises(RuntimeError):
                route_to_vendor("get_stock_data", "AAPL", "2025-01-01", "2025-01-31")

    def test_unsupported_method_for_category_raises(self):
        with self.assertRaises(ValueError):
            route_to_vendor("totally_fake_method")


class TestToolsCategoriesStructure(unittest.TestCase):
    def test_all_methods_in_vendor_methods(self):
        for cat, info in TOOLS_CATEGORIES.items():
            for tool in info["tools"]:
                self.assertIn(tool, VENDOR_METHODS, f"{tool} not in VENDOR_METHODS")

    def test_vendor_list(self):
        self.assertIn("yfinance", VENDOR_LIST)
        self.assertIn("alpha_vantage", VENDOR_LIST)


if __name__ == "__main__":
    unittest.main()
