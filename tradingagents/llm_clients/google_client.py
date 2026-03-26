from typing import Any, Optional

from langchain_google_genai import ChatGoogleGenerativeAI

from .base_client import BaseLLMClient, normalize_content
from .validators import validate_model


class NormalizedChatGoogleGenerativeAI(ChatGoogleGenerativeAI):
    """具有正規化內容輸出的 ChatGoogleGenerativeAI。

    Gemini 3 模型會以型別區塊清單回傳內容。
    此類別將其正規化為字串，確保下游處理的一致性。
    """

    def invoke(self, input, config=None, **kwargs):
        return normalize_content(super().invoke(input, config, **kwargs))


class GoogleClient(BaseLLMClient):
    """Google Gemini 模型的客戶端。"""

    def __init__(self, model: str, base_url: Optional[str] = None, **kwargs):
        super().__init__(model, base_url, **kwargs)

    def get_llm(self) -> Any:
        """回傳已設定的 ChatGoogleGenerativeAI 實例。"""
        llm_kwargs = {"model": self.model}

        for key in ("timeout", "max_retries", "google_api_key", "callbacks", "http_client", "http_async_client"):
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        # 根據模型將 thinking_level 對應到適當的 API 參數
        # Gemini 3 Pro：low、high
        # Gemini 3 Flash：minimal、low、medium、high
        # Gemini 2.5：thinking_budget（0=停用，-1=動態）
        thinking_level = self.kwargs.get("thinking_level")
        if thinking_level:
            model_lower = self.model.lower()
            if "gemini-3" in model_lower:
                # Gemini 3 Pro 不支援 "minimal"，改用 "low"
                if "pro" in model_lower and thinking_level == "minimal":
                    thinking_level = "low"
                llm_kwargs["thinking_level"] = thinking_level
            else:
                # Gemini 2.5：對應到 thinking_budget
                llm_kwargs["thinking_budget"] = -1 if thinking_level == "high" else 0

        return NormalizedChatGoogleGenerativeAI(**llm_kwargs)

    def validate_model(self) -> bool:
        """驗證 Google 的模型。"""
        return validate_model("google", self.model)
