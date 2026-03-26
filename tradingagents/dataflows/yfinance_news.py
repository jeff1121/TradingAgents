"""基於 yfinance 的新聞資料取得函式。"""

import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta


def _extract_article_data(article: dict) -> dict:
    """從 yfinance 新聞格式中擷取文章資料（處理巢狀 'content' 結構）。"""
    # 處理巢狀 content 結構
    if "content" in article:
        content = article["content"]
        title = content.get("title", "No title")
        summary = content.get("summary", "")
        provider = content.get("provider", {})
        publisher = provider.get("displayName", "Unknown")

        # 從 canonicalUrl 或 clickThroughUrl 取得 URL
        url_obj = content.get("canonicalUrl") or content.get("clickThroughUrl") or {}
        link = url_obj.get("url", "")

        # 取得發布日期
        pub_date_str = content.get("pubDate", "")
        pub_date = None
        if pub_date_str:
            try:
                pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass

        return {
            "title": title,
            "summary": summary,
            "publisher": publisher,
            "link": link,
            "pub_date": pub_date,
        }
    else:
        # 扁平結構的備援處理
        return {
            "title": article.get("title", "No title"),
            "summary": article.get("summary", ""),
            "publisher": article.get("publisher", "Unknown"),
            "link": article.get("link", ""),
            "pub_date": None,
        }


def get_news_yfinance(
    ticker: str,
    start_date: str,
    end_date: str,
) -> str:
    """
    使用 yfinance 取得特定股票代號的新聞。

    Args:
        ticker: 股票代號（例如 "AAPL"）
        start_date: 開始日期，格式為 yyyy-mm-dd
        end_date: 結束日期，格式為 yyyy-mm-dd

    Returns:
        包含新聞文章的格式化字串
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.get_news(count=20)

        if not news:
            return f"No news found for {ticker}"

        # 解析日期範圍以進行篩選
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        news_str = ""
        filtered_count = 0

        for article in news:
            data = _extract_article_data(article)

            # 若有發布時間則依日期篩選
            if data["pub_date"]:
                pub_date_naive = data["pub_date"].replace(tzinfo=None)
                if not (start_dt <= pub_date_naive <= end_dt + relativedelta(days=1)):
                    continue

            news_str += f"### {data['title']} (source: {data['publisher']})\n"
            if data["summary"]:
                news_str += f"{data['summary']}\n"
            if data["link"]:
                news_str += f"Link: {data['link']}\n"
            news_str += "\n"
            filtered_count += 1

        if filtered_count == 0:
            return f"No news found for {ticker} between {start_date} and {end_date}"

        return f"## {ticker} News, from {start_date} to {end_date}:\n\n{news_str}"

    except Exception as e:
        return f"Error fetching news for {ticker}: {str(e)}"


def get_global_news_yfinance(
    curr_date: str,
    look_back_days: int = 7,
    limit: int = 10,
) -> str:
    """
    使用 yfinance Search 取得全球／總體經濟新聞。

    Args:
        curr_date: 目前日期，格式為 yyyy-mm-dd
        look_back_days: 回顧天數
        limit: 回傳文章的最大數量

    Returns:
        包含全球新聞文章的格式化字串
    """
    # 用於總體／全球新聞的搜尋查詢
    search_queries = [
        "stock market economy",
        "Federal Reserve interest rates",
        "inflation economic outlook",
        "global markets trading",
    ]

    all_news = []
    seen_titles = set()

    try:
        for query in search_queries:
            search = yf.Search(
                query=query,
                news_count=limit,
                enable_fuzzy_query=True,
            )

            if search.news:
                for article in search.news:
                    # 處理扁平與巢狀兩種結構
                    if "content" in article:
                        data = _extract_article_data(article)
                        title = data["title"]
                    else:
                        title = article.get("title", "")

                    # 依標題去重
                    if title and title not in seen_titles:
                        seen_titles.add(title)
                        all_news.append(article)

            if len(all_news) >= limit:
                break

        if not all_news:
            return f"No global news found for {curr_date}"

        # 計算日期範圍
        curr_dt = datetime.strptime(curr_date, "%Y-%m-%d")
        start_dt = curr_dt - relativedelta(days=look_back_days)
        start_date = start_dt.strftime("%Y-%m-%d")

        news_str = ""
        for article in all_news[:limit]:
            # 處理扁平與巢狀兩種結構
            if "content" in article:
                data = _extract_article_data(article)
                title = data["title"]
                publisher = data["publisher"]
                link = data["link"]
                summary = data["summary"]
            else:
                title = article.get("title", "No title")
                publisher = article.get("publisher", "Unknown")
                link = article.get("link", "")
                summary = ""

            news_str += f"### {title} (source: {publisher})\n"
            if summary:
                news_str += f"{summary}\n"
            if link:
                news_str += f"Link: {link}\n"
            news_str += "\n"

        return f"## Global Market News, from {start_date} to {curr_date}:\n\n{news_str}"

    except Exception as e:
        return f"Error fetching global news: {str(e)}"
