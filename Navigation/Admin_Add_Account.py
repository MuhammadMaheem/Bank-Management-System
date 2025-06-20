import streamlit as st
from components.load_customers import load_customers

st.title("➕ Add Account to Customer")
customers = load_customers()

customer_id = st.text_input("Customer ID")
account_number = st.text_input("New Account Number")

if st.button("Add Account"):
    customer = customers.get(customer_id)

    if not customer:
        st.error("Customer not found.")
    elif not account_number:
        st.error("Account number required.")
    else:
        try:
            acc_num = int(account_number)
            success, msg = customer.add_account_with_number(acc_num)
            if success:
                st.success(msg)
            else:
                st.warning(msg)
        except ValueError:
            st.error("Invalid account number format.")
