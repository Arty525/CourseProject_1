import datetime
import logging
import os
from collections.abc import Callable
from pathlib import Path
from typing import Optional

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent

reports_logger = logging.getLogger("reports")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "reports.log"), "w")
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
file_handler.setFormatter(file_formatter)
reports_logger.addHandler(file_handler)
reports_logger.addHandler(console_handler)
reports_logger.setLevel(logging.DEBUG)


def report(filename: str = "report.csv"):
    """
    :param filename: имя файла с отчетом
    Декоратор записывает в файл результат работы функции
    """

    def decorator(func: Callable) -> object:
        def wrapper(*args: str, **kwargs: int) -> object:
            # попытка выполнения декорируемой функции
            result = func(*args, **kwargs)
            reports_logger.info("Основная функция выполнена успешно")
            with open(os.path.join(ROOT_DIR, "data", filename), "w", newline="") as file:
                result.to_csv(file, sep=" ", index=False, encoding="utf-8")
                reports_logger.info(f"Отчет сохранен в файле {ROOT_DIR}\\data\\{filename}")
                print(f"Отчет сохранен в файле {ROOT_DIR}\\data\\{filename}")
            return result

        return wrapper

    return decorator


@report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    :param transactions: DataFrame с банковскими операциями
    :param category: Категория операций по которой нужно выполнить поиск
    :param date: Дата до которой выводятся траты за полседние 3 месяца
    Функция возвращает список трат по заданной категории в заданном периоде
    """
    reports_logger.debug(transactions)
    if date is None:
        date = datetime.date.today()
    else:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
    second_date = date - datetime.timedelta(days=90)
    transactions = transactions.loc[:, ["Категория", "Дата операции", "Сумма операции"]]
    reports_logger.info("выполняется фильтрация значений по дате и категории")
    try:
        result = transactions.loc[
            (transactions["Категория"] == category)
            & (pd.to_datetime(transactions["Дата операции"], dayfirst=True) >= second_date)
            & (pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= date)
            & (transactions["Сумма операции"] < 0)
        ]
    except Exception:
        reports_logger.warning(Exception)
        raise Exception
    reports_logger.debug(result)
    reports_logger.info("фильтрация выполнена успешно")
    return result
