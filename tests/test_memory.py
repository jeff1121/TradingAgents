"""FinancialSituationMemory 的單元測試。"""

import unittest

from tradingagents.agents.utils.memory import FinancialSituationMemory


class TestFinancialSituationMemoryInit(unittest.TestCase):
    """初始化相關測試。"""

    def test_init_with_name(self):
        mem = FinancialSituationMemory("test")
        self.assertEqual(mem.name, "test")
        self.assertEqual(mem.documents, [])
        self.assertEqual(mem.recommendations, [])
        self.assertIsNone(mem.bm25)

    def test_init_with_config(self):
        cfg = {"some_key": "val"}
        mem = FinancialSituationMemory("x", config=cfg)
        self.assertEqual(mem.name, "x")

    def test_init_without_config(self):
        mem = FinancialSituationMemory("y")
        self.assertIsNone(mem.bm25)


class TestTokenize(unittest.TestCase):
    """分詞邏輯測試。"""

    def setUp(self):
        self.mem = FinancialSituationMemory("tok")

    def test_basic_tokenize(self):
        tokens = self.mem._tokenize("Hello World")
        self.assertEqual(tokens, ["hello", "world"])

    def test_empty_string(self):
        self.assertEqual(self.mem._tokenize(""), [])

    def test_punctuation_stripped(self):
        tokens = self.mem._tokenize("price: $100.50, volume=200!")
        self.assertIn("price", tokens)
        self.assertIn("100", tokens)
        self.assertIn("volume", tokens)
        self.assertIn("200", tokens)

    def test_case_insensitive(self):
        tokens = self.mem._tokenize("BUY SELL Hold")
        self.assertEqual(tokens, ["buy", "sell", "hold"])


class TestAddSituations(unittest.TestCase):
    """新增情境測試。"""

    def setUp(self):
        self.mem = FinancialSituationMemory("add")

    def test_add_single(self):
        self.mem.add_situations([("market crash", "sell everything")])
        self.assertEqual(len(self.mem.documents), 1)
        self.assertEqual(len(self.mem.recommendations), 1)
        self.assertIsNotNone(self.mem.bm25)

    def test_add_multiple(self):
        pairs = [
            ("bull market momentum", "buy growth stocks"),
            ("bear market decline", "shift to bonds"),
            ("sideways trading", "hold positions"),
        ]
        self.mem.add_situations(pairs)
        self.assertEqual(len(self.mem.documents), 3)
        self.assertEqual(len(self.mem.recommendations), 3)

    def test_add_incremental(self):
        self.mem.add_situations([("first", "rec1")])
        self.mem.add_situations([("second", "rec2")])
        self.assertEqual(len(self.mem.documents), 2)
        self.assertIsNotNone(self.mem.bm25)

    def test_empty_list(self):
        self.mem.add_situations([])
        self.assertEqual(len(self.mem.documents), 0)
        self.assertIsNone(self.mem.bm25)


class TestGetMemories(unittest.TestCase):
    """記憶檢索測試。"""

    def setUp(self):
        self.mem = FinancialSituationMemory("retrieve")
        self.mem.add_situations([
            ("stock price rising rapidly with high volume", "consider taking profits"),
            ("earnings report missed expectations significantly", "reduce position size"),
            ("interest rates cut by federal reserve", "buy growth stocks"),
            ("company announced stock buyback program", "positive signal hold"),
        ])

    def test_returns_list(self):
        results = self.mem.get_memories("stock price going up")
        self.assertIsInstance(results, list)

    def test_result_structure(self):
        results = self.mem.get_memories("price rising", n_matches=1)
        self.assertEqual(len(results), 1)
        r = results[0]
        self.assertIn("matched_situation", r)
        self.assertIn("recommendation", r)
        self.assertIn("similarity_score", r)

    def test_best_match_relevance(self):
        results = self.mem.get_memories("stock price rising with big volume", n_matches=1)
        self.assertIn("profits", results[0]["recommendation"])

    def test_n_matches(self):
        results = self.mem.get_memories("market", n_matches=3)
        self.assertEqual(len(results), 3)

    def test_n_matches_exceeds_docs(self):
        results = self.mem.get_memories("market", n_matches=100)
        self.assertEqual(len(results), 4)

    def test_empty_memory(self):
        empty = FinancialSituationMemory("empty")
        results = empty.get_memories("anything")
        self.assertEqual(results, [])

    def test_similarity_score_normalized(self):
        results = self.mem.get_memories("stock price", n_matches=1)
        score = results[0]["similarity_score"]
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1.0)


class TestClear(unittest.TestCase):
    """清除記憶測試。"""

    def test_clear_removes_all(self):
        mem = FinancialSituationMemory("clr")
        mem.add_situations([("a", "b"), ("c", "d")])
        mem.clear()
        self.assertEqual(mem.documents, [])
        self.assertEqual(mem.recommendations, [])
        self.assertIsNone(mem.bm25)

    def test_clear_then_query(self):
        mem = FinancialSituationMemory("clr2")
        mem.add_situations([("situation", "advice")])
        mem.clear()
        results = mem.get_memories("situation")
        self.assertEqual(results, [])

    def test_clear_then_add(self):
        mem = FinancialSituationMemory("clr3")
        mem.add_situations([("old", "old_rec")])
        mem.clear()
        mem.add_situations([("new", "new_rec")])
        self.assertEqual(len(mem.documents), 1)
        self.assertEqual(mem.documents[0], "new")


if __name__ == "__main__":
    unittest.main()
