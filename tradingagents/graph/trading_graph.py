# TradingAgents/graph/trading_graph.py — 交易代理圖主模組

import os
from pathlib import Path
import json
from datetime import date
from typing import Dict, Any, Tuple, List, Optional

from langgraph.prebuilt import ToolNode

from tradingagents.llm_clients import create_llm_client

from tradingagents.agents import *
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.agents.utils.memory import FinancialSituationMemory
from tradingagents.agents.utils.agent_states import (
    AgentState,
    InvestDebateState,
    RiskDebateState,
)
from tradingagents.dataflows.config import set_config

# 從 agent_utils 匯入抽象工具方法
from tradingagents.agents.utils.agent_utils import (
    get_stock_data,
    get_indicators,
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement,
    get_news,
    get_insider_transactions,
    get_global_news
)

from .conditional_logic import ConditionalLogic
from .setup import GraphSetup
from .propagation import Propagator
from .reflection import Reflector
from .signal_processing import SignalProcessor


class TradingAgentsGraph:
    """協調交易代理框架的主要類別。"""

    def __init__(
        self,
        selected_analysts=["market", "social", "news", "fundamentals"],
        debug=False,
        config: Dict[str, Any] = None,
        callbacks: Optional[List] = None,
    ):
        """初始化交易代理圖及各元件。

        Args:
            selected_analysts: 要納入的分析師類型列表
            debug: 是否以除錯模式執行
            config: 設定字典。若為 None 則使用預設設定
            callbacks: 可選的回呼處理器列表（例如用於追蹤 LLM / 工具統計）
        """
        self.debug = debug
        self.config = config or DEFAULT_CONFIG
        self.callbacks = callbacks or []

        # GITHUB_TOKEN 環境變數優先：若有設定且未指定其他供應商，自動切換為 GitHub Models
        github_token = os.getenv("GITHUB_TOKEN", "")
        if github_token and self.config.get("llm_provider", "openai") in ("openai",):
            self.config["llm_provider"] = "github"

        # 更新介面的設定
        set_config(self.config)

        # 建立必要的目錄
        os.makedirs(
            os.path.join(self.config["project_dir"], "dataflows/data_cache"),
            exist_ok=True,
        )

        # 使用供應商特定的思考設定初始化 LLM
        llm_kwargs = self._get_provider_kwargs()

        # 若有提供 callbacks，加入 kwargs（傳給 LLM 建構函式）
        if self.callbacks:
            llm_kwargs["callbacks"] = self.callbacks

        # quick_think_llm 用於呼叫工具的分析師代理，不可啟用 thinking
        # （Gemini thinking 模式下工具呼叫需 thought_signature，langchain 尚未支援）
        # 移除思考相關 kwargs，並對 Google 明確關閉 thinking（thinking_budget=0）
        thinking_keys = ("thinking_level", "thinking_budget", "reasoning_effort", "effort")
        quick_kwargs = {k: v for k, v in llm_kwargs.items() if k not in thinking_keys}
        if self.config.get("llm_provider", "").lower() == "google":
            quick_kwargs["thinking_budget"] = 0  # 明確關閉 Gemini thinking，避免 thought_signature 問題

        deep_client = create_llm_client(
            provider=self.config["llm_provider"],
            model=self.config["deep_think_llm"],
            base_url=self._resolve_base_url(),
            **llm_kwargs,
        )
        quick_client = create_llm_client(
            provider=self.config["llm_provider"],
            model=self.config["quick_think_llm"],
            base_url=self._resolve_base_url(),
            **quick_kwargs,
        )

        self.deep_thinking_llm = deep_client.get_llm()
        self.quick_thinking_llm = quick_client.get_llm()
        
        # 初始化記憶模組
        self.bull_memory = FinancialSituationMemory("bull_memory", self.config)
        self.bear_memory = FinancialSituationMemory("bear_memory", self.config)
        self.trader_memory = FinancialSituationMemory("trader_memory", self.config)
        self.invest_judge_memory = FinancialSituationMemory("invest_judge_memory", self.config)
        self.portfolio_manager_memory = FinancialSituationMemory("portfolio_manager_memory", self.config)

        # 建立工具節點
        self.tool_nodes = self._create_tool_nodes()

        # 初始化各元件
        self.conditional_logic = ConditionalLogic(
            max_debate_rounds=self.config["max_debate_rounds"],
            max_risk_discuss_rounds=self.config["max_risk_discuss_rounds"],
        )
        self.graph_setup = GraphSetup(
            self.quick_thinking_llm,
            self.deep_thinking_llm,
            self.tool_nodes,
            self.bull_memory,
            self.bear_memory,
            self.trader_memory,
            self.invest_judge_memory,
            self.portfolio_manager_memory,
            self.conditional_logic,
        )

        self.propagator = Propagator()
        self.reflector = Reflector(self.quick_thinking_llm)
        self.signal_processor = SignalProcessor(self.quick_thinking_llm)

        # 狀態追蹤
        self.curr_state = None
        self.ticker = None
        self.log_states_dict = {}  # 日期對應完整狀態字典

        # 設定圖
        self.graph = self.graph_setup.setup_graph(selected_analysts)

    def _resolve_base_url(self) -> Optional[str]:
        """解析 LLM API 的基底 URL。"""
        return self.config.get("backend_url")

    def _get_provider_kwargs(self) -> Dict[str, Any]:
        """取得供應商特定的 LLM 客戶端建立參數。"""
        kwargs = {}
        provider = self.config.get("llm_provider", "").lower()

        if provider == "google":
            thinking_level = self.config.get("google_thinking_level")
            if thinking_level:
                kwargs["thinking_level"] = thinking_level

        elif provider == "openai":
            reasoning_effort = self.config.get("openai_reasoning_effort")
            if reasoning_effort:
                kwargs["reasoning_effort"] = reasoning_effort

        elif provider == "anthropic":
            effort = self.config.get("anthropic_effort")
            if effort:
                kwargs["effort"] = effort

        return kwargs

    def _create_tool_nodes(self) -> Dict[str, ToolNode]:
        """使用抽象方法為不同資料來源建立工具節點。"""
        return {
            "market": ToolNode(
                [
                    # 核心股票資料工具
                    get_stock_data,
                    # 技術指標
                    get_indicators,
                ]
            ),
            "social": ToolNode(
                [
                    # 用於社群媒體分析的新聞工具
                    get_news,
                ]
            ),
            "news": ToolNode(
                [
                    # 新聞與內部人交易資訊
                    get_news,
                    get_global_news,
                    get_insider_transactions,
                ]
            ),
            "fundamentals": ToolNode(
                [
                    # 基本面分析工具
                    get_fundamentals,
                    get_balance_sheet,
                    get_cashflow,
                    get_income_statement,
                ]
            ),
        }

    def propagate(self, company_name, trade_date):
        """針對特定日期的公司執行交易代理圖。"""

        self.ticker = company_name

        # 初始化狀態
        init_agent_state = self.propagator.create_initial_state(
            company_name, trade_date
        )
        args = self.propagator.get_graph_args()

        if self.debug:
            # 除錯模式（含追蹤）
            trace = []
            for chunk in self.graph.stream(init_agent_state, **args):
                if len(chunk["messages"]) == 0:
                    pass
                else:
                    chunk["messages"][-1].pretty_print()
                    trace.append(chunk)

            final_state = trace[-1]
        else:
            # 標準模式（不含追蹤）
            final_state = self.graph.invoke(init_agent_state, **args)

        # 儲存當前狀態以供反思使用
        self.curr_state = final_state

        # 記錄狀態
        self._log_state(trade_date, final_state)

        # 回傳決策與處理後的訊號
        return final_state, self.process_signal(final_state["final_trade_decision"])

    def _log_state(self, trade_date, final_state):
        """將最終狀態記錄到 JSON 檔案。"""
        self.log_states_dict[str(trade_date)] = {
            "company_of_interest": final_state["company_of_interest"],
            "trade_date": final_state["trade_date"],
            "market_report": final_state["market_report"],
            "sentiment_report": final_state["sentiment_report"],
            "news_report": final_state["news_report"],
            "fundamentals_report": final_state["fundamentals_report"],
            "investment_debate_state": {
                "bull_history": final_state["investment_debate_state"]["bull_history"],
                "bear_history": final_state["investment_debate_state"]["bear_history"],
                "history": final_state["investment_debate_state"]["history"],
                "current_response": final_state["investment_debate_state"][
                    "current_response"
                ],
                "judge_decision": final_state["investment_debate_state"][
                    "judge_decision"
                ],
            },
            "trader_investment_decision": final_state["trader_investment_plan"],
            "risk_debate_state": {
                "aggressive_history": final_state["risk_debate_state"]["aggressive_history"],
                "conservative_history": final_state["risk_debate_state"]["conservative_history"],
                "neutral_history": final_state["risk_debate_state"]["neutral_history"],
                "history": final_state["risk_debate_state"]["history"],
                "judge_decision": final_state["risk_debate_state"]["judge_decision"],
            },
            "investment_plan": final_state["investment_plan"],
            "final_trade_decision": final_state["final_trade_decision"],
        }

        # 儲存到檔案
        directory = Path(f"eval_results/{self.ticker}/TradingAgentsStrategy_logs/")
        directory.mkdir(parents=True, exist_ok=True)

        with open(
            f"eval_results/{self.ticker}/TradingAgentsStrategy_logs/full_states_log_{trade_date}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(self.log_states_dict, f, indent=4)

    def reflect_and_remember(self, returns_losses):
        """根據報酬對決策進行反思並更新記憶。"""
        self.reflector.reflect_bull_researcher(
            self.curr_state, returns_losses, self.bull_memory
        )
        self.reflector.reflect_bear_researcher(
            self.curr_state, returns_losses, self.bear_memory
        )
        self.reflector.reflect_trader(
            self.curr_state, returns_losses, self.trader_memory
        )
        self.reflector.reflect_invest_judge(
            self.curr_state, returns_losses, self.invest_judge_memory
        )
        self.reflector.reflect_portfolio_manager(
            self.curr_state, returns_losses, self.portfolio_manager_memory
        )

    def process_signal(self, full_signal):
        """處理訊號以提取核心決策。"""
        return self.signal_processor.process_signal(full_signal)
