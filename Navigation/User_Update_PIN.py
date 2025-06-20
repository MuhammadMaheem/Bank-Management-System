import streamlit as st
from Pin.pin import updating_pin

st.title("🔐 Update PIN")
userID = st.session_state.get("user")
old_pin = st.text_input("Old PIN", type="password")
new_pin = st.text_input("New PIN", type="password")

if st.button("Update PIN"):
    if updating_pin("data/user.txt", userID, old_pin, new_pin) or updating_pin("data/customer.txt", userID, old_pin, new_pin):
        st.success("PIN updated successfully.")
    else:
        st.error("Incorrect old PIN.")
