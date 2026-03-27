from typing import Optional

from .base_client import BaseLLMClient
from .openai_client import OpenAIClient
from .anthropic_client import AnthropicClient
from .google_client import GoogleClient


def create_llm_client(
    provider: str,
    model: str,
    base_url: Optional[str] = None,
    **kwargs,
) -> BaseLLMClient:
    """為指定的供應商建立 LLM 客戶端。

    Args:
        provider: LLM 供應商（openai、anthropic、google、xai、ollama、openrouter）
        model: 模型名稱／識別碼
        base_url: 選用的 API 端點基底 URL
        **kwargs: 其他供應商專用參數
            - http_client: 自訂 httpx.Client，用於 SSL proxy 或憑證自訂
            - http_async_client: 自訂 httpx.AsyncClient，用於非同步操作
            - timeout: 請求逾時秒數
            - max_retries: 最大重試次數
            - api_key: 供應商的 API 金鑰
            - callbacks: LangChain 回呼函式

    Returns:
        已設定的 BaseLLMClient 實例

    Raises:
        ValueError: 當供應商不被支援時
    """
    provider_lower = provider.lower()

    if provider_lower in ("openai", "ollama", "openrouter", "github"):
        return OpenAIClient(model, base_url, provider=provider_lower, **kwargs)

    if provider_lower == "xai":
        return OpenAIClient(model, base_url, provider="xai", **kwargs)

    if provider_lower == "anthropic":
        return AnthropicClient(model, base_url, **kwargs)

    if provider_lower == "google":
        return GoogleClient(model, base_url, **kwargs)

    raise ValueError(f"Unsupported LLM provider: {provider}")
