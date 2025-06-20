import streamlit as st
import os
from components.load_customers import load_customers

st.title("📊 Total Balance")
userID = st.session_state.get("user")
customers = load_customers()
customer = customers.get(userID)

if customer:
    st.subheader(customer)
    total_accounts = customer.number_of_accounts(userID)
    st.write("Total Accounts:", total_accounts)
    balance = customer.calculate_balance_from_accounts()
    st.write("💰 Total Balance:", balance)

    df = customer.get_balance_over_time()
    if not df.empty:
        st.line_chart(df)
    else:
        st.info("No transaction history chart.")

    # 🔽 Transaction History Table
    transactions = []
    if os.path.exists("data/transaction.txt"):
        with open("data/transaction.txt", "r") as file:
            for line in file:
                data = line.strip().split(',')
                if len(data) == 6 and data[0] == userID:
                    transactions.append({
                        "Account": data[1],
                        "Balance": data[2],
                        "Action": data[3],
                        "Amount": data[4],
                        "Timestamp": data[5]
                    })
    if transactions:
        st.markdown("### 🧾 Transaction History")
        st.table(transactions)
    else:
        st.info("No transactions found for your accounts.")
else:
    st.error("❌ Customer not found.")
