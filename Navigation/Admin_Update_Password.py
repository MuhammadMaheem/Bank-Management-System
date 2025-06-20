import streamlit as st
from Pin.pin import updating_pin

st.title("🔐 Update Admin Password")
userID = st.session_state.get("user")

old_pin = st.text_input("Old PIN", type="password")
new_pin = st.text_input("New PIN", type="password")

if st.button("Update Password"):
    if updating_pin("data/admin.txt", userID, old_pin, new_pin):
        st.success("Password updated successfully.")
    else:
        st.error("Incorrect old PIN.")
