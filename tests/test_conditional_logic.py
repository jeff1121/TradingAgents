"""ConditionalLogic 的單元測試。"""

import unittest
from unittest.mock import MagicMock

from tradingagents.graph.conditional_logic import ConditionalLogic


class TestConditionalLogicInit(unittest.TestCase):
    def test_default_rounds(self):
        cl = ConditionalLogic()
        self.assertEqual(cl.max_debate_rounds, 1)
        self.assertEqual(cl.max_risk_discuss_rounds, 1)

    def test_custom_rounds(self):
        cl = ConditionalLogic(max_debate_rounds=5, max_risk_discuss_rounds=3)
        self.assertEqual(cl.max_debate_rounds, 5)
        self.assertEqual(cl.max_risk_discuss_rounds, 3)


def _make_state_with_tool_calls(has_tool_calls: bool):
    """建立帶有（或不帶有）tool_calls 的模擬狀態。"""
    msg = MagicMock()
    msg.tool_calls = [{"name": "get_stock_data"}] if has_tool_calls else []
    return {"messages": [msg]}


class TestShouldContinueAnalysts(unittest.TestCase):
    """分析師工具迴圈路由測試。"""

    def setUp(self):
        self.cl = ConditionalLogic()

    def test_market_continues_to_tools(self):
        state = _make_state_with_tool_calls(True)
        self.assertEqual(self.cl.should_continue_market(state), "tools_market")

    def test_market_stops(self):
        state = _make_state_with_tool_calls(False)
        self.assertEqual(self.cl.should_continue_market(state), "Msg Clear Market")

    def test_social_continues_to_tools(self):
        state = _make_state_with_tool_calls(True)
        self.assertEqual(self.cl.should_continue_social(state), "tools_social")

    def test_social_stops(self):
        state = _make_state_with_tool_calls(False)
        self.assertEqual(self.cl.should_continue_social(state), "Msg Clear Social")

    def test_news_continues_to_tools(self):
        state = _make_state_with_tool_calls(True)
        self.assertEqual(self.cl.should_continue_news(state), "tools_news")

    def test_news_stops(self):
        state = _make_state_with_tool_calls(False)
        self.assertEqual(self.cl.should_continue_news(state), "Msg Clear News")

    def test_fundamentals_continues_to_tools(self):
        state = _make_state_with_tool_calls(True)
        self.assertEqual(self.cl.should_continue_fundamentals(state), "tools_fundamentals")

    def test_fundamentals_stops(self):
        state = _make_state_with_tool_calls(False)
        self.assertEqual(self.cl.should_continue_fundamentals(state), "Msg Clear Fundamentals")


class TestShouldContinueDebate(unittest.TestCase):
    """研究員辯論路由測試。"""

    def setUp(self):
        self.cl = ConditionalLogic(max_debate_rounds=2)

    def test_routes_to_bear_after_bull(self):
        state = {
            "investment_debate_state": {
                "count": 1,
                "current_response": "Bull: I think we should buy",
            }
        }
        self.assertEqual(self.cl.should_continue_debate(state), "Bear Researcher")

    def test_routes_to_bull_after_bear(self):
        state = {
            "investment_debate_state": {
                "count": 1,
                "current_response": "Bear: I think we should sell",
            }
        }
        self.assertEqual(self.cl.should_continue_debate(state), "Bull Researcher")

    def test_ends_at_limit(self):
        state = {
            "investment_debate_state": {
                "count": 4,  # 2 * max_debate_rounds(2) = 4
                "current_response": "Bull: final statement",
            }
        }
        self.assertEqual(self.cl.should_continue_debate(state), "Research Manager")

    def test_single_round(self):
        cl = ConditionalLogic(max_debate_rounds=1)
        state = {
            "investment_debate_state": {
                "count": 2,
                "current_response": "Bull: done",
            }
        }
        self.assertEqual(cl.should_continue_debate(state), "Research Manager")


class TestShouldContinueRiskAnalysis(unittest.TestCase):
    """風險分析路由測試。"""

    def setUp(self):
        self.cl = ConditionalLogic(max_risk_discuss_rounds=2)

    def test_aggressive_to_conservative(self):
        state = {
            "risk_debate_state": {
                "count": 1,
                "latest_speaker": "Aggressive analyst",
            }
        }
        self.assertEqual(
            self.cl.should_continue_risk_analysis(state), "Conservative Analyst"
        )

    def test_conservative_to_neutral(self):
        state = {
            "risk_debate_state": {
                "count": 1,
                "latest_speaker": "Conservative analyst",
            }
        }
        self.assertEqual(
            self.cl.should_continue_risk_analysis(state), "Neutral Analyst"
        )

    def test_neutral_to_aggressive(self):
        state = {
            "risk_debate_state": {
                "count": 1,
                "latest_speaker": "Neutral analyst",
            }
        }
        self.assertEqual(
            self.cl.should_continue_risk_analysis(state), "Aggressive Analyst"
        )

    def test_ends_at_limit(self):
        state = {
            "risk_debate_state": {
                "count": 6,  # 3 * max_risk_discuss_rounds(2)
                "latest_speaker": "Aggressive analyst",
            }
        }
        self.assertEqual(
            self.cl.should_continue_risk_analysis(state), "Portfolio Manager"
        )

    def test_single_round_ends(self):
        cl = ConditionalLogic(max_risk_discuss_rounds=1)
        state = {
            "risk_debate_state": {
                "count": 3,
                "latest_speaker": "Neutral",
            }
        }
        self.assertEqual(cl.should_continue_risk_analysis(state), "Portfolio Manager")


if __name__ == "__main__":
    unittest.main()
