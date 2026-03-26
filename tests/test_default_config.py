"""default_config 的單元測試。"""

import unittest

from tradingagents.default_config import DEFAULT_CONFIG


class TestDefaultConfig(unittest.TestCase):
    """DEFAULT_CONFIG 結構與內容測試。"""

    def test_is_dict(self):
        self.assertIsInstance(DEFAULT_CONFIG, dict)

    def test_llm_settings(self):
        self.assertIn("llm_provider", DEFAULT_CONFIG)
        self.assertIn("deep_think_llm", DEFAULT_CONFIG)
        self.assertIn("quick_think_llm", DEFAULT_CONFIG)

    def test_debate_settings(self):
        self.assertIn("max_debate_rounds", DEFAULT_CONFIG)
        self.assertIn("max_risk_discuss_rounds", DEFAULT_CONFIG)
        self.assertIsInstance(DEFAULT_CONFIG["max_debate_rounds"], int)
        self.assertIsInstance(DEFAULT_CONFIG["max_risk_discuss_rounds"], int)

    def test_data_vendors(self):
        vendors = DEFAULT_CONFIG["data_vendors"]
        self.assertIsInstance(vendors, dict)
        expected_keys = [
            "core_stock_apis",
            "technical_indicators",
            "fundamental_data",
            "news_data",
        ]
        for key in expected_keys:
            self.assertIn(key, vendors)

    def test_tool_vendors_empty_by_default(self):
        self.assertIsInstance(DEFAULT_CONFIG["tool_vendors"], dict)
        self.assertEqual(len(DEFAULT_CONFIG["tool_vendors"]), 0)

    def test_project_dir_exists(self):
        self.assertIn("project_dir", DEFAULT_CONFIG)
        self.assertIsInstance(DEFAULT_CONFIG["project_dir"], str)

    def test_thinking_configs_present(self):
        self.assertIn("google_thinking_level", DEFAULT_CONFIG)
        self.assertIn("openai_reasoning_effort", DEFAULT_CONFIG)
        self.assertIn("anthropic_effort", DEFAULT_CONFIG)

    def test_backend_url(self):
        self.assertIn("backend_url", DEFAULT_CONFIG)


if __name__ == "__main__":
    unittest.main()
