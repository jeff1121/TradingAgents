"""Propagator 的單元測試。"""

import unittest

from tradingagents.graph.propagation import Propagator


class TestPropagatorInit(unittest.TestCase):
    def test_default_recur_limit(self):
        p = Propagator()
        self.assertEqual(p.max_recur_limit, 100)

    def test_custom_recur_limit(self):
        p = Propagator(max_recur_limit=50)
        self.assertEqual(p.max_recur_limit, 50)


class TestCreateInitialState(unittest.TestCase):
    def setUp(self):
        self.propagator = Propagator()

    def test_returns_dict(self):
        state = self.propagator.create_initial_state("AAPL", "2025-01-01")
        self.assertIsInstance(state, dict)

    def test_company_and_date(self):
        state = self.propagator.create_initial_state("TSLA", "2025-06-15")
        self.assertEqual(state["company_of_interest"], "TSLA")
        self.assertEqual(state["trade_date"], "2025-06-15")

    def test_reports_empty(self):
        state = self.propagator.create_initial_state("SPY", "2025-01-01")
        for key in ("market_report", "fundamentals_report", "sentiment_report", "news_report"):
            self.assertEqual(state[key], "")

    def test_invest_debate_state_initialized(self):
        state = self.propagator.create_initial_state("GOOG", "2025-01-01")
        ids = state["investment_debate_state"]
        self.assertEqual(ids["bull_history"], "")
        self.assertEqual(ids["bear_history"], "")
        self.assertEqual(ids["count"], 0)

    def test_risk_debate_state_initialized(self):
        state = self.propagator.create_initial_state("GOOG", "2025-01-01")
        rds = state["risk_debate_state"]
        self.assertEqual(rds["aggressive_history"], "")
        self.assertEqual(rds["conservative_history"], "")
        self.assertEqual(rds["neutral_history"], "")
        self.assertEqual(rds["count"], 0)

    def test_messages_contain_company(self):
        state = self.propagator.create_initial_state("MSFT", "2025-01-01")
        self.assertEqual(len(state["messages"]), 1)
        self.assertEqual(state["messages"][0], ("human", "MSFT"))

    def test_exchange_suffix_preserved(self):
        state = self.propagator.create_initial_state("7203.T", "2025-03-01")
        self.assertEqual(state["company_of_interest"], "7203.T")

    def test_date_converted_to_str(self):
        from datetime import date
        state = self.propagator.create_initial_state("AAPL", date(2025, 5, 10))
        self.assertEqual(state["trade_date"], "2025-05-10")


class TestGetGraphArgs(unittest.TestCase):
    def setUp(self):
        self.propagator = Propagator(max_recur_limit=42)

    def test_returns_dict(self):
        args = self.propagator.get_graph_args()
        self.assertIsInstance(args, dict)

    def test_stream_mode(self):
        args = self.propagator.get_graph_args()
        self.assertEqual(args["stream_mode"], "values")

    def test_recursion_limit(self):
        args = self.propagator.get_graph_args()
        self.assertEqual(args["config"]["recursion_limit"], 42)

    def test_no_callbacks_by_default(self):
        args = self.propagator.get_graph_args()
        self.assertNotIn("callbacks", args["config"])

    def test_with_callbacks(self):
        cb = [lambda x: x]
        args = self.propagator.get_graph_args(callbacks=cb)
        self.assertEqual(args["config"]["callbacks"], cb)


if __name__ == "__main__":
    unittest.main()
