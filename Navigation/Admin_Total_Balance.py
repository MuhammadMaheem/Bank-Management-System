import streamlit as st
from components.load_customers import load_customers

st.title("💼 Total Balance Overview")
customers = load_customers()
customer_id = st.text_input("Enter Customer ID")

if st.button("Show Balance"):
    customer = customers.get(customer_id)

    if not customer:
        st.error("Customer not found.")
    else:
        st.subheader(f"Customer: {customer.name} (ID: {customer.ID})")

        total_accounts = customer.number_of_accounts(customer_id)
        st.write("📁 Number of Accounts:", total_accounts)

        total_balance = customer.calculate_balance_from_accounts()
        st.write(f"💰 Total Balance: {total_balance}")

        df = customer.get_balance_over_time()
        if not df.empty:
            st.line_chart(df)
        else:
            st.info("No transaction history.")
