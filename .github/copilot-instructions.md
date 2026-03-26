# TradingAgents 的 Copilot 指引

## 建置與執行

```bash
uv sync                        # Install package + dependencies（從 uv.lock 還原，推薦）
uv sync --dev                  # 含開發依賴（如 pytest）
uv run tradingagents           # Launch interactive CLI
uv run python -m cli.main      # Alternative CLI launch
uv run python main.py          # Run single analysis via script
```

> 若已啟動虛擬環境（`source .venv/bin/activate`），可直接使用 `tradingagents` / `python -m cli.main`。
>
> 舊版相容：`pip install .` 與 `pip install -e .` 仍可正常使用（setuptools 不變）。

### 測試

```bash
uv run pytest tests/                                  # Full suite
uv run pytest tests/test_ticker_symbol_handling.py    # Single file
uv run pytest tests/test_ticker_symbol_handling.py::TickerSymbolHandlingTests::test_normalize_ticker_symbol_preserves_exchange_suffix  # Single test
```

測試使用 `unittest.TestCase`，由 pytest 進行探索與執行。

## 架構

TradingAgents 是一個基於 LangGraph 的多代理框架，模擬一間交易公司的運作。核心進入點為 `tradingagents/graph/trading_graph.py` 中的 `TradingAgentsGraph`。

### 代理管線

呼叫 `ta.propagate(ticker, date)` 會執行以下 LangGraph `StateGraph`：

```
分析師（循序執行，含工具呼叫迴圈）
  → 市場 → 社群 → 新聞 → 基本面
    ↓
研究員辯論（多頭 vs 空頭，可設定回合數）
  → 多頭研究員 ↔ 空頭研究員 → 研究經理（裁判）
    ↓
交易員（將報告彙整為交易計畫）
    ↓
風險辯論（三方，可設定回合數）
  → 積極型 ↔ 保守型 ↔ 中立型 → 投資組合經理（最終決策）
```

每位分析師在工具呼叫迴圈中運行：LLM 呼叫工具 → 工具回傳結果 → LLM 彙整為報告。為了管理上下文，分析師之間的訊息會被清除。

### 主要模組

- **`tradingagents/graph/`** — 圖形建構與流程編排。`setup.py` 建立 `StateGraph`，`conditional_logic.py` 控制路由，`propagation.py` 建立初始狀態，`reflection.py` 處理交易後學習，`signal_processing.py` 擷取最終評等（BUY/OVERWEIGHT/HOLD/UNDERWEIGHT/SELL）。
- **`tradingagents/agents/`** — 依角色分類的代理工廠函式：`analysts/`、`researchers/`、`trader/`、`risk_mgmt/`、`managers/`。所有代理皆透過 `create_*()` 工廠函式建立（非類別）。
- **`tradingagents/dataflows/`** — 資料抽象層，含供應商路由。`interface.py` 將方法名稱對應至供應商實作（yfinance、Alpha Vantage），並在遇到速率限制時自動降級。
- **`tradingagents/llm_clients/`** — 多供應商 LLM 抽象層。`BaseLLMClient` 抽象基底類別，搭配 `OpenAIClient`（亦支援 xAI、Ollama、OpenRouter）、`AnthropicClient`、`GoogleClient`。透過 `create_llm_client()` 工廠函式建立。
- **`cli/`** — 使用 Typer + Rich 的互動式 CLI。

### 狀態管理

此圖形使用三個 TypedDict 狀態：
- `AgentState`（繼承 `MessagesState`）— 頂層狀態，承載報告、辯論子狀態與最終決策。
- `InvestDebateState` — 追蹤多頭/空頭辯論歷史與回合數。
- `RiskDebateState` — 追蹤積極型/保守型/中立型辯論歷史與回合數。

### 記憶系統

`FinancialSituationMemory` 使用 BM25（rank_bm25）進行離線詞彙相似度比對——不需要 API 呼叫，也不需要向量資料庫。每個代理角色（bull、bear、trader、invest_judge、portfolio_manager）皆有各自的記憶實例，透過 `reflect_and_remember()` 填充。

## 重要慣例

### 代理模式

每個代理都是一個**工廠函式**，回傳閉包（而非類別）：

```python
def create_<role>(llm, memory=None):
    def <role>_node(state):
        # Build prompt with ChatPromptTemplate
        # Bind tools to LLM, invoke, return state updates
        return {"messages": [result], "<role>_report": report}
    return <role>_node
```

代理註冊於 `tradingagents/agents/__init__.py`，並透過 `__all__` 匯出。

### 資料供應商路由

`tradingagents/agents/utils/` 中的資料工具（例如 `get_stock_data`、`get_indicators`）是以 `@tool` 裝飾的函式，會呼叫 `tradingagents/dataflows/interface.py` 中的 `route_to_vendor()`。供應商在兩個層級解析：類別層級（`data_vendors`）與工具層級（`tool_vendors`，優先採用）。

### LLM 用戶端正規化

所有 LLM 用戶端將其 LangChain 聊天模型包裝在 `Normalized*` 子類別中，將區塊列表回應（來自 OpenAI Responses API、Gemini、Claude 延伸思考）轉換為純字串。這點至關重要——代理預期 `response.content` 為字串。

### 組態設定

所有組態流經 `tradingagents/default_config.py` → `DEFAULT_CONFIG` 字典。資料流層透過 `tradingagents/dataflows/config.py` 中的模組級單例（`get_config()`/`set_config()`）取得設定。請務必使用 `DEFAULT_CONFIG.copy()` 以避免修改全域預設值。

### 雙層 LLM 使用策略

- `quick_think_llm` — 用於分析師、研究員、風險辯論者、反思、訊號處理。
- `deep_think_llm` — 用於研究經理（裁判）與投資組合經理（最終決策）——兩個最關鍵的決策節點。

### 環境變數

API 金鑰從環境變數或 `.env` 檔案（透過 python-dotenv）載入。必要條件：至少需要一個 LLM 供應商的金鑰。完整清單請參閱 `.env.example`。`ALPHA_VANTAGE_API_KEY` 僅在使用 Alpha Vantage 作為資料供應商時才需要。
