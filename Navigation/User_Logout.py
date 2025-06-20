import streamlit as st

st.title("🚪 Logout")
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.success("Successfully logged out.")
    st.rerun()
