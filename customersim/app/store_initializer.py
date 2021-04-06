import csv

from app import logger
from app.config import CUSTOMERS_LIST_FILE, STORE_WIDTH, STORE_HEIGHT
from app.domain_model import Store


def init_store():
    return Store(STORE_WIDTH, STORE_HEIGHT)


def init_customer_list(customer_file_path: str = CUSTOMERS_LIST_FILE):
    try:
        with open(customer_file_path, 'rt') as csvfile:
            fake_reader = csv.DictReader(csvfile, delimiter=',')
            customer_list = [row for row in fake_reader]
    except IOError as e:
        logger.error("Whoops....can't find the fake data file.\nTry generating the fake data file and try again\n")
        exit(0)

    return customer_list
