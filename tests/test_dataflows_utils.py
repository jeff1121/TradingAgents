"""dataflows/utils 的單元測試。"""

import unittest
from datetime import datetime, date
from unittest.mock import patch, MagicMock
import pandas as pd

from tradingagents.dataflows.utils import (
    save_output,
    get_current_date,
    get_next_weekday,
    decorate_all_methods,
)


class TestGetCurrentDate(unittest.TestCase):
    def test_format(self):
        result = get_current_date()
        # 驗證 YYYY-MM-DD 格式
        datetime.strptime(result, "%Y-%m-%d")

    def test_matches_today(self):
        expected = date.today().strftime("%Y-%m-%d")
        self.assertEqual(get_current_date(), expected)


class TestGetNextWeekday(unittest.TestCase):
    def test_weekday_returns_same(self):
        # 2025-01-06 是星期一
        dt = datetime(2025, 1, 6)
        self.assertEqual(get_next_weekday(dt), dt)

    def test_friday_returns_same(self):
        # 2025-01-10 是星期五
        dt = datetime(2025, 1, 10)
        self.assertEqual(get_next_weekday(dt), dt)

    def test_saturday_returns_monday(self):
        # 2025-01-11 是星期六 → 2025-01-13 星期一
        dt = datetime(2025, 1, 11)
        result = get_next_weekday(dt)
        self.assertEqual(result, datetime(2025, 1, 13))

    def test_sunday_returns_monday(self):
        # 2025-01-12 是星期日 → 2025-01-13 星期一
        dt = datetime(2025, 1, 12)
        result = get_next_weekday(dt)
        self.assertEqual(result, datetime(2025, 1, 13))

    def test_string_input(self):
        result = get_next_weekday("2025-01-11")  # 星期六
        self.assertEqual(result, datetime(2025, 1, 13))

    def test_string_weekday(self):
        result = get_next_weekday("2025-01-06")  # 星期一
        self.assertEqual(result, datetime(2025, 1, 6))


class TestSaveOutput(unittest.TestCase):
    def test_no_save_path(self):
        df = pd.DataFrame({"a": [1, 2]})
        # 不應報錯
        save_output(df, "test")

    @patch.object(pd.DataFrame, "to_csv")
    def test_saves_when_path_given(self, mock_csv):
        df = pd.DataFrame({"a": [1]})
        save_output(df, "tag", save_path="/tmp/test.csv")
        mock_csv.assert_called_once_with("/tmp/test.csv")


class TestDecorateAllMethods(unittest.TestCase):
    def test_decorates(self):
        call_log = []

        def logger(func):
            def wrapper(*args, **kwargs):
                call_log.append(func.__name__)
                return func(*args, **kwargs)
            return wrapper

        @decorate_all_methods(logger)
        class MyClass:
            def foo(self):
                return 1

            def bar(self):
                return 2

        obj = MyClass()
        obj.foo()
        obj.bar()
        self.assertEqual(call_log, ["foo", "bar"])


if __name__ == "__main__":
    unittest.main()
