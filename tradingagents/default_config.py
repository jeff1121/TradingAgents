import os

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM 設定
    "llm_provider": "openai",
    "deep_think_llm": "gpt-5.2",
    "quick_think_llm": "gpt-5-mini",
    "backend_url": "https://api.openai.com/v1",
    # 報表語言設定（空字串表示不指定，使用 LLM 預設語言）
    "report_language": "繁體中文",
    # 供應商專用思考配置
    "google_thinking_level": None,      # "high"、"minimal" 等
    "openai_reasoning_effort": None,    # "medium"、"high"、"low"
    "anthropic_effort": None,           # "high"、"medium"、"low"
    # 辯論與討論設定
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # 資料供應商配置
    # 類別層級配置（該類別中所有工具的預設值）
    "data_vendors": {
        "core_stock_apis": "yfinance",       # 選項：alpha_vantage、yfinance
        "technical_indicators": "yfinance",  # 選項：alpha_vantage、yfinance
        "fundamental_data": "yfinance",      # 選項：alpha_vantage、yfinance
        "news_data": "yfinance",             # 選項：alpha_vantage、yfinance
    },
    # 工具層級配置（優先於類別層級）
    "tool_vendors": {
        # 範例："get_stock_data": "alpha_vantage",  # 覆寫類別預設值
    },
}
