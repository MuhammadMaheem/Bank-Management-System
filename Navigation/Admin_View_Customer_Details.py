import streamlit as st
import os
from components.load_customers import load_customers

st.title("📄 View Customer Details")
customer_id = st.text_input("Customer ID")
customers = load_customers()

if st.button("Show Details"):
    customer = customers.get(customer_id)
    if customer:
        st.write(customer)
        st.write("Accounts:", customer.accounts if customer.accounts else "No accounts.")
        transactions = []
        if os.path.exists("data/transaction.txt"):
            with open("data/transaction.txt", "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    if data[0] == customer_id:
                        transactions.append({
                            "Account": data[1],
                            "Action": data[2],
                            "Amount": data[3],
                            "Timestamp": data[4]
                        })
        if transactions:
            st.table(transactions)
        else:
            st.info("No transactions found.")
    else:
        st.error("Customer not found.")
