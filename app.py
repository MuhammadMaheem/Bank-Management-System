import streamlit as st
import os
import sys

# Set page configuration
st.set_page_config(
    page_title="\U0001F3E6 Bank Management System",
    page_icon=":bank:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session setup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

# Authentication Navigation
def login():
    with st.sidebar:
        st.title("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            from components.auth import verification
            role = verification(username, password)

            if role:  # If not None
                st.session_state.logged_in = True
                st.session_state.user = username
                st.session_state.role = role  # Now includes 'admin' or 'user'
                st.success(f"✅ Login successful as {role.capitalize()}")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

def logout():
    st.title("🔓 Logout")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()

# Admin Navigation (linked to actual files)
add_account = st.Page("Navigation/Admin_Add_Account.py", title="Add Account", icon=":material/account_balance:")
create_admin = st.Page("Navigation/Admin_Create_Admin.py", title="Create Admin", icon=":material/admin_panel_settings:")
create_customer = st.Page("Navigation/Admin_Create_Customer.py", title="Create Customer", icon=":material/person_add:")
logout_page = st.Page("Navigation/Admin_Logout.py", title="Logout", icon=":material/logout:")
remove_account = st.Page("Navigation/Admin_Remove_Account.py", title="Remove Account", icon=":material/remove_circle:")
remove_customer = st.Page("Navigation/Admin_Remove_Customer.py", title="Remove Customer", icon=":material/person_remove:")
total_balance = st.Page("Navigation/Admin_Total_Balance.py", title="Total Balance", icon=":material/account_balance_wallet:")
update_password = st.Page("Navigation/Admin_Update_Password.py", title="Update Password", icon=":material/password:")
view_customer = st.Page("Navigation/Admin_View_Customer_Details.py", title="View Customer Details", icon=":material/visibility:")

# User Navigation (linked to actual files)
deposit_page = st.Page("Navigation/User_Deposit.py", title="Deposit", icon=":material/savings:")
withdraw_page = st.Page("Navigation/User_Withdraw.py", title="Withdraw", icon=":material/credit_card:")
total_balance_user = st.Page("Navigation/User_Total_Balance.py", title="Total Balance", icon=":material/account_balance_wallet:")
update_pin_page = st.Page("Navigation/User_Update_PIN.py", title="Update PIN", icon=":material/password:")
logout_func_page = st.Page(logout, title="Logout", icon=":material/logout:")

# Login page
login_page = st.Page(login, title="Login", icon=":material/login:")

# Navigation setup
# Navigation setup
if st.session_state.logged_in:
    if st.session_state.role == "admin":
        pg = st.navigation({
            "🔧 Admin Tools": [
                create_admin,
                create_customer,
                view_customer,
                add_account,
                remove_account,
                remove_customer,
                total_balance,
                update_password
            ],
            "🔓 Account": [logout_page]
        })
    else:
        pg = st.navigation({
            "👤 User Tools": [
                deposit_page,
                withdraw_page,
                total_balance_user,
                update_pin_page
            ],
            "🔓 Account": [logout_func_page]
        })
else:
    pg = st.navigation({
        "🔐 Login": [login_page]
    })


pg.run()
