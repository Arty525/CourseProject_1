import requests, datetime, json, logging, os, csv
import pandas as pd
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent

views_logger = logging.getLogger("utils")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "utils.log"), "w")
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
file_handler.setFormatter(file_formatter)
views_logger.addHandler(file_handler)
views_logger.addHandler(console_handler)
views_logger.setLevel(logging.DEBUG)

def cards_collector(data: dict) -> dict:
    cards_data = {}

    for string in data:
        card_number = ""
        total_spent = 0.0
        cashback = 0
        if string.get('Номер карты') is not None:
            card_number = string.get('Номер карты')[2:]
            views_logger.debug(f"card_number: {card_number} ")
            if int(string.get('Сумма операции')) < 0:
                total_spent = float(string.get('Сумма операции'))
                views_logger.debug(f"card_number: {total_spent} ")
            if string.get('Кэшбэк') is not None:
                cashback = float(string.get('Кэшбэк'))
                views_logger.debug(f"card_number: {cashback} ")

        if cards_data.get(card_number) is None:
            cards_data[card_number] = {"last_digits": card_number, "total_spent": total_spent, "cashback": cashback}
        else:
            cards_data[card_number]["total_spent"] += total_spent
            cards_data[card_number]["cashback"] += cashback

        views_logger.debug(f"at dict: card_number: {cards_data[card_number]["last_digits"]}, total_spent: {cards_data[card_number]["total_spent"]}, cashback: {cards_data[card_number]["cashback"]} ")

    for card in cards_data:
        cards_data[card]["total_spent"] = abs(cards_data[card]["total_spent"])
        cards_data[card]["cashback"] = int(cards_data[card]["cashback"] // 100)
    result = []

    for card in cards_data:
        result.append(cards_data[card])

    return result


def top_transactions(data: dict) -> list:
    sorted_transactions = sorted(data, key=lambda operation: (int(operation.get('Сумма платежа')), datetime.datetime.strptime(operation.get('Дата платежа'), '%d.%m.%Y')), reverse=True)
    top_transactions = sorted_transactions[:5]
    return top_transactions


def currency_rates(currency_list) -> dict:



################
def main_page(date: datetime) -> json:
    greeting_text = ""
    if 4 > date.hour < 10:
        greeting_text = "Доброе утро"
    elif 10 >= date.hour < 17:
        greeting_text = "Добрый день"
    elif 17 >= date.hour < 23:
        greeting_text = "Добрый вечер"
    elif 23 >= date.hour < 24 or 0 < date.hour < 4:
        greeting_text = "Доброй ночи"

    data = excel_reader(os.path.join(ROOT_DIR, "data", "operations.xlsx"))


