import streamlit as st
from Admin.createadmin import Admin

st.title("👮 Create New Admin")
name = st.text_input("Name")
address = st.text_input("Address")
phone = st.text_input("Phone")
pin = st.text_input("PIN (4 digit)", type="password")

if st.button("Create Admin"):
    if len(pin) != 4 or not pin.isdigit():
        st.error("PIN must be 4 digits.")
    else:
        admin = Admin(name, address, phone, pin)
        admin.Create_new_admin()
        st.success("✅ Admin created.")
