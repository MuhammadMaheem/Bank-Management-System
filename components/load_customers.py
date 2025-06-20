from Customer.customer import Customer

def load_customers():
    customers = Customer.load_customer(Customer)
    for c in customers.values():
        c.load_accounts()
    return customers

def save_customers(customers):
    for customer in customers.values():
        customer.save_customer()
