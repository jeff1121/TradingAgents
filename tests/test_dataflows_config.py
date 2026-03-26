"""dataflows 設定管理的單元測試。"""

import unittest
from unittest.mock import patch

from tradingagents.dataflows import config as df_config


class TestDataflowsConfig(unittest.TestCase):
    """get_config / set_config / initialize_config 測試。"""

    def setUp(self):
        # 每個測試前重設全域 _config
        df_config._config = None

    def tearDown(self):
        # 恢復預設狀態
        df_config._config = None
        df_config.initialize_config()

    def test_initialize_creates_config(self):
        self.assertIsNone(df_config._config)
        df_config.initialize_config()
        self.assertIsNotNone(df_config._config)

    def test_initialize_idempotent(self):
        df_config.initialize_config()
        first = df_config._config
        df_config.initialize_config()
        # 第二次呼叫不應覆蓋
        self.assertIs(df_config._config, first)

    def test_get_config_returns_copy(self):
        df_config.initialize_config()
        c1 = df_config.get_config()
        c2 = df_config.get_config()
        self.assertEqual(c1, c2)
        # 修改副本不影響原始
        c1["extra"] = True
        c3 = df_config.get_config()
        self.assertNotIn("extra", c3)

    def test_get_config_auto_initializes(self):
        self.assertIsNone(df_config._config)
        cfg = df_config.get_config()
        self.assertIn("llm_provider", cfg)

    def test_set_config_merges(self):
        df_config.initialize_config()
        df_config.set_config({"llm_provider": "anthropic"})
        cfg = df_config.get_config()
        self.assertEqual(cfg["llm_provider"], "anthropic")
        # 其他欄位仍在
        self.assertIn("data_vendors", cfg)

    def test_set_config_auto_initializes(self):
        df_config._config = None
        df_config.set_config({"custom_key": "value"})
        cfg = df_config.get_config()
        self.assertEqual(cfg["custom_key"], "value")
        self.assertIn("llm_provider", cfg)

    def test_default_config_has_required_keys(self):
        df_config.initialize_config()
        cfg = df_config.get_config()
        required = [
            "llm_provider", "deep_think_llm", "quick_think_llm",
            "max_debate_rounds", "max_risk_discuss_rounds",
            "data_vendors", "tool_vendors",
        ]
        for key in required:
            self.assertIn(key, cfg, f"Missing required key: {key}")


if __name__ == "__main__":
    unittest.main()
