import os
from pathlib import Path

import pandas as pd
import pytest

import src.reports as reports

ROOT_DIR = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            pd.DataFrame(
                {
                    "Дата операции": [
                        "02.12.2021 14:41:17",
                        "01.12.2021 23:40:34",
                        "01.12.2021 18:50:24",
                        "01.12.2021 13:12:18",
                        "30.11.2021 18:19:28",
                        "29.11.2021 14:40:46",
                        "25.11.2021 20:47:27",
                        "25.11.2021 19:02:06",
                        "09.11.2021 18:45:24",
                        "01.09.2021 18:50:25",
                        "01.09.2021 15:51:42",
                    ],
                    "Категория": [
                        "Продукты",
                        "Переводы",
                        "Продукты",
                        "Переводы",
                        "Продукты",
                        "Переводы",
                        "Продукты",
                        "Переводы",
                        "Продукты",
                        "Переводы",
                        "Продукты",
                    ],
                    "Сумма операции": [-1000, 1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, 1000],
                }
            ),
            pd.DataFrame(
                {
                    "Категория": ["Переводы", "Переводы", "Переводы"],
                    "Дата операции": ["29.11.2021 14:40:46", "25.11.2021 19:02:06", "01.09.2021 18:50:25"],
                    "Сумма операции": [-1000, -1000, -1000],
                }
            ),
        )
    ],
)
def test_spending_by_category(value, expected):
    assert reports.spending_by_category(value, "Переводы", "30.11.2021").to_dict("records") == expected.to_dict(
        "records"
    )


def test_report_decorator() -> None:
    @reports.report(filename="test_decorator.txt")  # type: ignore[operator]
    def func() -> pd.DataFrame:
        return pd.DataFrame({"test"})

    func()
    file = open(os.path.join(ROOT_DIR, "data", "test_decorator.txt"), "r")
    line = file.readlines()
    file.close()
    assert line[-1] == "test\n"
