"""LLM 客戶端工廠的單元測試。"""

import unittest
from unittest.mock import patch, MagicMock

from tradingagents.llm_clients.factory import create_llm_client
from tradingagents.llm_clients.base_client import BaseLLMClient


class TestCreateLLMClient(unittest.TestCase):
    """create_llm_client() 工廠函式測試。"""

    @patch("tradingagents.llm_clients.factory.OpenAIClient")
    def test_openai_provider(self, mock_cls):
        mock_cls.return_value = MagicMock(spec=BaseLLMClient)
        client = create_llm_client("openai", "gpt-5-mini")
        mock_cls.assert_called_once_with("gpt-5-mini", None, provider="openai")

    @patch("tradingagents.llm_clients.factory.OpenAIClient")
    def test_ollama_provider(self, mock_cls):
        mock_cls.return_value = MagicMock(spec=BaseLLMClient)
        create_llm_client("ollama", "llama3", base_url="http://localhost:11434")
        mock_cls.assert_called_once_with(
            "llama3", "http://localhost:11434", provider="ollama"
        )

    @patch("tradingagents.llm_clients.factory.OpenAIClient")
    def test_openrouter_provider(self, mock_cls):
        mock_cls.return_value = MagicMock(spec=BaseLLMClient)
        create_llm_client("openrouter", "meta/llama-3")
        mock_cls.assert_called_once_with("meta/llama-3", None, provider="openrouter")

    @patch("tradingagents.llm_clients.factory.OpenAIClient")
    def test_xai_provider(self, mock_cls):
        mock_cls.return_value = MagicMock(spec=BaseLLMClient)
        create_llm_client("xai", "grok-4-0709")
        mock_cls.assert_called_once_with("grok-4-0709", None, provider="xai")

    @patch("tradingagents.llm_clients.factory.AnthropicClient")
    def test_anthropic_provider(self, mock_cls):
        mock_cls.return_value = MagicMock(spec=BaseLLMClient)
        create_llm_client("anthropic", "claude-opus-4-6")
        mock_cls.assert_called_once_with("claude-opus-4-6", None)

    @patch("tradingagents.llm_clients.factory.GoogleClient")
    def test_google_provider(self, mock_cls):
        mock_cls.return_value = MagicMock(spec=BaseLLMClient)
        create_llm_client("google", "gemini-2.5-pro")
        mock_cls.assert_called_once_with("gemini-2.5-pro", None)

    def test_unsupported_provider_raises(self):
        with self.assertRaises(ValueError) as ctx:
            create_llm_client("unsupported", "model")
        self.assertIn("Unsupported", str(ctx.exception))

    @patch("tradingagents.llm_clients.factory.OpenAIClient")
    def test_case_insensitive(self, mock_cls):
        mock_cls.return_value = MagicMock(spec=BaseLLMClient)
        create_llm_client("OpenAI", "gpt-5-mini")
        mock_cls.assert_called_once()

    @patch("tradingagents.llm_clients.factory.AnthropicClient")
    def test_kwargs_forwarded(self, mock_cls):
        mock_cls.return_value = MagicMock(spec=BaseLLMClient)
        create_llm_client("anthropic", "claude-opus-4-6", timeout=60, api_key="k")
        _, kwargs = mock_cls.call_args
        self.assertEqual(kwargs["timeout"], 60)
        self.assertEqual(kwargs["api_key"], "k")


if __name__ == "__main__":
    unittest.main()
