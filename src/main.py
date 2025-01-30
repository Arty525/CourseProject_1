import requests, datetime, json, logging, os, csv
import pandas as pd
from pathlib import Path


def main(date: datetime.date):
    pass


if __name__ == '__main__':
    today = datetime.date.today()
    month_start = datetime.date(today.year, today.month, 1)
    today_string = today.strftime("%Y-%m-%d %H:%M:%S")
    month_start_string = month_start.strftime("%Y-%m-%d") #перенести в другую функцию

    main(today)