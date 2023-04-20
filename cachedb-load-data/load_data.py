import os

import psycopg

print("load_data.py")
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

TABLE_NAMES = [
    'product_info',
    'coupon_info',
    'coupon_product',
    'customer_info'
]

TABLE_COLUMNS_STRING = {
    'product_info': 'product_id, name, category, sizes, vendor, description, buy_price, department',
    'coupon_info': 'coupon_id, coupon_type, department, discount, ' +
                   'how_many_products_required, start_date, end_date, product_mean_price, products_available',
    'coupon_product': 'coupon_id, product_id',
    'customer_info': 'customer_id, gender, age, mean_buy_price, total_coupons_used, mean_discount_received, ' +
                     'unique_products_bought, unique_products_bought_with_coupons, total_items_bought'
}


def generate_insert_statement(table_name, table_columns_string):
    sql = f"INSERT INTO {table_name} ({table_columns_string})"
    columns = table_columns_string.split(',')
    sql += " VALUES ("
    for i in range(len(columns)):
        sql += f"%({columns[i].strip()})s"
        if i < len(columns) - 1:
            sql += ", "
    sql += ")"

    return sql


INSERT_STATEMENTS = {}


def get_insert_statement(table_name):
    if table_name not in INSERT_STATEMENTS:
        INSERT_STATEMENTS[table_name] = generate_insert_statement(table_name, TABLE_COLUMNS_STRING[table_name])
    return INSERT_STATEMENTS[table_name]


def get_connection(db, user, password, host):
    return psycopg.connect(
        dbname=db,
        user=user,
        password=password,
        host=host,
        autocommit=True
    )


def insert_row(cur, table_name, csv_row):
    insert_statement = get_insert_statement(table_name)
    columns = TABLE_COLUMNS_STRING[table_name].split(',')

    # convert the csv row into a json object
    json = {columns[i].strip(): csv_row[i] for i in range(len(columns))}
    # insert a row into the table using json
    cur.execute(insert_statement, json)


def insert_data_from_csv(conn, table_name, csv_file_path):
    print(f"Inserting data from {csv_file_path} into {table_name} table....")
    cur = conn.cursor()
    # open csv file
    with open(csv_file_path, 'r') as csv_file:
        # skip the first line
        csv_file.readline()
        # read it line by line, and insert data into the table, record by record
        for line in csv_file:
            # split the line by comma
            values = line.split(',')
            # remove the last comma
            values[-1] = values[-1].replace('\n', '')
            # insert the data into the table
            print(f"INSERT INTO {table_name} VALUES ({','.join(values)})")
            insert_row(cur, table_name, values)

    cur.close()


if __name__ == '__main__':
    # show current working directory
    print(f"Current working directory: {os.getcwd()}")

    # list all files in the current directory
    print(f"Files in the current directory: {os.listdir()}")

    # connect to the database
    db_connection = get_connection(POSTGRES_DB, POSTGRES_USR, POSTGRES_PW, POSTGRES_HST)
    print("Connection established")

    for table_name in TABLE_NAMES:
        insert_data_from_csv(db_connection, table_name, f'{DATA_PATH}/{table_name}.csv')

    print("Data loaded")
    db_connection.close()
    print("Connection closed")
