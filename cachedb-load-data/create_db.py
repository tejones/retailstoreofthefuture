import os

import psycopg

# get the POSTGRES_USR, POSTGRES_PW, POSTGRES_DBdata from environment variables or use default values
print("create_db.py: Getting environment variables")
POSTGRES_USR = os.getenv('POSTGRES_USR', 'cacheUser')
POSTGRES_PW = os.getenv('POSTGRES_PW', 'cachePass')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'cacheDb')
POSTGRES_HST = os.getenv('POSTGRES_HST', 'localhost')
DATA_PATH = os.getenv('DATA_PATH', 'data')
# print out the values
print(f"POSTGRES_USR: {POSTGRES_USR}")
print(f"POSTGRES_PW: {POSTGRES_PW}")
print(f"POSTGRES_DB: {POSTGRES_DB}")
print(f"POSTGRES_HST: {POSTGRES_HST}")

PRODUCT_INFO_TABLE_DDL = \
    """
CREATE TABLE product_info (
    product_id INT,
    name VARCHAR(256),
    category VARCHAR(50),
    sizes VARCHAR(50),
    vendor VARCHAR(50),
    description VARCHAR(256),
    buy_price REAL,
    department VARCHAR(10),
    PRIMARY KEY (product_id)
);
"""

COUPON_INFO_TABLE_DDL = \
    """
CREATE TABLE coupon_info (
  coupon_id INT,
  coupon_type VARCHAR(16),
  department VARCHAR(10),
  discount INT,
  how_many_products_required INT,
  start_date VARCHAR(10),
  end_date VARCHAR(10),
  product_mean_price REAL,
  products_available INT,
  PRIMARY KEY (coupon_id)
);
"""

COUPON_PRODUCT_TABLE_DDL = \
    """
CREATE TABLE coupon_product (
    coupon_id INT,
    product_id INT,
    FOREIGN KEY (coupon_id) REFERENCES coupon_info(coupon_id),
    FOREIGN KEY (product_id) REFERENCES product_info(product_id)
);
"""

CUSTOMER_INFO_TABLE_DDL = \
    """
CREATE TABLE customer_info (
  customer_id INT,
  gender VARCHAR(1),
  age INT,
  mean_buy_price REAL,
  total_coupons_used INT,
  mean_discount_received REAL,
  unique_products_bought INT,
  unique_products_bought_with_coupons INT,
  total_items_bought INT, 
  PRIMARY KEY (customer_id)
);

"""

LOAD_DATA_SQL = \
    f"""
COPY coupon_info FROM '{DATA_PATH}/coupon_info.csv' DELIMITER ',' CSV HEADER;
COPY product_info FROM '{DATA_PATH}/products.csv' DELIMITER ',' CSV HEADER;
COPY coupon_product FROM '{DATA_PATH}/coupon_product.csv' DELIMITER ',' CSV HEADER;
COPY customer_info FROM '{DATA_PATH}/customer_info.csv' DELIMITER ',' CSV HEADER;
"""


def get_connection(db, user, password, host):
    print(f"Connecting to database: {db}, {user}, {password}, {host}")

    return psycopg.connect(
        dbname=db,
        user=user,
        password=password,
        host=host,
        autocommit=True
    )


def drop_all(conn):
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS "{POSTGRES_DB}"')
    cur.close()


def create_user(conn):
    cur = conn.cursor()
    cur.execute(f'CREATE USER "{POSTGRES_USR}" WITH PASSWORD \'{POSTGRES_PW}\'')
    cur.close()


def create_database(conn):
    cur = conn.cursor()
    cur.execute(f'CREATE DATABASE "{POSTGRES_DB}"')
    cur.close()


def create_tables(conn):
    cur = conn.cursor()
    result = cur.execute(PRODUCT_INFO_TABLE_DDL)
    result = cur.execute(COUPON_INFO_TABLE_DDL)
    result = cur.execute(COUPON_PRODUCT_TABLE_DDL)
    result = cur.execute(CUSTOMER_INFO_TABLE_DDL)
    cur.close()


def load_data(conn):
    cur = conn.cursor()
    cur.execute(LOAD_DATA_SQL)
    cur.close()


if __name__ == '__main__':
    # show current working directory
    print(f"Current working directory: {os.getcwd()}")
    # list all files in the current directory
    print(f"Files in the current directory: {os.listdir()}")

    # connect to the default database
    db_connection = get_connection('postgres', POSTGRES_USR, POSTGRES_PW, POSTGRES_HST)
    print("Connection established")
    drop_all(db_connection)

    create_database(db_connection)
    print("Database created")

    # connect to the database
    db_connection = get_connection(POSTGRES_DB, POSTGRES_USR, POSTGRES_PW, POSTGRES_HST)
    create_tables(db_connection)
    print("Tables created")
