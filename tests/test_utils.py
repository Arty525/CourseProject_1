from unittest.mock import patch, Mock
import src.utils as utils
import requests


@patch("requests.request")
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {
        "base": "RUB",
        "date": "2025-02-02",
        "rates": {
        "EUR": 0.009785,
        "USD": 0.010139
        },
        "success": True,
        "timestamp": 1738482316
    }

    requests.request = mock_get
    assert utils.get_currency_rates(["EUR", "USD"]) == {"EUR": 0.009785, "USD": 0.010139}


@patch("requests.get")
def test_get_stock_prices(mock_get):
    utils.get_currency_rates = Mock(return_value={"USD":100.0})
    mock_get.return_value.json.return_value = {
        'pagination':
            {'limit': 100, 'offset': 0, 'count': 5, 'total': 5},
        'data':
            [
                {'open': 247.97, 'high': 247.97, 'low': 233.45, 'last': 233.88, 'close': 237.59, 'volume': 1516752.0,
                 'date': '2025-01-31T20:00:00+0000', 'symbol': 'AAPL', 'exchange': 'IEXG'},
                {'open': 236.89, 'high': 240.285, 'low': 236.31, 'last': 237.82, 'close': 234.64, 'volume': 817875.0,
                 'date': '2025-01-31T20:00:00+0000', 'symbol': 'AMZN', 'exchange': 'IEXG'},
                {'open': 201.69, 'high': 205.475, 'low': 201.61, 'last': 204.0, 'close': 200.87, 'volume': 924014.0,
                 'date': '2025-01-31T20:00:00+0000', 'symbol': 'GOOGL', 'exchange': 'IEXG'},
                {'open': 419.29, 'high': 420.65, 'low': 415.06, 'last': 416.25, 'close': 414.99, 'volume': 693167.0,
                 'date': '2025-01-31T20:00:00+0000', 'symbol': 'MSFT', 'exchange': 'IEXG'},
                {'open': 399.99, 'high': 419.98, 'low': 397.74, 'last': 404.83, 'close': 400.28, 'volume': 726160.0,
                 'date': '2025-01-31T20:00:00+0000', 'symbol': 'TSLA', 'exchange': 'IEXG'}
            ]
    }
    requests.get = mock_get
    assert utils.get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]) == [
        {'AAPL': 23388.0},
        {'AMZN': 23782.0},
        {'GOOGL': 20400.0},
        {'MSFT': 41625.0},
        {'TSLA': 40483.0}
    ]
