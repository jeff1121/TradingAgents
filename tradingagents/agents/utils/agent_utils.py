from langchain_core.messages import HumanMessage, RemoveMessage

# 從各工具模組匯入工具
from tradingagents.agents.utils.core_stock_tools import (
    get_stock_data
)
from tradingagents.agents.utils.technical_indicators_tools import (
    get_indicators
)
from tradingagents.agents.utils.fundamental_data_tools import (
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement
)
from tradingagents.agents.utils.news_data_tools import (
    get_news,
    get_insider_transactions,
    get_global_news
)


def build_instrument_context(ticker: str) -> str:
    """描述確切的金融工具，以便代理程式保留含交易所後綴的股票代碼。"""
    return (
        f"The instrument to analyze is `{ticker}`. "
        "Use this exact ticker in every tool call, report, and recommendation, "
        "preserving any exchange suffix (e.g. `.TO`, `.L`, `.HK`, `.T`)."
    )


def build_language_instruction() -> str:
    """根據設定中的 report_language 產生語言指示。"""
    from tradingagents.dataflows.config import get_config
    config = get_config()
    lang = config.get("report_language", "")
    if lang:
        return f"\n\nIMPORTANT: You MUST write your entire response and report in {lang}."
    return ""

def create_msg_delete():
    def delete_messages(state):
        """清除訊息並新增佔位訊息以相容 Anthropic"""
        messages = state["messages"]

        # 移除所有訊息
        removal_operations = [RemoveMessage(id=m.id) for m in messages]

        # 新增最小化的佔位訊息
        placeholder = HumanMessage(content="Continue")

        return {"messages": removal_operations + [placeholder]}

    return delete_messages


        
