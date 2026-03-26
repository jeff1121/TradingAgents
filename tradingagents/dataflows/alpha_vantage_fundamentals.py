from .alpha_vantage_common import _make_api_request


def get_fundamentals(ticker: str, curr_date: str = None) -> str:
    """
    使用 Alpha Vantage 取得指定股票代號的完整基本面資料。

    Args:
        ticker (str): 公司的股票代號
        curr_date (str): 目前交易日期，格式為 yyyy-mm-dd（Alpha Vantage 不使用此參數）

    Returns:
        str: 包含財務比率和關鍵指標的公司概覽資料
    """
    params = {
        "symbol": ticker,
    }

    return _make_api_request("OVERVIEW", params)


def get_balance_sheet(ticker: str, freq: str = "quarterly", curr_date: str = None) -> str:
    """
    使用 Alpha Vantage 取得指定股票代號的資產負債表資料。

    Args:
        ticker (str): 公司的股票代號
        freq (str): 報告頻率：annual/quarterly（預設 quarterly）— Alpha Vantage 不使用此參數
        curr_date (str): 目前交易日期，格式為 yyyy-mm-dd（Alpha Vantage 不使用此參數）

    Returns:
        str: 包含正規化欄位的資產負債表資料
    """
    params = {
        "symbol": ticker,
    }

    return _make_api_request("BALANCE_SHEET", params)


def get_cashflow(ticker: str, freq: str = "quarterly", curr_date: str = None) -> str:
    """
    使用 Alpha Vantage 取得指定股票代號的現金流量表資料。

    Args:
        ticker (str): 公司的股票代號
        freq (str): 報告頻率：annual/quarterly（預設 quarterly）— Alpha Vantage 不使用此參數
        curr_date (str): 目前交易日期，格式為 yyyy-mm-dd（Alpha Vantage 不使用此參數）

    Returns:
        str: 包含正規化欄位的現金流量表資料
    """
    params = {
        "symbol": ticker,
    }

    return _make_api_request("CASH_FLOW", params)


def get_income_statement(ticker: str, freq: str = "quarterly", curr_date: str = None) -> str:
    """
    使用 Alpha Vantage 取得指定股票代號的損益表資料。

    Args:
        ticker (str): 公司的股票代號
        freq (str): 報告頻率：annual/quarterly（預設 quarterly）— Alpha Vantage 不使用此參數
        curr_date (str): 目前交易日期，格式為 yyyy-mm-dd（Alpha Vantage 不使用此參數）

    Returns:
        str: 包含正規化欄位的損益表資料
    """
    params = {
        "symbol": ticker,
    }

    return _make_api_request("INCOME_STATEMENT", params)

