import os
from typing import Any, Optional

from langchain_openai import ChatOpenAI

from .base_client import BaseLLMClient, normalize_content
from .validators import validate_model


class NormalizedChatOpenAI(ChatOpenAI):
    """具有正規化內容輸出的 ChatOpenAI。

    Responses API 會以型別區塊清單（reasoning、text 等）回傳內容。
    此類別將其正規化為字串，確保下游處理的一致性。
    """

    def invoke(self, input, config=None, **kwargs):
        return normalize_content(super().invoke(input, config, **kwargs))

# 從使用者設定轉發至 ChatOpenAI 的 kwargs
_PASSTHROUGH_KWARGS = (
    "timeout", "max_retries", "reasoning_effort",
    "api_key", "callbacks", "http_client", "http_async_client",
)

# 供應商基底 URL 與 API 金鑰環境變數
_PROVIDER_CONFIG = {
    "xai": ("https://api.x.ai/v1", "XAI_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "ollama": ("http://localhost:11434/v1", None),
}


class OpenAIClient(BaseLLMClient):
    """OpenAI、Ollama、OpenRouter 及 xAI 供應商的客戶端。

    原生 OpenAI 模型使用 Responses API（/v1/responses），
    該 API 在所有模型系列（GPT-4.1、GPT-5）中支援搭配 function tools 的 reasoning_effort。
    第三方相容供應商（xAI、OpenRouter、Ollama）使用標準 Chat Completions。
    """

    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        provider: str = "openai",
        **kwargs,
    ):
        super().__init__(model, base_url, **kwargs)
        self.provider = provider.lower()

    def get_llm(self) -> Any:
        """回傳已設定的 ChatOpenAI 實例。"""
        llm_kwargs = {"model": self.model}

        # 供應商專用的基底 URL 與驗證
        if self.provider in _PROVIDER_CONFIG:
            base_url, api_key_env = _PROVIDER_CONFIG[self.provider]
            llm_kwargs["base_url"] = base_url
            if api_key_env:
                api_key = os.environ.get(api_key_env)
                if api_key:
                    llm_kwargs["api_key"] = api_key
            else:
                llm_kwargs["api_key"] = "ollama"
        elif self.base_url:
            llm_kwargs["base_url"] = self.base_url

        # 轉發使用者提供的 kwargs
        for key in _PASSTHROUGH_KWARGS:
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        # 原生 OpenAI：使用 Responses API 以確保所有模型系列的一致行為。
        # 第三方供應商使用 Chat Completions。
        if self.provider == "openai":
            llm_kwargs["use_responses_api"] = True

        return NormalizedChatOpenAI(**llm_kwargs)

    def validate_model(self) -> bool:
        """驗證供應商的模型。"""
        return validate_model(self.provider, self.model)
