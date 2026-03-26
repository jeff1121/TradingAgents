"""normalize_content 及 BaseLLMClient 的單元測試。"""

import unittest
from unittest.mock import MagicMock

from tradingagents.llm_clients.base_client import normalize_content, BaseLLMClient


class TestNormalizeContent(unittest.TestCase):
    """normalize_content() 測試。"""

    def test_string_content_unchanged(self):
        resp = MagicMock()
        resp.content = "Hello world"
        result = normalize_content(resp)
        self.assertEqual(result.content, "Hello world")

    def test_list_with_text_blocks(self):
        resp = MagicMock()
        resp.content = [
            {"type": "reasoning", "text": "thinking..."},
            {"type": "text", "text": "The answer is 42"},
        ]
        result = normalize_content(resp)
        self.assertEqual(result.content, "The answer is 42")

    def test_list_with_multiple_text_blocks(self):
        resp = MagicMock()
        resp.content = [
            {"type": "text", "text": "Part 1"},
            {"type": "text", "text": "Part 2"},
        ]
        result = normalize_content(resp)
        self.assertEqual(result.content, "Part 1\nPart 2")

    def test_list_with_only_reasoning(self):
        resp = MagicMock()
        resp.content = [
            {"type": "reasoning", "text": "thinking..."},
        ]
        result = normalize_content(resp)
        self.assertEqual(result.content, "")

    def test_list_with_plain_strings(self):
        resp = MagicMock()
        resp.content = ["hello", "world"]
        result = normalize_content(resp)
        self.assertEqual(result.content, "hello\nworld")

    def test_empty_list(self):
        resp = MagicMock()
        resp.content = []
        result = normalize_content(resp)
        self.assertEqual(result.content, "")

    def test_mixed_strings_and_dicts(self):
        resp = MagicMock()
        resp.content = [
            "raw string",
            {"type": "text", "text": "dict text"},
        ]
        result = normalize_content(resp)
        self.assertEqual(result.content, "raw string\ndict text")

    def test_returns_same_response_object(self):
        resp = MagicMock()
        resp.content = "test"
        result = normalize_content(resp)
        self.assertIs(result, resp)


class TestBaseLLMClient(unittest.TestCase):
    """BaseLLMClient 抽象類別測試。"""

    def test_cannot_instantiate_directly(self):
        with self.assertRaises(TypeError):
            BaseLLMClient("model-name")

    def test_subclass_works(self):
        class ConcreteClient(BaseLLMClient):
            def get_llm(self):
                return "llm"

            def validate_model(self):
                return True

        client = ConcreteClient("test-model", base_url="http://localhost")
        self.assertEqual(client.model, "test-model")
        self.assertEqual(client.base_url, "http://localhost")
        self.assertEqual(client.get_llm(), "llm")
        self.assertTrue(client.validate_model())

    def test_kwargs_stored(self):
        class ConcreteClient(BaseLLMClient):
            def get_llm(self):
                return None

            def validate_model(self):
                return True

        client = ConcreteClient("m", timeout=30, api_key="k")
        self.assertEqual(client.kwargs["timeout"], 30)
        self.assertEqual(client.kwargs["api_key"], "k")


if __name__ == "__main__":
    unittest.main()
