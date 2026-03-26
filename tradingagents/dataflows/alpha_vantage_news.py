from .alpha_vantage_common import _make_api_request, format_datetime_for_api

def get_news(ticker, start_date, end_date) -> dict[str, str] | str:
    """回傳來自全球頂尖新聞媒體的即時與歷史市場新聞及情緒資料。

    涵蓋股票、加密貨幣、外匯，以及財政政策、併購、IPO 等主題。

    Args:
        ticker: 新聞文章的股票代號。
        start_date: 新聞搜尋的開始日期。
        end_date: 新聞搜尋的結束日期。

    Returns:
        包含新聞情緒資料的字典或 JSON 字串。
    """

    params = {
        "tickers": ticker,
        "time_from": format_datetime_for_api(start_date),
        "time_to": format_datetime_for_api(end_date),
    }

    return _make_api_request("NEWS_SENTIMENT", params)

def get_global_news(curr_date, look_back_days: int = 7, limit: int = 50) -> dict[str, str] | str:
    """回傳不限特定股票代號的全球市場新聞及情緒資料。

    涵蓋金融市場、經濟等廣泛市場主題。

    Args:
        curr_date: 目前日期，格式為 yyyy-mm-dd。
        look_back_days: 回顧天數（預設 7）。
        limit: 文章最大數量（預設 50）。

    Returns:
        包含全球新聞情緒資料的字典或 JSON 字串。
    """
    from datetime import datetime, timedelta

    # 計算開始日期
    curr_dt = datetime.strptime(curr_date, "%Y-%m-%d")
    start_dt = curr_dt - timedelta(days=look_back_days)
    start_date = start_dt.strftime("%Y-%m-%d")

    params = {
        "topics": "financial_markets,economy_macro,economy_monetary",
        "time_from": format_datetime_for_api(start_date),
        "time_to": format_datetime_for_api(curr_date),
        "limit": str(limit),
    }

    return _make_api_request("NEWS_SENTIMENT", params)


def get_insider_transactions(symbol: str) -> dict[str, str] | str:
    """回傳關鍵利害關係人的最新及歷史內部人交易資料。

    涵蓋創辦人、高階主管、董事會成員等的交易。

    Args:
        symbol: 股票代號。範例："IBM"。

    Returns:
        包含內部人交易資料的字典或 JSON 字串。
    """

    params = {
        "symbol": symbol,
    }

    return _make_api_request("INSIDER_TRANSACTIONS", params)