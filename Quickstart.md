# TradingAgents 快速入門指南

本指南將帶你從零開始安裝與使用 TradingAgents 框架。

---

## 1. 環境需求

| 項目 | 最低版本 |
|------|----------|
| Python | ≥ 3.10 |
| pip | 最新版本（建議） |
| Git | 任意版本 |

> **建議：** 使用 Python 3.13 以獲得最佳相容性。

---

## 2. 安裝步驟

### 2.1 複製專案

```bash
git clone https://github.com/jeff1121/TradingAgents.git
cd TradingAgents
```

### 2.2 建立虛擬環境

你可以選擇 `venv` 或 `conda` 來建立虛擬環境：

**使用 venv：**

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

**使用 conda：**

```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

### 2.3 安裝套件與相依套件

```bash
pip install .
```

---

## 3. API 金鑰設定

TradingAgents 支援多個 LLM 供應商。你只需設定所使用供應商的金鑰即可。

### 方法一：環境變數

在終端機中直接匯出：

```bash
export OPENAI_API_KEY=你的金鑰          # OpenAI (GPT)
export GOOGLE_API_KEY=你的金鑰          # Google (Gemini)
export ANTHROPIC_API_KEY=你的金鑰       # Anthropic (Claude)
export XAI_API_KEY=你的金鑰             # xAI (Grok)
export OPENROUTER_API_KEY=你的金鑰      # OpenRouter
```

### 方法二：使用 `.env` 檔案

將範本複製為 `.env`，然後填入你的金鑰：

```bash
cp .env.example .env
```

`.env.example` 的內容如下，請在 `=` 後方填入對應的值：

```
OPENAI_API_KEY=
GOOGLE_API_KEY=
ANTHROPIC_API_KEY=
XAI_API_KEY=
OPENROUTER_API_KEY=
```

> **注意：** 若使用本機模型（Ollama），無需設定任何 API 金鑰，只需在設定中將 `llm_provider` 改為 `"ollama"` 即可。

---

## 4. CLI 使用方式

安裝完成後，可透過以下任一指令啟動互動式介面：

```bash
tradingagents          # 已安裝的指令
python -m cli.main     # 從原始碼直接執行
```

啟動後，你將看到互動式介面，可以選擇：

- **股票代碼**（例如 NVDA、AAPL）
- **分析日期**
- **LLM 供應商**
- **研究深度**
- 以及其他選項

系統會即時顯示各代理人的分析進度與最終交易決策。

---

## 5. Python 程式碼使用

你也可以在自己的 Python 程式中直接匯入 TradingAgents。

### 基本範例

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# 前向傳播，取得交易決策
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

### 自訂設定範例

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"        # openai, google, anthropic, xai, openrouter, ollama
config["deep_think_llm"] = "gpt-5.2"     # 用於複雜推理的模型
config["quick_think_llm"] = "gpt-5-mini" # 用於快速任務的模型
config["max_debate_rounds"] = 2          # 研究員辯論回合數

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

### 使用 `.env` 載入金鑰

若你的金鑰存放在 `.env` 檔案中，請在程式開頭加入：

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 6. 設定選項

所有可用的設定項目定義在 `tradingagents/default_config.py` 中。以下為主要選項說明：

### LLM 相關設定

| 設定鍵 | 預設值 | 說明 |
|--------|--------|------|
| `llm_provider` | `"openai"` | LLM 供應商：`openai`、`google`、`anthropic`、`xai`、`openrouter`、`ollama` |
| `deep_think_llm` | `"gpt-5.2"` | 用於複雜推理任務的模型 |
| `quick_think_llm` | `"gpt-5-mini"` | 用於快速回應任務的模型 |
| `backend_url` | `"https://api.openai.com/v1"` | API 端點（自訂或本機部署時使用） |

### 供應商專屬思考設定

| 設定鍵 | 預設值 | 說明 |
|--------|--------|------|
| `google_thinking_level` | `None` | Google 模型的思考等級，例如 `"high"`、`"minimal"` |
| `openai_reasoning_effort` | `None` | OpenAI 模型的推理強度，例如 `"high"`、`"medium"`、`"low"` |
| `anthropic_effort` | `None` | Anthropic 模型的投入程度，例如 `"high"`、`"medium"`、`"low"` |

### 辯論與討論設定

| 設定鍵 | 預設值 | 說明 |
|--------|--------|------|
| `max_debate_rounds` | `1` | 研究員（多空雙方）辯論的最大回合數 |
| `max_risk_discuss_rounds` | `1` | 風險管理討論的最大回合數 |
| `max_recur_limit` | `100` | 圖遍歷的最大遞迴上限 |

### 資料來源設定

預設使用 `yfinance`（免費，無需額外金鑰）。若需要更多資料，可切換至 `alpha_vantage`（需設定 `ALPHA_VANTAGE_API_KEY`）。

```python
config["data_vendors"] = {
    "core_stock_apis": "yfinance",           # 選項：alpha_vantage, yfinance
    "technical_indicators": "yfinance",      # 選項：alpha_vantage, yfinance
    "fundamental_data": "yfinance",          # 選項：alpha_vantage, yfinance
    "news_data": "yfinance",                 # 選項：alpha_vantage, yfinance
}
```

你也可以在 `tool_vendors` 中針對個別工具覆寫設定：

```python
config["tool_vendors"] = {
    "get_stock_data": "alpha_vantage",  # 僅覆寫此工具的資料來源
}
```

### 其他設定

| 設定鍵 | 預設值 | 說明 |
|--------|--------|------|
| `results_dir` | `"./results"` | 分析結果輸出目錄（可透過環境變數 `TRADINGAGENTS_RESULTS_DIR` 覆寫） |

---

## 延伸閱讀

- [README.md](./README.md) — 完整專案說明與架構介紹
- [tradingagents/default_config.py](./tradingagents/default_config.py) — 所有設定選項的原始定義
- [.env.example](./.env.example) — API 金鑰範本
- [arXiv 論文](https://arxiv.org/abs/2412.20138) — TradingAgents 研究論文
