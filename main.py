from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

from dotenv import load_dotenv

# 從 .env 檔案載入環境變數
load_dotenv()

# 建立自訂設定
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "github"
config["deep_think_llm"] = "openai/gpt-4.1"
config["quick_think_llm"] = "openai/gpt-4.1-mini"
config["max_debate_rounds"] = 1  # 減少辯論回合數以加快測試

# 配置資料供應商（預設使用 yfinance，不需額外 API 金鑰）
config["data_vendors"] = {
    "core_stock_apis": "yfinance",           # 選項：alpha_vantage、yfinance
    "technical_indicators": "yfinance",      # 選項：alpha_vantage、yfinance
    "fundamental_data": "yfinance",          # 選項：alpha_vantage、yfinance
    "news_data": "yfinance",                 # 選項：alpha_vantage、yfinance
}

# 使用自訂設定初始化
ta = TradingAgentsGraph(debug=True, config=config)

# 前向傳播
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)

# 記憶錯誤並反思
# ta.reflect_and_remember(1000) # 參數為持倉報酬
