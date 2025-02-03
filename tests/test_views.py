import json

import pytest
import src.views as views
import src.utils as utils
import datetime
import requests
from unittest.mock import patch, Mock


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            [
                {"Номер карты": "*1234", "Сумма операции": "-500", "Кэшбэк": 70},
                {"Номер карты": "*5533", "Сумма операции": "500"},
                {"Номер карты": "*1234", "Сумма операции": "-100", "Кэшбэк": 20},
                {"Номер карты": "*5533", "Сумма операции": "720", "Кэшбэк": 10},
                {"Номер карты": "*6251", "Сумма операции": "-700", "Кэшбэк": 150},
                {"Номер карты": "*1234", "Сумма операции": " 200", "Кэшбэк": 70},
                {"Номер карты": "*6251", "Сумма операции": "-1000"},
                {"Номер карты": "*1234", "Сумма операции": "-30", "Кэшбэк": 70},
            ],
            [
                {"last_digits": "1234", "total_spent": 630.0, "cashback": 2},
                {"last_digits": "5533", "total_spent": 0.0, "cashback": 0},
                {"last_digits": "6251", "total_spent": 1700.0, "cashback": 1},
            ]
        )
    ],
)


def test_cards_collector(value: list, expected: list) -> None:
    assert views.cards_collector(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            [
                {"Дата операции": "01.02.2020 15:02:12", "Сумма операции": "-500", "Категория": "Переводы", "Описание": "Дмитрий Ш."},
                {"Дата операции": "01.01.2019 15:02:12", "Сумма операции": "500", "Категория": "Переводы", "Описание": "Василий П."},
                {"Дата операции": "21.12.2024 15:02:12", "Сумма операции": "-1500", "Категория": "Супермаркеты", "Описание": "Пятерочка"},
                {"Дата операции": "21.12.2020 15:02:12", "Сумма операции": "-500", "Категория": "Фастфуд", "Описание": "Вкусно и точка"},
                {"Дата операции": "21.12.2024 15:02:12", "Сумма операции": "-500", "Категория": "Развлечения", "Описание": "Steam"},
                {"Дата операции": "10.03.2022 15:02:12", "Сумма операции": "-2500", "Категория": "Заправки", "Описание": "Роснефть №152"},
                {"Дата операции": "24.02.2022 15:02:12", "Сумма операции": "-500", "Категория": "Переводы", "Описание": "Ирина Л."},
                {"Дата операции": "25.02.2024 15:02:12", "Сумма операции": "600", "Категория": "Переводы", "Описание": "Петр Р."},
            ],
            [
                    {"amount": "600", "category": "Переводы", "date": "25.02.2024", "description": "Петр Р."},
                    {"amount": "500", "category": "Переводы", "date": "01.01.2019", "description": "Василий П."},
                    {"amount": "-500", "category": "Развлечения", "date": "21.12.2024", "description": "Steam"},
                    {"amount": "-500", "category": "Переводы", "date": "24.02.2022", "description": "Ирина Л."},
                    {"amount": "-500", "category": "Фастфуд", "date": "21.12.2020", "description": "Вкусно и точка"}
            ]
        )
    ],
)

def test_top_transactions(value: list, expected: list) -> None:
    assert views.top_transactions(value) == expected


def test_main_page():
    date = datetime.datetime.strptime("28.12.2021 00:00:00", "%d.%m.%Y %H:%M:%S")
    utils.get_currency_rates = Mock(return_value=[{"currency" : "EUR", "rate" : 102.55},
        {"currency" : "USD", "rate" : 97.31}])
    utils.get_stock_prices = Mock(return_value=[
        {"price" : 23388.0, "stock" : "AAPL"},
        {"price" : 23782.0, "stock" : "AMZN"},
        {"price" : 20400.0, "stock" : "GOOGL"},
        {"price" : 41625.0, "stock" : "MSFT"},
        {"price" : 40483.0, "stock" : "TSLA"}
    ])
    assert json.loads(views.main_page(date)) == {'cards': [{'cashback': 0, 'last_digits': '5091', 'total_spent': 14034.37},
           {'cashback': 0, 'last_digits': '7197', 'total_spent': 20427.45},
           {'cashback': 0, 'last_digits': '4556', 'total_spent': 952.9}],
 'currency_rates': [{'currency': 'EUR', 'rate': 102.55},
                    {'currency': 'USD', 'rate': 97.31}],
 'greeting': 'Доброе утро',
 'stock_prices': [{'price': 23388.0, 'stock': 'AAPL'},
                  {'price': 23782.0, 'stock': 'AMZN'},
                  {'price': 20400.0, 'stock': 'GOOGL'},
                  {'price': 41625.0, 'stock': 'MSFT'},
                  {'price': 40483.0, 'stock': 'TSLA'}],
 'top_transactions': [{'amount': 28001.94,
                       'category': 'Переводы',
                       'date': '22.12.2021',
                       'description': 'Перевод Кредитная карта. ТП 10.2 RUR'},
                      {'amount': 20000.0,
                       'category': 'Другое',
                       'date': '23.12.2021',
                       'description': 'Иван С.'},
                      {'amount': 3500.0,
                       'category': 'Пополнения',
                       'date': '05.12.2021',
                       'description': 'Внесение наличных через банкомат '
                                      'Тинькофф'},
                      {'amount': 1721.38,
                       'category': 'Каршеринг',
                       'date': '12.12.2021',
                       'description': 'Ситидрайв'},
                      {'amount': 1198.23,
                       'category': 'Переводы',
                       'date': '21.12.2021',
                       'description': 'Перевод Кредитная карта. ТП 10.2 RUR'}]}
