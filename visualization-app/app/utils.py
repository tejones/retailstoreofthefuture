def find_customer(customer_id, customers):
    customer_id = int(customer_id)
    if len(customers) >= customer_id and int(customers[customer_id - 1].customer_id) == customer_id:
        return customers[customer_id - 1]
    for customer in customers:
        if customer_id == customer.customer_id:
            return customer
    return None
