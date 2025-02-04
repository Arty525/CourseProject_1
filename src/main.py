import datetime
import json
import logging
import os
from pathlib import Path

import src.reports as reports
import src.services as services
import src.utils as utils
import src.views as views

ROOT_DIR = Path(__file__).resolve().parent.parent

main_logger = logging.getLogger("main")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "main.log"), "w")
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
file_handler.setFormatter(file_formatter)
main_logger.addHandler(file_handler)
main_logger.addHandler(console_handler)
main_logger.setLevel(logging.DEBUG)


def main(date: datetime.datetime):
    """
    :param date: текущая дата
    Основная функция программы получающая на вход текущую дату и выполняющая команды пользователя.
    """
    data = utils.excel_reader(os.path.join(ROOT_DIR, "data", "operations.xlsx"))
    main_logger.info("DataFrame с банковскими операциями успешно прочитан")

    print("Доступные команды: main_page, cashback, report")

    main_logger.info("Запрос команды у пользователя")
    user_input = input("Введите команду: ")

    if user_input == "main_page":
        main_logger.info("Выбрана функция views.main_page")
        print(json.loads(views.main_page(date)))

    if user_input == "cashback":
        main_logger.info("Выбрана функция services.cashback")
        print("Введите числом месяц и год за которые необходимо вывести категории выгодного кэшбэка")
        month = int(input("месяц: "))

        year = int(input("год: "))

        print(json.loads(services.cashback_category(data, year, month)))

    if user_input == "report":
        main_logger.info("Выбрана функция reports.spending_by_category")
        print("Введите категорию и дату для получения списка трат за три месяца до указанной даты")

        category = input("Категория: ")

        date = input("Дата: ")

        reports.spending_by_category(data, category, date)


if __name__ == "__main__":
    today = datetime.datetime.today()
    main(today)

    main_logger.info("Программа успешно завершила работу")
