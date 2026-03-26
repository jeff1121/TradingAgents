# TradingAgents/graph/signal_processing.py — 訊號處理模組

from langchain_openai import ChatOpenAI


class SignalProcessor:
    """處理交易訊號以提取可執行的決策。"""

    def __init__(self, quick_thinking_llm: ChatOpenAI):
        """以 LLM 進行初始化以處理訊號。"""
        self.quick_thinking_llm = quick_thinking_llm

    def process_signal(self, full_signal: str) -> str:
        """
        處理完整的交易訊號以提取核心決策。

        Args:
            full_signal: 完整的交易訊號文字

        Returns:
            提取的評級（BUY、OVERWEIGHT、HOLD、UNDERWEIGHT 或 SELL）
        """
        messages = [
            (
                "system",
                "You are an efficient assistant that extracts the trading decision from analyst reports. "
                "Extract the rating as exactly one of: BUY, OVERWEIGHT, HOLD, UNDERWEIGHT, SELL. "
                "Output only the single rating word, nothing else.",
            ),
            ("human", full_signal),
        ]

        return self.quick_thinking_llm.invoke(messages).content
