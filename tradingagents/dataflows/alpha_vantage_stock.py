from datetime import datetime
from .alpha_vantage_common import _make_api_request, _filter_csv_by_date_range

def get_stock(
    symbol: str,
    start_date: str,
    end_date: str
) -> str:
    """
    回傳經過指定日期範圍篩選的原始每日 OHLCV 值、調整後收盤價，
    以及歷史拆股／配息事件。

    Args:
        symbol: 股票名稱。例如：symbol=IBM
        start_date: 開始日期，格式為 yyyy-mm-dd
        end_date: 結束日期，格式為 yyyy-mm-dd

    Returns:
        包含經日期範圍篩選的每日調整時間序列資料的 CSV 字串。
    """
    # 解析日期以判斷範圍
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    today = datetime.now()

    # 根據請求範圍是否在最近 100 天內來選擇 outputsize
    # compact 回傳最近 100 個資料點，因此檢查 start_date 是否夠近
    days_from_today_to_start = (today - start_dt).days
    outputsize = "compact" if days_from_today_to_start < 100 else "full"

    params = {
        "symbol": symbol,
        "outputsize": outputsize,
        "datatype": "csv",
    }

    response = _make_api_request("TIME_SERIES_DAILY_ADJUSTED", params)

    return _filter_csv_by_date_range(response, start_date, end_date)