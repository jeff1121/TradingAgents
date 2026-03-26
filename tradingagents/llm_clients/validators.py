"""各供應商的模型名稱驗證器。

僅驗證模型名稱——不強制執行限制。
讓 LLM 供應商對未指定的參數使用其自身的預設值。
"""

VALID_MODELS = {
    "openai": [
        # GPT-5 系列
        "gpt-5.4-pro",
        "gpt-5.4",
        "gpt-5.2",
        "gpt-5.1",
        "gpt-5",
        "gpt-5-mini",
        "gpt-5-nano",
        # GPT-4.1 系列
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4.1-nano",
    ],
    "anthropic": [
        # Claude 4.6 系列（最新）
        "claude-opus-4-6",
        "claude-sonnet-4-6",
        # Claude 4.5 系列
        "claude-opus-4-5",
        "claude-sonnet-4-5",
        "claude-haiku-4-5",
    ],
    "google": [
        # Gemini 3.1 系列（預覽版）
        "gemini-3.1-pro-preview",
        "gemini-3.1-flash-lite-preview",
        # Gemini 3 系列（預覽版）
        "gemini-3-flash-preview",
        # Gemini 2.5 系列
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ],
    "xai": [
        # Grok 4.1 系列
        "grok-4-1-fast-reasoning",
        "grok-4-1-fast-non-reasoning",
        # Grok 4 系列
        "grok-4-0709",
        "grok-4-fast-reasoning",
        "grok-4-fast-non-reasoning",
    ],
}


def validate_model(provider: str, model: str) -> bool:
    """檢查模型名稱對於指定供應商是否有效。

    對於 ollama、openrouter——接受任何模型。
    """
    provider_lower = provider.lower()

    if provider_lower in ("ollama", "openrouter"):
        return True

    if provider_lower not in VALID_MODELS:
        return True

    return model in VALID_MODELS[provider_lower]
