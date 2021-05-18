import argparse
from datetime import datetime, timedelta
import logging
import os
import pprint
import random

from config import DATETIME_FORMAT, EXPORT_PATH, GENDER_PREF_FUNCTIONS, AGE_PREF_FUNCTIONS,\
    AGE_YOUNG_MID, AGE_MID_OLD, DEPARTMENTS, VENDORS, CATEGORIES, CATEGORIES_UNIQUE, DEVELOPMENT
from converters.summary_con import SummaryCon
from exporters.csv_exp import CsvExp
from exporters.postgres_exp import PostgresExp
from exporters.json_exp import JsonExp
from generators.customers_gen import CustomersGen
from generators.inventory_gen import InventoryGen
from generators.products_gen import ProductsGen
from generators.simple_gen import SimpleGen
from generators.stores_gen import StoresGen
from generators.customer_preferences_gen import CustomerPreferencesGen
from generators.coupon_gen import CouponGen
from generators.orders_gen import OrdersGen


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--customers", type=int, help="number of customers")
parser.add_argument("-d", "--departments", type=int, help="number of departments")
parser.add_argument("-p", "--products", type=int, help="number of products")
parser.add_argument("-C", "--coupons", type=int, help="number of coupons")
parser.add_argument("-S", "--start", type=str, help=f"start date")
parser.add_argument("-E", "--end", type=str, help=f"end date")
parser.add_argument("-D", "--days", type=int, help="number of days if end not set")
parser.add_argument("-P", "--path", type=str, help="path where to generate a files")
parser.add_argument("-v", "--verbose", help="verbose", action='store_true')

command_params = parser.parse_args()

customers_nr = command_params.customers or 1000
departments_nr = len(DEPARTMENTS)
products_nr = command_params.products or 3000
vendors_nr = len(VENDORS)
categories_nr = len(CATEGORIES_UNIQUE)
start = datetime.strptime(command_params.start or '2010-01-01 09:00:00', DATETIME_FORMAT)
end = datetime.strptime(command_params.end, DATETIME_FORMAT)\
    if command_params.end else start + timedelta(days=command_params.days or 365)
path = command_params.path or EXPORT_PATH

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO if not command_params.verbose else logging.DEBUG)
logger = logging.getLogger('datagen')

if __name__ == "__main__":
    if DEVELOPMENT:
        random.seed(5793)

    logger.info("Generating data:")
    logger.info(f"    Customers:   {customers_nr}")
    logger.info(f"    Departments: {departments_nr}")
    logger.info(f"    Products:    {products_nr}")
    logger.info(f"    Vendors:     {vendors_nr}")
    logger.info(f"    Categories:  {categories_nr}")
    logger.info(f"to path: {path}")
    logger.info("-" * 30)

    # TODO: departments generator
    # dg = SimpleGen()
    # departments = dg.generate()

    # vg = SimpleGen(vendors_nr)
    # vendors = vg.generate()
    
    # cag = SimpleGen(categories_nr)
    # categories = cag.generate()
    
    cug = CustomersGen(customers_nr)
    customers = cug.generate()
    
    pg = ProductsGen(products_nr)
    products = pg.generate()
    
    ig = InventoryGen(products_nr)
    inventory = ig.generate()
    
    cpg = CustomerPreferencesGen(customers)
    customer_preferences = cpg.generate()

    cog = CouponGen(start, end, products_nr)
    coupons = cog.generate()
    
    og = OrdersGen(customer_preferences, products, coupons, start, end)
    orders, order_details = og.generate()
    
    logger.debug("-" * 30)
    logger.debug("SAMPLES:")
    logger.debug("Customers:")
    logger.debug(pprint.pformat(customers[:5]))
    logger.debug("-" * 10)
    logger.debug("Products:")
    logger.debug(pprint.pformat(products[:5]))
    logger.debug("-" * 10)
    logger.debug("Inventory:")
    logger.debug(pprint.pformat(inventory[:5]))
    logger.debug("-" * 10)
    logger.debug("Preferences:")
    logger.debug(pprint.pformat(customer_preferences[:3]))
    logger.debug("-" * 10)
    logger.debug("Coupons:")
    logger.debug(pprint.pformat(coupons[:5]))
    logger.debug("-" * 10)
    logger.debug("Orders:")
    logger.debug(pprint.pformat(orders[:5]))

    logger.info("-" * 30)
    logger.info("SUMMARY:")
    logger.debug("    Customers: " + str(len(customers)))
    logger.info("    Orders:    " + str(len(orders)))
    logger.info("    Order_details: " + str(len(order_details)))
    logger.debug("    Departments: " + str(departments_nr))   # TODO: change to departments
    logger.debug("    Products: " + str(len(products)))
    logger.debug("    Vendors: " + str(vendors_nr))
    logger.debug("    Categories: " + str(categories_nr))
    logger.info("    Inventory: " + str(len(inventory)))
    logger.debug("    Customer_preferences: " + str(len(customer_preferences)))
    logger.info("-" * 30)

    # PostgresExp.exrpot(
    #     path,
    #     # Departments=departments,
    #     Vendors=vendors,
    #     Categories=categories,
    #     Customers=customers,
    #     Products=products,
    #     Inventory=inventory,
    #     Orders=orders,
    #     OrderDetails=order_details
    # )

    # JsonExp.export(
    #     path,
    #     filename='preferences.json',
    #     indent=4,
    #     MenPreferences={
    #         'departments': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['M'], cpg.departments),
    #         'vendors': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['M'], cpg.vendorsd),
    #         'categories': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['M'], cpg.categories)
    #     },
    #     WomenPreferences={
    #         'departments': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['F'], cpg.departments),
    #         'vendors': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['F'], cpg.vendors),
    #         'categories': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['F'], cpg.categories)
    #     },
    #     Young={
    #         'departments': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"0-{AGE_YOUNG_MID - 1}"], cpg.departments_shuffled),
    #         'vendors': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"0-{AGE_YOUNG_MID - 1}"], cpg.vendors_shuffled),
    #         'categories': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"0-{AGE_YOUNG_MID - 1}"], cpg.categories_shuffled)
    #     },
    #     Mid={
    #         'departments': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}"], cpg.departments_shuffled),
    #         'vendors': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}"], cpg.vendors_shuffled),
    #         'categories': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}"], cpg.categories_shuffled)
    #     },
    #     Old={
    #         'departments': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_MID_OLD}-200"], cpg.departments_shuffled),
    #         'vendors': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_MID_OLD}-200"], cpg.vendors_shuffled),
    #         'categories': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_MID_OLD}-200"], cpg.categories_shuffled)
    #     }
    # )

    # sum_conv = SummaryCon(orders, order_details, customers, products, vendors_nr, departments_nr, categories_nr)
    # vendor_sum, department_sum, category_sum = sum_conv.convert()
    CsvExp.export(path, "customers", customers)
    CsvExp.export(path, "products", products)
    CsvExp.export(path, "inventory", inventory)
    CsvExp.export(path, "orders", orders)
    CsvExp.export(path, "order_details", order_details)

    # prepare coupons data
    coupon_product = []
    for coupon in coupons:
        coupon_product += [{'coupon_id': coupon['id'], 'product_id': p} for p in coupon['products']]
        del(coupon['products'])
    CsvExp.export(path, "coupons", coupons)
    CsvExp.export(path, "coupon_product", coupon_product)

    JsonExp.export(
        path,
        filename='customer_preferences',
        indent=4,
        CustomerPreferences=customer_preferences
    )

    logger.info("All done")
