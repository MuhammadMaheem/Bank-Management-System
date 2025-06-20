import streamlit as st
from components.load_customers import load_customers
from Customer.customer import Customer

st.title("🗑️ Remove Account")
temp_customer = Customer("dummy", "dummy", "0000")
customers = load_customers()

customer_id = st.text_input("Customer ID")
account_number = st.text_input("Account Number")

if st.button("Remove Account"):
    customer = customers.get(customer_id)

    if not customer:
        st.error("Customer not found.")
    elif not account_number:
        st.error("Account number required.")
    else:
        try:
            acc_num_int = int(account_number)
            if any(acc.account_number == acc_num_int for acc in customer.accounts):
                customer.remove_account(acc_num_int)
                st.success("✅ Account removed.")
            else:
                st.error("Account not found.")
        except ValueError:
            st.error("Account number must be an integer.")
