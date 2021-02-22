from utils.helpers import define_age_range_as_nr


class SummaryCon:
    def __init__(self, orders, order_details, customers, products, number_of_vendors, number_of_departments, number_of_categories):
        self.orders = orders
        self.order_details = order_details
        self.customers = customers
        self.products = products
        self.number_of_vendors = number_of_vendors
        self.number_of_departments = number_of_departments
        self.number_of_categories = number_of_categories

    def convert(self):
        orders_v = []
        orders_d = []
        orders_c = []

        for od in self.order_details:
            order = self.orders[od['orderId'] - 1]
            product = self.products[od['productId'] - 1]
            customer = self.customers[order['customerId'] - 1]

            oindex = order['id'] - 1

            if len(orders_v) < order['id']:
                for o in [orders_v, orders_d, orders_c]:
                    o.append({})

                for i in range(1, self.number_of_vendors + 1):
                    orders_v[oindex][f'vendor{i}'] = 0

                for i in range(1, self.number_of_departments + 1):
                    orders_d[oindex][f'department{i}'] = 0

                for i in range(1, self.number_of_categories + 1):
                    orders_c[oindex][f'category{i}'] = 0

                for o in [orders_v, orders_d, orders_c]:
                    o[oindex]['customerId'] = customer['id']
                    o[oindex]['age'] = customer['age']
                    o[oindex]['age_range'] = define_age_range_as_nr(customer['age'])
                    o[oindex]['gender'] = customer['gender']

            orders_v[oindex][f"vendor{product['productVendor']}"] += od['quantityOrdered']
            orders_d[oindex][f"department{product['departmentCode']}"] += od['quantityOrdered']
            orders_c[oindex][f"category{product['category']}"] += od['quantityOrdered']

        return orders_v, orders_d, orders_c
