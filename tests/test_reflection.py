"""Reflector 的單元測試。"""

import unittest
from unittest.mock import MagicMock, patch

from tradingagents.graph.reflection import Reflector


def _make_state():
    """建立帶有全部報告的模擬狀態。"""
    return {
        "market_report": "Market is up 2%",
        "sentiment_report": "Social sentiment is positive",
        "news_report": "Fed cut rates",
        "fundamentals_report": "PE ratio 15x, strong earnings",
        "investment_debate_state": {
            "bull_history": "Bull argued for growth",
            "bear_history": "Bear argued for caution",
            "judge_decision": "Buy with caution",
        },
        "trader_investment_plan": "Buy 100 shares",
        "risk_debate_state": {
            "judge_decision": "Accept moderate risk",
        },
    }


class TestReflectorInit(unittest.TestCase):
    def test_creates_with_llm(self):
        mock_llm = MagicMock()
        r = Reflector(mock_llm)
        self.assertIs(r.quick_thinking_llm, mock_llm)
        self.assertIsInstance(r.reflection_system_prompt, str)


class TestExtractCurrentSituation(unittest.TestCase):
    def test_combines_reports(self):
        mock_llm = MagicMock()
        r = Reflector(mock_llm)
        state = _make_state()
        situation = r._extract_current_situation(state)
        self.assertIn("Market is up 2%", situation)
        self.assertIn("Social sentiment is positive", situation)
        self.assertIn("Fed cut rates", situation)
        self.assertIn("PE ratio 15x", situation)


class TestReflectOnComponent(unittest.TestCase):
    def test_invokes_llm(self):
        mock_llm = MagicMock()
        mock_result = MagicMock()
        mock_result.content = "Reflection result"
        mock_llm.invoke.return_value = mock_result

        r = Reflector(mock_llm)
        result = r._reflect_on_component("BULL", "report", "situation", 0.05)
        self.assertEqual(result, "Reflection result")
        mock_llm.invoke.assert_called_once()


class TestReflectMethods(unittest.TestCase):
    """測試各角色反思方法是否正確更新記憶。"""

    def setUp(self):
        self.mock_llm = MagicMock()
        mock_result = MagicMock()
        mock_result.content = "reflection"
        self.mock_llm.invoke.return_value = mock_result
        self.reflector = Reflector(self.mock_llm)
        self.state = _make_state()

    def test_reflect_bull(self):
        mem = MagicMock()
        self.reflector.reflect_bull_researcher(self.state, 0.1, mem)
        mem.add_situations.assert_called_once()

    def test_reflect_bear(self):
        mem = MagicMock()
        self.reflector.reflect_bear_researcher(self.state, -0.05, mem)
        mem.add_situations.assert_called_once()

    def test_reflect_trader(self):
        mem = MagicMock()
        self.reflector.reflect_trader(self.state, 0.03, mem)
        mem.add_situations.assert_called_once()

    def test_reflect_invest_judge(self):
        mem = MagicMock()
        self.reflector.reflect_invest_judge(self.state, 0.02, mem)
        mem.add_situations.assert_called_once()

    def test_reflect_portfolio_manager(self):
        mem = MagicMock()
        self.reflector.reflect_portfolio_manager(self.state, -0.01, mem)
        mem.add_situations.assert_called_once()


if __name__ == "__main__":
    unittest.main()
