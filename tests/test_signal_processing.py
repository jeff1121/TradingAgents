"""SignalProcessor 的單元測試。"""

import unittest
from unittest.mock import MagicMock

from tradingagents.graph.signal_processing import SignalProcessor


class TestSignalProcessor(unittest.TestCase):
    def _make_processor(self, llm_response: str) -> SignalProcessor:
        mock_llm = MagicMock()
        mock_result = MagicMock()
        mock_result.content = llm_response
        mock_llm.invoke.return_value = mock_result
        return SignalProcessor(mock_llm)

    def test_extracts_buy(self):
        sp = self._make_processor("BUY")
        result = sp.process_signal("very bullish analysis text")
        self.assertEqual(result, "BUY")

    def test_extracts_sell(self):
        sp = self._make_processor("SELL")
        result = sp.process_signal("bearish outlook")
        self.assertEqual(result, "SELL")

    def test_extracts_hold(self):
        sp = self._make_processor("HOLD")
        result = sp.process_signal("neutral")
        self.assertEqual(result, "HOLD")

    def test_extracts_overweight(self):
        sp = self._make_processor("OVERWEIGHT")
        result = sp.process_signal("slightly bullish")
        self.assertEqual(result, "OVERWEIGHT")

    def test_extracts_underweight(self):
        sp = self._make_processor("UNDERWEIGHT")
        result = sp.process_signal("slightly bearish")
        self.assertEqual(result, "UNDERWEIGHT")

    def test_llm_invoked_with_signal(self):
        mock_llm = MagicMock()
        mock_result = MagicMock()
        mock_result.content = "BUY"
        mock_llm.invoke.return_value = mock_result

        sp = SignalProcessor(mock_llm)
        sp.process_signal("my signal text")

        mock_llm.invoke.assert_called_once()
        call_args = mock_llm.invoke.call_args[0][0]
        # 最後一個 message 應包含訊號文字
        self.assertEqual(call_args[-1][1], "my signal text")


if __name__ == "__main__":
    unittest.main()
