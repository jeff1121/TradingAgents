from typing import Any, Optional

from langchain_anthropic import ChatAnthropic

from .base_client import BaseLLMClient, normalize_content
from .validators import validate_model

_PASSTHROUGH_KWARGS = (
    "timeout", "max_retries", "api_key", "max_tokens",
    "callbacks", "http_client", "http_async_client", "effort",
)


class NormalizedChatAnthropic(ChatAnthropic):
    """具有正規化內容輸出的 ChatAnthropic。

    啟用延伸思考或工具使用的 Claude 模型會以型別區塊清單回傳內容。
    此類別將其正規化為字串，確保下游處理的一致性。
    """

    def invoke(self, input, config=None, **kwargs):
        return normalize_content(super().invoke(input, config, **kwargs))


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude 模型的客戶端。"""

    def __init__(self, model: str, base_url: Optional[str] = None, **kwargs):
        super().__init__(model, base_url, **kwargs)

    def get_llm(self) -> Any:
        """回傳已設定的 ChatAnthropic 實例。"""
        llm_kwargs = {"model": self.model}

        for key in _PASSTHROUGH_KWARGS:
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        return NormalizedChatAnthropic(**llm_kwargs)

    def validate_model(self) -> bool:
        """驗證 Anthropic 的模型。"""
        return validate_model("anthropic", self.model)
