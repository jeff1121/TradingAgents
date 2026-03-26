from abc import ABC, abstractmethod
from typing import Any, Optional


def normalize_content(response):
    """將 LLM 回應內容正規化為純字串。

    多個供應商（OpenAI Responses API、Google Gemini 3）會以型別區塊清單回傳內容，
    例如 [{'type': 'reasoning', ...}, {'type': 'text', 'text': '...'}]。
    下游 agent 預期 response.content 為字串。此函式會擷取並合併 text 區塊，
    捨棄 reasoning/metadata 區塊。
    """
    content = response.content
    if isinstance(content, list):
        texts = [
            item.get("text", "") if isinstance(item, dict) and item.get("type") == "text"
            else item if isinstance(item, str) else ""
            for item in content
        ]
        response.content = "\n".join(t for t in texts if t)
    return response


class BaseLLMClient(ABC):
    """LLM 客戶端的抽象基底類別。"""

    def __init__(self, model: str, base_url: Optional[str] = None, **kwargs):
        self.model = model
        self.base_url = base_url
        self.kwargs = kwargs

    @abstractmethod
    def get_llm(self) -> Any:
        """回傳已設定的 LLM 實例。"""
        pass

    @abstractmethod
    def validate_model(self) -> bool:
        """驗證此客戶端是否支援該模型。"""
        pass
