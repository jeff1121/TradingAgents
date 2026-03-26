"""LLM 模型驗證器的單元測試。"""

import unittest

from tradingagents.llm_clients.validators import validate_model, VALID_MODELS


class TestValidateModel(unittest.TestCase):
    """validate_model() 測試。"""

    # --- OpenAI ---
    def test_openai_valid_model(self):
        self.assertTrue(validate_model("openai", "gpt-5-mini"))

    def test_openai_invalid_model(self):
        self.assertFalse(validate_model("openai", "nonexistent-model"))

    def test_openai_case_insensitive_provider(self):
        self.assertTrue(validate_model("OpenAI", "gpt-5-mini"))

    # --- Anthropic ---
    def test_anthropic_valid_model(self):
        self.assertTrue(validate_model("anthropic", "claude-opus-4-6"))

    def test_anthropic_invalid_model(self):
        self.assertFalse(validate_model("anthropic", "claude-2"))

    # --- Google ---
    def test_google_valid_model(self):
        self.assertTrue(validate_model("google", "gemini-2.5-pro"))

    def test_google_invalid_model(self):
        self.assertFalse(validate_model("google", "gemini-1.0"))

    # --- xAI ---
    def test_xai_valid_model(self):
        self.assertTrue(validate_model("xai", "grok-4-0709"))

    def test_xai_invalid_model(self):
        self.assertFalse(validate_model("xai", "grok-1"))

    # --- Ollama / OpenRouter 接受任何模型 ---
    def test_ollama_accepts_any(self):
        self.assertTrue(validate_model("ollama", "llama3:70b"))
        self.assertTrue(validate_model("ollama", "totally-custom"))

    def test_openrouter_accepts_any(self):
        self.assertTrue(validate_model("openrouter", "anthropic/claude-3.5"))
        self.assertTrue(validate_model("openrouter", "whatever"))

    # --- 未知供應商預設接受 ---
    def test_unknown_provider_accepts(self):
        self.assertTrue(validate_model("unknown_provider", "any-model"))


class TestValidModelsStructure(unittest.TestCase):
    """VALID_MODELS 字典結構測試。"""

    def test_has_main_providers(self):
        for provider in ("openai", "anthropic", "google", "xai"):
            self.assertIn(provider, VALID_MODELS)

    def test_each_provider_has_models(self):
        for provider, models in VALID_MODELS.items():
            self.assertIsInstance(models, list)
            self.assertGreater(len(models), 0, f"{provider} has no models")

    def test_no_duplicates(self):
        for provider, models in VALID_MODELS.items():
            self.assertEqual(
                len(models), len(set(models)),
                f"{provider} has duplicate models"
            )


if __name__ == "__main__":
    unittest.main()
