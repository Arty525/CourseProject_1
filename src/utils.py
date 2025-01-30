import requests, datetime, json, logging, os, csv, re, collections
import pandas as pd
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent

utils_logger = logging.getLogger("utils")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "utils.log"), "w")
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.addHandler(console_handler)
utils_logger.setLevel(logging.DEBUG)


def excel_reader(filepath: str = "") -> Any:
    """
    :param filepath: Путь к файлу формата .xslx
    Функция принимает на вход путь к файлу формата .xlsx и возвращает список словарей
    с данными из файла.
    """
    data = pd.read_excel(filepath).to_dict("records")
    return data


def cards_collector(data: dict) -> dict:
    cards_data = {}
    result = []
    # card_number = ""
    # total_spent = 0.0
    # cashback = 0

    for string in data:
        card_number = ""
        total_spent = 0.0
        cashback = 0
        if string.get('Номер карты') is not None:
            card_number = string.get('Номер карты')[2:]
            utils_logger.debug(f"card_number: {card_number} ")
            if int(string.get('Сумма операции')) < 0:
                total_spent = float(string.get('Сумма операции'))
                utils_logger.debug(f"card_number: {total_spent} ")
            if string.get('Кэшбэк') is not None:
                cashback = float(string.get('Кэшбэк'))
                utils_logger.debug(f"card_number: {cashback} ")

        if cards_data.get(card_number) is None:
            cards_data[card_number] = {"last_digits": card_number, "total_spent": total_spent, "cashback": cashback}
        else:
            cards_data[card_number]["total_spent"] += total_spent
            cards_data[card_number]["cashback"] += cashback

        utils_logger.debug(f"at dict: card_number: {cards_data[card_number]["last_digits"]}, total_spent: {cards_data[card_number]["total_spent"]}, cashback: {cards_data[card_number]["cashback"]} ")

    for card in cards_data:
        cards_data[card]["total_spent"] = abs(cards_data[card]["total_spent"])
        cards_data[card]["cashback"] = int(cards_data[card]["cashback"] // 100)

    return {"cards": cards_data}