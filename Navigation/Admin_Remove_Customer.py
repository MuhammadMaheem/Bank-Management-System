import streamlit as st
from components.load_customers import load_customers
from Customer.customer import Customer
import os

st.title("❌ Remove Customer")
customers = load_customers()
customer_id = st.text_input("Enter Customer ID to remove")

if st.button("Remove Customer"):
    if customer_id in customers:
        del customers[customer_id]

        # Update customer.txt
        with open("data/customer.txt", "w") as f:
            for cust in customers.values():
                f.write(f"{cust.ID},{cust.name},{cust.address},{cust.phone}\n")

        # Remove from user.txt
        try:
            with open("data/user.txt", "r") as f:
                lines = f.readlines()
            with open("data/user.txt", "w") as f:
                for line in lines:
                    if not line.startswith(customer_id + ","):
                        f.write(line)
        except FileNotFoundError:
            st.warning("⚠️ data/user.txt not found.")

        # Remove from accounts.txt
        try:
            with open("data/accounts.txt", "r") as f:
                lines = f.readlines()
            with open("data/accounts.txt", "w") as f:
                for line in lines:
                    if not line.startswith(customer_id + ","):
                        f.write(line)
        except FileNotFoundError:
            st.warning("⚠️ data/accounts.txt not found.")

        # Remove from transaction.txt
        try:
            with open("data/transaction.txt", "r") as f:
                lines = f.readlines()
            with open("data/transaction.txt", "w") as f:
                for line in lines:
                    if not line.startswith(customer_id + ","):
                        f.write(line)
        except FileNotFoundError:
            st.warning("⚠️ data/transaction.txt not found.")

        st.success(f"✅ Customer {customer_id} deleted.")
    else:
        st.error("❌ Customer not found.")
