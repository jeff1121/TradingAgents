<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <a href="https://github.com/jeff1121/TradingAgents/releases/tag/v0.2.2" target="_blank"><img alt="Version" src="https://img.shields.io/badge/version-v0.2.2-blue?logo=github"/></a>
  <br>
  <a href="https://github.com/jeff1121/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <!-- 保留這些連結。翻譯會隨 README 自動更新。 -->
  <a href="https://www.readme-i18n.com/jeff1121/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/jeff1121/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/jeff1121/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/jeff1121/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/jeff1121/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/jeff1121/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/jeff1121/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/jeff1121/TradingAgents?lang=zh">中文</a>
</div>

---

# TradingAgents：多代理 LLM 金融交易框架

## 最新消息
- [2026-03] **TradingAgents v0.2.2** 發佈，新增 GPT-5.4/Gemini 3.1/Claude 4.6 模型支援、五級評分量表、OpenAI Responses API、Anthropic effort control 以及跨平台穩定性改進。
- [2026-02] **TradingAgents v0.2.0** 發佈，支援多家 LLM 供應商（GPT-5.x、Gemini 3.x、Claude 4.x、Grok 4.x）並改善系統架構。
- [2026-01] **Trading-R1** [技術報告](https://arxiv.org/abs/2509.11420)發佈，[Terminal](https://github.com/jeff1121/Trading-R1) 預計即將推出。

<div align="center">
<a href="https://www.star-history.com/#jeff1121/TradingAgents&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=jeff1121/TradingAgents&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=jeff1121/TradingAgents&type=Date" />
   <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=jeff1121/TradingAgents&type=Date" style="width: 80%; height: auto;" />
 </picture>
</a>
</div>

> 🎉 **TradingAgents** 正式發佈！我們收到了許多關於此專案的詢問，在此衷心感謝社群的熱情支持。
>
> 因此我們決定將框架完全開源。期待與大家一起打造具有影響力的專案！

<div align="center">

🚀 [TradingAgents](#tradingagents-框架) | ⚡ [安裝與 CLI](#安裝與-cli) | 🎬 [展示](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [套件使用方式](#tradingagents-套件) | 🤝 [貢獻](#貢獻) | 📄 [引用](#引用)

</div>

## TradingAgents 框架

TradingAgents 是一個多代理交易框架，模擬真實交易公司的運作模式。透過部署專業的 LLM 驅動代理——從基本面分析師、市場情緒專家、技術分析師，到交易員與風險管理團隊——平台協同評估市場狀況並輔助交易決策。此外，這些代理會進行動態討論，以找出最佳策略。

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> TradingAgents 框架專為研究目的而設計。交易績效可能因多種因素而異，包括所選的骨幹語言模型、模型溫度參數、交易期間、資料品質及其他不確定因素。[本框架不構成任何財務、投資或交易建議。](https://tauric.ai/disclaimer/)

我們的框架將複雜的交易任務分解為各個專業角色，確保系統以穩健且可擴展的方式進行市場分析與決策。

### 分析師團隊
- 基本面分析師：評估公司財務狀況與績效指標，辨識內在價值與潛在風險。
- 情緒分析師：運用情緒評分演算法分析社群媒體與大眾情緒，掌握短期市場氛圍。
- 新聞分析師：監控全球新聞與總體經濟指標，解讀事件對市場狀況的影響。
- 技術分析師：利用技術指標（如 MACD 和 RSI）偵測交易模式並預測價格走勢。

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### 研究員團隊
- 由看多與看空研究員組成，針對分析師團隊提供的見解進行批判性評估。透過結構化辯論，在潛在收益與固有風險之間取得平衡。

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### 交易員代理
- 彙整分析師與研究員的報告，做出明智的交易決策。根據全面的市場洞察，決定交易的時機與規模。

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### 風險管理與投資組合經理
- 透過評估市場波動性、流動性及其他風險因素，持續監控投資組合風險。風險管理團隊評估並調整交易策略，將評估報告提交給投資組合經理做最終決策。
- 投資組合經理批准或駁回交易提案。一旦批准，訂單將發送至模擬交易所並執行。

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## 安裝與 CLI

### 安裝

複製 TradingAgents 儲存庫：
```bash
git clone https://github.com/jeff1121/TradingAgents.git
cd TradingAgents
```

使用你偏好的環境管理工具建立虛擬環境並安裝套件：

**推薦：使用 uv（速度最快）**
```bash
pip install uv                 # 若尚未安裝 uv
uv sync                        # 自動建立 .venv 並從 uv.lock 還原所有依賴
```

**或使用 conda**
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
pip install .
```

### 必要的 API

TradingAgents 支援多家 LLM 供應商。請設定你所選供應商的 API 金鑰：

```bash
export OPENAI_API_KEY=...          # OpenAI (GPT)
export GOOGLE_API_KEY=...          # Google (Gemini)
export ANTHROPIC_API_KEY=...       # Anthropic (Claude)
export XAI_API_KEY=...             # xAI (Grok)
export OPENROUTER_API_KEY=...      # OpenRouter
export ALPHA_VANTAGE_API_KEY=...   # Alpha Vantage
```

若要使用本機模型，請在設定中將 `llm_provider` 設為 `"ollama"` 以使用 Ollama。

或者，將 `.env.example` 複製為 `.env` 並填入你的金鑰：
```bash
cp .env.example .env
```

### CLI 使用方式

啟動互動式 CLI：
```bash
tradingagents          # 已安裝的指令
python -m cli.main     # 替代方式：直接從原始碼執行
```
你將看到一個畫面，可以選擇想要的股票代碼、分析日期、LLM 供應商、研究深度等。

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

介面將顯示即時載入的結果，讓你追蹤代理的執行進度。

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

## TradingAgents 套件

### 實作細節

我們使用 LangGraph 建構 TradingAgents，以確保靈活性與模組化。框架支援多家 LLM 供應商：OpenAI、Google、Anthropic、xAI、OpenRouter 及 Ollama。

### Python 使用方式

若要在程式碼中使用 TradingAgents，你可以匯入 `tradingagents` 模組並初始化 `TradingAgentsGraph()` 物件。`.propagate()` 函式將回傳決策結果。你可以執行 `main.py`，以下是一個簡單範例：

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# forward propagate
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

你也可以調整預設設定，自訂 LLM 選擇、辯論回合數等。

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"        # openai, google, anthropic, xai, openrouter, ollama
config["deep_think_llm"] = "gpt-5.2"     # Model for complex reasoning
config["quick_think_llm"] = "gpt-5-mini" # Model for quick tasks
config["max_debate_rounds"] = 2

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

所有設定選項請參閱 `tradingagents/default_config.py`。

## 貢獻

我們歡迎社群的貢獻！無論是修復 bug、改善文件，還是提出新功能建議，你的參與都能讓這個專案更好。如果你對這個研究方向感興趣，歡迎加入我們的開源金融 AI 研究社群 [Tauric Research](https://tauric.ai/)。

## 引用

如果 *TradingAgents* 對你有所幫助，請引用我們的研究 :)

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```
