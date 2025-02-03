import requests, datetime, json, logging, os, csv, re, collections
import pandas as pd
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from urllib3 import request

load_dotenv(".env")

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
    data = pd.read_excel(filepath).to_dict("records")
    return data


def get_currency_rates(currency_list: list) -> list:
    currencies = ""

    for currency in currency_list:
        currencies += currency + "RUB" + ","

    currencies = currencies[:-1]

    url = f"https://currate.ru/api/?get=rates&pairs={currencies}&key={CURRENCY_RATE_API_KEY}"

    payload = {}
    headers = {
        "apikey": CURRENCY_RATE_API_KEY
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Connection Error. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("Timeout Error. Please check your internet connection.")
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects. Please check your internet connection.")
    except requests.exceptions.HTTPError:
        print("HTTP Error. Please check your internet connection.")
    except requests.exceptions.RequestException:
        print("Something went wrong. Please check your internet connection or try again later.")
    else:

        status_code = response.status_code
        if status_code == 400:
            print('Bad Request')
        if status_code == 401:
            print('Unauthorized')
        if status_code == 404:
            print('Not Found')
        if status_code == 429:
            print('Too many requests')
        if status_code == 500:
            print('Server Error')

        #result = response.json()
        result = response.json().get("data")

        currency_rates = []
        for currency, rate in result.items():
            currency_rates.append({"currency": currency[:-3], "rate": float(rate)})

        return currency_rates


def get_stock_prices(stock_list: list) -> list:
    stocks = ",".join(stock_list)

    url = f"http://api.marketstack.com/v1/intraday/latest?access_key={STOCK_PRICES_API_KEY}"

    querystring = {"symbols":stocks}

    try:
        response = requests.get(url, params=querystring)
    except requests.exceptions.ConnectionError:
        print("Connection Error. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("Timeout Error. Please check your internet connection.")
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects. Please check your internet connection.")
    except requests.exceptions.HTTPError:
        print("HTTP Error. Please check your internet connection.")
    except requests.exceptions.RequestException:
        print("Something went wrong. Please check your internet connection or try again later.")
    else:

        status_code = response.status_code
        if status_code == 400:
            print('Bad Request')
        if status_code == 401:
            print('Unauthorized')
        if status_code == 403:
            print('Forbidden')
        if status_code == 404:
            print('Not Found')
        if status_code == 429:
            print('Too many requests')
        if status_code == 500:
            print('Server Error')

        result = response.json()
        utils_logger.info(f"result: {result}")

        stock_prices = []
        for stock in result.get('data'):
            stock_prices.append({"price" : stock.get('last'), "stock" : stock.get('symbol')})

        usd_rate = get_currency_rates(["USD"]).get("USD")

        for stock in stock_prices:
            stock["price"] *= usd_rate
            stock["price"] = round(stock["price"], 2)

        return stock_prices
