import requests, datetime, json, logging, os, csv
import pandas as pd
import src.utils as utils
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent

views_logger = logging.getLogger("views")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "views.log"), "w")
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
file_handler.setFormatter(file_formatter)
views_logger.addHandler(file_handler)
views_logger.addHandler(console_handler)
views_logger.setLevel(logging.DEBUG)

def cards_collector(data: dict) -> dict:
    cards_data = {}
    result = []
    def get_last_digits(operation):
        return type(operation.get('Номер карты')) is str

    filtered_data = filter(get_last_digits, data)

    for line in filtered_data:
        if cards_data.get(line.get('Номер карты')) is None:
            cards_data[line.get('Номер карты')] = {'last_digits':line.get('Номер карты')[1:], 'total_spent': 0.0 , 'cashback': 0}
        if float(line.get('Сумма операции')) < 0:
            cards_data[line.get('Номер карты')]['total_spent'] += abs(float(line.get('Сумма операции')))
        if line.get('Кэшбэк') > 0:
            views_logger.debug(f"cashback: {line.get('Кэшбэк')}")
            cards_data[line.get('Номер карты')]['cashback'] += abs(int(line.get('Кэшбэк')))

    for card in cards_data.values():
        card['total_spent'] = round(card.get('total_spent'), 2)
        card['cashback'] = int(card.get('cashback') // 100)
        result.append(card)

    return result


def top_transactions(data: dict) -> list:
    sorted_transactions = sorted(data, key=lambda operation: (operation.get('Сумма платежа'), datetime.datetime.strptime(operation.get('Дата операции'), '%d.%m.%Y %H:%M:%S')), reverse=True)
    top_transactions = sorted_transactions[:5]
    return top_transactions


def currency_rates(currency_list) -> dict:
    return utils.get_currency_rates(currency_list)



################
def main_page(date: datetime) -> json:
    greeting = ""
    if 4 > date.hour < 10:
        greeting = "Доброе утро"
    elif 10 >= date.hour < 17:
        greeting = "Добрый день"
    elif 17 >= date.hour < 23:
        greeting = "Добрый вечер"
    elif 23 >= date.hour < 24 or 0 < date.hour < 4:
        greeting = "Доброй ночи"

    month_start = datetime.datetime(date.year, date.month, 1)
    month_start_string = month_start.strftime("%Y-%m-%d")

    data = utils.excel_reader(os.path.join(ROOT_DIR, "data", "operations.xlsx"))

    filtered_data = []

    for line in data:
        if date >= datetime.datetime.strptime(line.get('Дата операции'), '%d.%m.%Y %H:%M:%S') >= month_start:
            filtered_data.append(line)

    with open(os.path.join(ROOT_DIR, "user_settings.json")) as json_file:
        user_settings = json.load(json_file)


    result = {
        "greeting": greeting,
        "cards": cards_collector(filtered_data),
        "top_transactions": top_transactions(filtered_data),
        "currency_rates": utils.get_currency_rates(user_settings.get('user_currencies')),
        "stock_prices": utils.get_stock_prices(user_settings.get('user_stocks'))
    }

    print(json.dumps(result))

    return result

if __name__ == "__main__":
    date = datetime.datetime.strptime("28.12.2021 00:00:00", "%d.%m.%Y %H:%M:%S")
    main_page(date)


#формат вывода данных неправильный (убрать лишние поля)
#переписать входные данные для теста
