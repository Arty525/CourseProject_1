import requests, datetime, json, logging, os, csv
import pandas as pd
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent





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


