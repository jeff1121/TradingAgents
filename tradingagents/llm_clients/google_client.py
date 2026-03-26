import base64
from typing import Any, Optional

from langchain_google_genai import ChatGoogleGenerativeAI

from .base_client import BaseLLMClient, normalize_content
from .validators import validate_model

# ──────────────────────────────────────────────────────────────────────────────
# Monkey-patch: Gemini 3 thought_signature support for langchain-google-genai 2.x
#
# Gemini 3 thinking models always embed a `thought_signature` bytes field on the
# function_call Part in their responses.  When that Part is reconstructed from the
# stored AIMessage during the next API call, the signature must be re-attached or
# the Gemini API rejects the request with:
#   "400 Function call is missing a thought_signature"
#
# langchain-google-genai 3+ handles this natively; 2.x does not.
# google-ai-generativelanguage 0.10+ exposes Part.thought_signature as a proper
# proto field (bytes, field number 13), which makes mutable post-processing safe.
# ──────────────────────────────────────────────────────────────────────────────

_THOUGHT_SIG_KEY = "__gemini_thought_sigs__"


def _apply_gemini_thought_signature_patch() -> None:
    """Patches langchain_google_genai 2.x to round-trip Gemini 3 thought_signature."""
    import langchain_google_genai.chat_models as _gcm

    if getattr(_gcm, "_thought_sig_patched", False):
        return

    # ── Patch 1: _parse_response_candidate ────────────────────────────────────
    # After the original function builds the AIMessage, extract thought_signature
    # bytes from each function_call Part and stash them in additional_kwargs,
    # keyed by tool_call id.
    _orig_parse_response_candidate = _gcm._parse_response_candidate

    def _patched_parse_response_candidate(response_candidate, streaming=False):
        result = _orig_parse_response_candidate(response_candidate, streaming)

        thought_sigs: dict[str, str] = {}
        tc_idx = 0
        for part in response_candidate.content.parts:
            if part.function_call:
                ts = getattr(part, "thought_signature", None)
                if ts:
                    if tc_idx < len(result.tool_calls):
                        tc_id = result.tool_calls[tc_idx]["id"]
                        thought_sigs[tc_id] = base64.b64encode(ts).decode("ascii")
                tc_idx += 1

        if thought_sigs:
            result.additional_kwargs[_THOUGHT_SIG_KEY] = thought_sigs

        return result

    _gcm._parse_response_candidate = _patched_parse_response_candidate

    # ── Patch 2: _parse_chat_history ──────────────────────────────────────────
    # After the original function builds the proto Content objects for history,
    # find the model-role Contents whose Parts carry function_calls and re-attach
    # the thought_signature bytes (stored in the paired AIMessage.additional_kwargs).
    _orig_parse_chat_history = _gcm._parse_chat_history

    def _patched_parse_chat_history(input_messages, convert_system_message_to_human=False):
        from langchain_core.messages import AIMessage as _AIMessage

        system_instruction, messages = _orig_parse_chat_history(
            input_messages, convert_system_message_to_human
        )

        # Collect AIMessages that carry thought_signatures (in input order).
        ai_msgs_with_sigs: list[tuple[_AIMessage, dict[str, str]]] = []
        for msg in input_messages:
            if isinstance(msg, _AIMessage) and msg.tool_calls:
                sigs = msg.additional_kwargs.get(_THOUGHT_SIG_KEY)
                if sigs:
                    ai_msgs_with_sigs.append((msg, sigs))

        if not ai_msgs_with_sigs:
            return system_instruction, messages

        # Walk the output Contents and re-attach thought_signature to the
        # function_call Parts of model-role entries (in the same order they were
        # built from input AIMessages).
        sig_queue_idx = 0
        for content in messages:
            if sig_queue_idx >= len(ai_msgs_with_sigs):
                break
            if content.role != "model":
                continue
            fc_indices = [i for i, p in enumerate(content.parts) if p.function_call]
            if not fc_indices:
                continue

            ai_msg, sigs = ai_msgs_with_sigs[sig_queue_idx]
            sig_queue_idx += 1

            for j, part_idx in enumerate(fc_indices):
                if j < len(ai_msg.tool_calls):
                    tc_id = ai_msg.tool_calls[j]["id"]
                    sig_b64 = sigs.get(tc_id)
                    if sig_b64:
                        try:
                            content.parts[part_idx].thought_signature = base64.b64decode(sig_b64)
                        except Exception:
                            pass

        return system_instruction, messages

    _gcm._parse_chat_history = _patched_parse_chat_history
    _gcm._thought_sig_patched = True


# Apply patch at import time so all ChatGoogleGenerativeAI subclasses benefit.
_apply_gemini_thought_signature_patch()


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
        # thinking_budget=0 明確關閉 thinking（優先採用，供 quick_think_llm 使用）
        thinking_budget = self.kwargs.get("thinking_budget")
        if thinking_budget is not None:
            llm_kwargs["thinking_budget"] = thinking_budget
        else:
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
