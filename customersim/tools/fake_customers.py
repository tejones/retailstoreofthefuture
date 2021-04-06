import csv
from faker import Faker


fake = Faker()
fake_data_file = 'customer_info.csv'
output_file = 'customers.csv'

customers = []
try:
    with open(fake_data_file, 'rt') as csvfile:
        fake_reader = csv.DictReader(csvfile, delimiter=',')
        # customer_list = [row for row in fake_reader]
        for row in fake_reader:
            row['name'] = fake.name_male() if row['gender'] == 'M' else fake.name_female()
            customers.append(row)
except IOError as e:
    print("Whoops....can't find the fake data file.\nTry generating the fake data file and try again\n")
    exit(0)


with open(output_file, 'w', newline='') as csvfile:
    fieldnames = 'customer_id,name,age_range,marital_status,family_size,no_of_children,income_bracket,gender,mean_discount_used_by_cust,unique_items_bought_by_cust,mean_selling_price_paid_by_cust,mean_quantity_bought_by_cust,total_discount_used_by_cust,total_coupons_used_by_cust,total_price_paid_by_cust,total_quantity_bought_by_cust'.split(sep=',')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(customers)