import argparse
from datetime import datetime
import logging
import os

from config import DATETIME_FORMAT, EXPORT_PATH, GENDER_PREF_FUNCTIONS, AGE_PREF_FUNCTIONS, AGE_YOUNG_MID, AGE_MID_OLD
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
from generators.orders_gen import OrdersGen


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--customers", type=int, help="number of customers")
parser.add_argument("-d", "--departments", type=int, help="number of departments")
parser.add_argument("-p", "--products", type=int, help="number of products")
parser.add_argument("-s", "--stores", type=int, help="number of stores")
parser.add_argument("-v", "--vendors", type=int, help="number of vendors")
parser.add_argument("-C", "--categories", type=int, help="number of categories")
parser.add_argument("--start", type=str, help=f"start date in format: {DATETIME_FORMAT}")
parser.add_argument("--end", type=str, help=f"end date in format: {DATETIME_FORMAT}")
parser.add_argument("--path", type=str, help="path where to generate a files")
parser.add_argument("--verbose", help="verbose", action='store_true')

command_params = parser.parse_args()

customers_nr = command_params.customers or 1000
departments_nr = command_params.departments or 10
products_nr = command_params.products or 1000
stores_nr = command_params.stores or 20
vendors_nr = command_params.vendors or 500
categories_nr = command_params.categories or 1000
start = datetime.strptime(command_params.start or '2010-01-01 09:00:00', DATETIME_FORMAT)
end = datetime.strptime(command_params.end or '2021-01-01 20:00:00', DATETIME_FORMAT)
path = command_params.path or EXPORT_PATH

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO if not command_params.verbose else logging.DEBUG)
logger = logging.getLogger('datagen')

if __name__ == "__main__":
    logger.info("Generating data:")
    logger.info(f"    Customers:   {customers_nr}")
    logger.info(f"    Departments: {departments_nr}")
    logger.info(f"    Products:    {products_nr}")
    logger.info(f"    Stores:      {stores_nr}")
    logger.info(f"    Vendors:     {vendors_nr}")
    logger.info(f"    Categories:  {categories_nr}")
    logger.info(f"to path: {path}")
    logger.info("-" * 30)

    sg = StoresGen(stores_nr)
    stores = sg.generate()

    dg = SimpleGen(departments_nr)
    departments = dg.generate()

    vg = SimpleGen(vendors_nr)
    vendors = vg.generate()
    
    cg = SimpleGen(categories_nr)
    categories = cg.generate()
    
    cg = CustomersGen(customers_nr, stores_nr)
    customers = cg.generate()
    
    pg = ProductsGen(products_nr, departments_nr, vendors_nr, categories_nr)
    products = pg.generate()
    
    ig = InventoryGen(products_nr, stores_nr)
    inventory = ig.generate()
    
    cpg = CustomerPreferencesGen(customers, departments_nr, vendors_nr, categories_nr)
    customer_preferences = cpg.generate()
    
    og = OrdersGen(stores_nr, customer_preferences, products, start, end)
    orders, order_details = og.generate()

    logger.info("-" * 30)
    logger.info("SUMMARY:")
    logger.debug("    Customers: " + str(len(customers)))
    logger.info("    Orders:    " + str(len(orders)))
    logger.info("    Order_details: " + str(len(order_details)))
    logger.debug("    Departments: " + str(len(departments)))
    logger.debug("    Products: " + str(len(products)))
    logger.debug("    Stores: " + str(len(stores)))
    logger.debug("    Vendors: " + str(len(vendors)))
    logger.debug("    Categories: " + str(len(categories)))
    logger.info("    Inventory: " + str(len(inventory)))
    logger.debug("    Customer_preferences: " + str(len(customer_preferences)))
    logger.info("-" * 30)

    PostgresExp.exrpot(
        path,
        Stores=stores,
        Departments=departments,
        Vendors=vendors,
        Categories=categories,
        Customers=customers,
        Products=products,
        Inventory=inventory,
        Orders=orders,
        OrderDetails=order_details
    )
    
    JsonExp.export(
        path,
        filename='customer_preferences.json',
        indent=4,
        CustomerPreferences=customer_preferences
    )

    JsonExp.export(
        path,
        filename='preferences.json',
        indent=4,
        MenPreferences={
            'departments': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['M'], cpg.departments_shuffled),
            'vendors': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['M'], cpg.vendors_shuffled),
            'categories': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['M'], cpg.categories_shuffled)
        },
        WomenPreferences={
            'departments': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['F'], cpg.departments_shuffled),
            'vendors': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['F'], cpg.vendors_shuffled),
            'categories': cpg.reveal_general_preferences(GENDER_PREF_FUNCTIONS['F'], cpg.categories_shuffled)
        },
        Young={
            'departments': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"0-{AGE_YOUNG_MID - 1}"], cpg.departments_shuffled),
            'vendors': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"0-{AGE_YOUNG_MID - 1}"], cpg.vendors_shuffled),
            'categories': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"0-{AGE_YOUNG_MID - 1}"], cpg.categories_shuffled)
        },
        Mid={
            'departments': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}"], cpg.departments_shuffled),
            'vendors': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}"], cpg.vendors_shuffled),
            'categories': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_YOUNG_MID}-{AGE_MID_OLD - 1}"], cpg.categories_shuffled)
        },
        Old={
            'departments': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_MID_OLD}-200"], cpg.departments_shuffled),
            'vendors': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_MID_OLD}-200"], cpg.vendors_shuffled),
            'categories': cpg.reveal_general_preferences(AGE_PREF_FUNCTIONS[f"{AGE_MID_OLD}-200"], cpg.categories_shuffled)
        }
    )

    sum_conv = SummaryCon(orders, order_details, customers, products, vendors_nr, departments_nr, categories_nr)
    vendor_sum, department_sum, category_sum = sum_conv.convert()
    CsvExp.export(path, "vendors.csv", vendor_sum)
    CsvExp.export(path, "departments.csv", department_sum)
    CsvExp.export(path, "categories.csv", category_sum)

    logger.info("All done")
