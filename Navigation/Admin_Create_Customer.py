import streamlit as st
from Customer.customer import Customer
from components.load_customers import load_customers, save_customers

st.title("🧑 Create New Customer")
name = st.text_input("Name")
address = st.text_input("Address")
phone = st.text_input("Phone")

customers = load_customers()

if st.button("Create Customer"):
    customer = Customer(name, address, phone)
    customers[customer.ID] = customer
    customer.save_customer()
    st.success(f"✅ Customer created: ID {customer.ID}")
