"""agent_utils 的單元測試。"""

import unittest

from tradingagents.agents.utils.agent_utils import (
    build_instrument_context,
    create_msg_delete,
)


class TestBuildInstrumentContext(unittest.TestCase):
    def test_contains_ticker(self):
        ctx = build_instrument_context("AAPL")
        self.assertIn("AAPL", ctx)

    def test_exchange_suffix_mentioned(self):
        ctx = build_instrument_context("CNC.TO")
        self.assertIn("CNC.TO", ctx)
        self.assertIn("exchange suffix", ctx)

    def test_japanese_ticker(self):
        ctx = build_instrument_context("7203.T")
        self.assertIn("7203.T", ctx)

    def test_hk_ticker(self):
        ctx = build_instrument_context("0700.HK")
        self.assertIn("0700.HK", ctx)

    def test_returns_string(self):
        self.assertIsInstance(build_instrument_context("SPY"), str)


class TestCreateMsgDelete(unittest.TestCase):
    def test_returns_callable(self):
        fn = create_msg_delete()
        self.assertTrue(callable(fn))

    def test_clears_messages_and_adds_placeholder(self):
        from unittest.mock import MagicMock

        msg1 = MagicMock()
        msg1.id = "msg-1"
        msg2 = MagicMock()
        msg2.id = "msg-2"
        state = {"messages": [msg1, msg2]}

        fn = create_msg_delete()
        result = fn(state)

        self.assertIn("messages", result)
        messages = result["messages"]
        # len(original) 個 RemoveMessage + 1 個 placeholder
        self.assertEqual(len(messages), 3)
        # 最後一個是 HumanMessage placeholder
        self.assertEqual(messages[-1].content, "Continue")


if __name__ == "__main__":
    unittest.main()
