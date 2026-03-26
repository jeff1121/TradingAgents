"""使用 BM25 進行詞彙相似度匹配的金融情境記憶模組。

採用 BM25（Best Matching 25）演算法進行檢索——無需 API 呼叫、
無 token 限制，可在離線環境下搭配任何 LLM 供應商使用。
"""

from rank_bm25 import BM25Okapi
from typing import List, Tuple
import re


class FinancialSituationMemory:
    """使用 BM25 儲存與檢索金融情境的記憶系統。"""

    def __init__(self, name: str, config: dict = None):
        """初始化記憶系統。

        Args:
            name: 此記憶實例的名稱識別碼
            config: 設定字典（為保持 API 相容性而保留，BM25 不使用）
        """
        self.name = name
        self.documents: List[str] = []
        self.recommendations: List[str] = []
        self.bm25 = None

    def _tokenize(self, text: str) -> List[str]:
        """將文字進行 BM25 索引所需的分詞處理。

        使用空白字元與標點符號的簡易分詞，並轉為小寫。
        """
        # 轉為小寫並依非英數字元分割
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def _rebuild_index(self):
        """在新增文件後重建 BM25 索引。"""
        if self.documents:
            tokenized_docs = [self._tokenize(doc) for doc in self.documents]
            self.bm25 = BM25Okapi(tokenized_docs)
        else:
            self.bm25 = None

    def add_situations(self, situations_and_advice: List[Tuple[str, str]]):
        """新增金融情境及其對應的建議。

        Args:
            situations_and_advice: 由 (情境, 建議) 元組組成的列表
        """
        for situation, recommendation in situations_and_advice:
            self.documents.append(situation)
            self.recommendations.append(recommendation)

        # 使用新文件重建 BM25 索引
        self._rebuild_index()

    def get_memories(self, current_situation: str, n_matches: int = 1) -> List[dict]:
        """使用 BM25 相似度查找匹配的建議。

        Args:
            current_situation: 要進行匹配的當前金融情境
            n_matches: 回傳的最佳匹配數量

        Returns:
            包含 matched_situation、recommendation 和 similarity_score 的字典列表
        """
        if not self.documents or self.bm25 is None:
            return []

        # 對查詢進行分詞
        query_tokens = self._tokenize(current_situation)

        # 取得所有文件的 BM25 分數
        scores = self.bm25.get_scores(query_tokens)

        # 取得依分數降序排列的前 n 個索引
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_matches]

        # 組建結果
        results = []
        max_score = max(scores) if max(scores) > 0 else 1  # 正規化分數

        for idx in top_indices:
            # 將分數正規化至 0-1 範圍以保持一致性
            normalized_score = scores[idx] / max_score if max_score > 0 else 0
            results.append({
                "matched_situation": self.documents[idx],
                "recommendation": self.recommendations[idx],
                "similarity_score": normalized_score,
            })

        return results

    def clear(self):
        """清除所有已儲存的記憶。"""
        self.documents = []
        self.recommendations = []
        self.bm25 = None


if __name__ == "__main__":
    # 使用範例
    matcher = FinancialSituationMemory("test_memory")

    # 範例資料
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # 新增範例情境與建議
    matcher.add_situations(example_data)

    # 範例查詢
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
