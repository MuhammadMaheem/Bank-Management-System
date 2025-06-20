import streamlit as st
from components.load_customers import load_customers

st.title("🏧 Withdraw")
customers = load_customers()
userID = st.session_state.get("user")
customer = customers.get(userID)

if customer:
    account_number = st.text_input("Account Number")
    amount = st.number_input("Amount", min_value=0.0)
    if st.button("Withdraw"):
        customer.withdraw(account_number, amount)
        st.success("✅ Withdrawn successfully.")
else:
    st.error("Customer not found.")
