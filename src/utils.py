import logging
import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv("../.env")

CURRENCY_RATE_API_KEY = os.getenv("CURRENCY_RATE_API_KEY")
STOCK_PRICES_API_KEY = os.getenv("STOCK_PRICES_API_KEY")

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
    try:
        data = pd.read_excel(filepath)
    except Exception:
        utils_logger.warning(Exception)
        raise Exception
    utils_logger.info("Функция выполнена успешно")
    return data


def get_currency_rates(currency_list: list) -> list:
    """
    :param currency_list: список валют
    Функция обращается к внешнему API и возвращает курсы валют из списка
    """

    currencies = ""

    for currency in currency_list:
        currencies += currency + "RUB" + ","

    currencies = currencies[:-1]

    url = f"https://currate.ru/api/?get=rates&pairs={currencies}&key={CURRENCY_RATE_API_KEY}"

    payload = {}
    headers = {"apikey": CURRENCY_RATE_API_KEY}

    response = requests.request("GET", url, headers=headers, data=payload)
    status_code = response.status_code
    if status_code == 400:
        utils_logger.warning("Bad Request")
        print("Bad Request")
    if status_code == 401:
        utils_logger.warning("Unauthorized")
        print("Unauthorized")
    if status_code == 404:
        utils_logger.warning("Not Found")
        print("Not Found")
    if status_code == 429:
        utils_logger.warning("Too many requests")
        print("Too many requests")
    if status_code == 500:
        utils_logger.warning("Server Error")
        print("Server Error")

    result = response.json().get("data")

    currency_rates = []
    for currency, rate in result.items():
        currency_rates.append({"currency": currency[:-3], "rate": float(rate)})

    utils_logger.info("Функция выполнена успешно")
    return currency_rates


def get_stock_prices(stock_list: list) -> list:
    """
    :param stock_list: Список акций
    Функция обращается к внешнему API и возвращает курсы акций из списка
    """
    stocks = ",".join(stock_list)

    url = f"http://api.marketstack.com/v1/intraday/latest?access_key={STOCK_PRICES_API_KEY}"

    querystring = {"symbols": stocks}

    response = requests.get(url, params=querystring)

    status_code = response.status_code
    if status_code == 400:
        utils_logger.warning("Bad Request")
        print("Bad Request")
    if status_code == 401:
        utils_logger.warning("Unauthorized")
        print("Unauthorized")
    if status_code == 403:
        utils_logger.warning("Forbidden")
        print("Forbidden")
    if status_code == 404:
        utils_logger.warning("Not Found")
        print("Not Found")
    if status_code == 429:
        utils_logger.warning("Too many requests")
        print("Too many requests")
    if status_code == 500:
        utils_logger.warning("Server Error")
        print("Server Error")

    result = response.json()

    stock_prices = []
    for stock in result.get("data"):
        stock_prices.append({"price": stock.get("last"), "stock": stock.get("symbol")})

    usd_rate = get_currency_rates(["USD"]).get("USD")

    for stock in stock_prices:
        stock["price"] *= usd_rate
        stock["price"] = round(stock["price"], 2)

    utils_logger.info("Функция выполнена успешно")
    return stock_prices
