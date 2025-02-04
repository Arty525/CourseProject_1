import datetime
import json
import logging
import os
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent

services_logger = logging.getLogger("services")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "services.log"), "w")
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
file_handler.setFormatter(file_formatter)
services_logger.addHandler(file_handler)
services_logger.addHandler(console_handler)
services_logger.setLevel(logging.DEBUG)


def cashback_category(data: pd.DataFrame, year: datetime.datetime, month: datetime.datetime) -> json:
    """
    :param data: DataFrame с банковскими операциями
    :param year: Год за который выводятся категории кэшбэка
    :param month: Месяц за который выводятся категории кэшбэка
    Функция возвращает JSON с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года.
    """
    categories = {}
    data = data.to_dict("records")
    for operation in data:
        date = datetime.datetime.strptime(operation.get("Дата операции"), "%d.%m.%Y %H:%M:%S")
        if date.month == month and date.year == year:
            if categories.get(operation.get("Категория")) is None:
                if operation.get("Кэшбэк") is not None and operation.get("Кэшбэк") > 0:
                    categories[operation.get("Категория")] = int(operation.get("Кэшбэк"))
            else:
                if operation.get("Кэшбэк") is not None and operation.get("Кэшбэк") > 0:
                    categories[operation.get("Категория")] += int(operation.get("Кэшбэк"))

    categories = sorted(categories.items(), key=lambda item: item[1], reverse=True)
    services_logger.debug("Список отсортирован по убыванию кэшбэка")
    result = {}
    for category in categories:
        result[category[0]] = category[1]

    services_logger.info("Функция выполнена успешно")
    return json.dumps(result)
