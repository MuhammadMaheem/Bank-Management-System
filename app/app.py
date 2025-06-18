import sys
import os
import streamlit as st
from verification import verification
from customer import Customer
from createadmin import Admin
from pin import updating_pin
from account import Account
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Load customers
def load_customers():
    customers = Customer.load_customer(Customer)
    for c in customers.values():
        c.load_accounts()
    return customers

def save_customers(customers):
    for customer in customers.values():
        customer.save_customer()

# Admin Dashboard
def admin_dashboard(userID):
    st.title(f"Admin Dashboard — Logged in as: {userID}")

    menu = [
        "Create Admin", "Create Customer", "View Customer Details",
        "Remove Customer", "Add Account", "Remove Account",
        "Total Balance","Update Password", "Logout"
    ]
    choice = st.sidebar.selectbox("Select an action", menu)
    customers = load_customers()

    if choice == "Create Admin":
        st.header("Create New Admin")
        name = st.text_input("Name")
        address = st.text_input("Address")
        phone = st.text_input("Phone")
        pin = st.text_input("PIN (4 digit)", type="password")
        if st.button("Create Admin"):
            if len(pin) != 4 or not pin.isdigit():
                st.error("PIN must be exactly 4 digits.")
            else:
                admin = Admin(name, address, phone, pin)
                admin.Create_new_admin()
                st.success("New admin created successfully.")

    elif choice == "Create Customer":
        st.header("Create New Customer")
        name = st.text_input("Name")
        address = st.text_input("Address")
        phone = st.text_input("Phone")
        if st.button("Create Customer"):
            customer = Customer(name, address, phone)
            customers[customer.ID] = customer
            customer.save_customer()
            st.success(f"Customer created with ID: {customer.ID}")

    elif choice == "View Customer Details":
        st.header("View Customer Details")
        customer_id = st.text_input("Enter Customer ID")
        if st.button("Show Details"):
            customer = customers.get(customer_id)
            if not customer:
                st.error("Customer not found.")
            else:
                st.write(customer)
                accounts = customer.accounts
                st.write(f"Accounts: {accounts if accounts else 'No accounts found.'}")
                transactions = []
                if os.path.exists("data/transaction.txt"):
                    with open("data/transaction.txt", "r") as file:
                        for line in file:
                            data = line.strip().split(',')
                            if data[0] == customer_id:
                                transactions.append({
                                    "Account": data[1],
                                    "Action": data[2],
                                    "Amount": data[3],
                                    "Timestamp": data[4]
                                })
                if transactions:
                    st.table(transactions)
                else:
                    st.info("No transactions found for this customer.")

    elif choice == "Remove Customer":
        st.header("Remove Customer")
        customer_id = st.text_input("Customer ID to Remove")

        if st.button("Remove Customer"):
            # Load customers
            temp_customer = Customer("dummy", "dummy", "0000")
            customers = temp_customer.load_customer()

            if customer_id in customers:
                # Remove from the in-memory dictionary
                del customers[customer_id]

                # 1. Update data/customer.txt
                try:
                    with open("data/customer.txt", "w") as f:
                        for cust in customers.values():
                            f.write(f"{cust.ID},{cust.name},{cust.address},{cust.phone}\n")
                except FileNotFoundError:
                    st.warning("⚠️ data/customer.txt not found.")

                # 2. Update data/user.txt (if it stores customer credentials)
                try:
                    with open("data/user.txt", "r") as f:
                        lines = f.readlines()
                    with open("data/user.txt", "w") as f:
                        for line in lines:
                            if not line.startswith(customer_id + ","):
                                f.write(line)
                except FileNotFoundError:
                    st.warning("⚠️ data/user.txt not found.")

                # 3. Update data/accounts.txt
                try:
                    with open("data/accounts.txt", "r") as f:
                        lines = f.readlines()
                    with open("data/accounts.txt", "w") as f:
                        for line in lines:
                            if not line.startswith(customer_id + ","):
                                f.write(line)
                except FileNotFoundError:
                    st.warning("⚠️ data/accounts.txt not found.")

                # 4. Update data/transaction.txt
                try:
                    with open("data/transaction.txt", "r") as f:
                        lines = f.readlines()
                    with open("data/transaction.txt", "w") as f:
                        for line in lines:
                            if not line.startswith(customer_id + ","):
                                f.write(line)
                except FileNotFoundError:
                    st.warning("⚠️ data/transaction.txt not found.")

                st.success(f"✅ Customer {customer_id} removed from all records.")
            else:
                st.error("❌ Customer not found.")


    elif choice == "Add Account":
        st.header("Add Account to Customer")
        customer_id = st.text_input("Customer ID")
        account_number = st.text_input("New Account Number")
        
        if st.button("Add Account"):
            customer = customers.get(customer_id)

            if not customer:
                st.error("Customer not found.")
            elif not account_number:
                st.error("Account number required.")
            else:
                try:
                    acc_num = int(account_number)
                    success, msg = customer.add_account_with_number(acc_num)
                    if success:
                        st.success(msg)
                    else:
                        st.warning(msg)
                except ValueError:
                    st.error("❌ Invalid account number format.")




    elif choice == "Remove Account":
        temp_customer = Customer("dummy", "dummy", "0000")  # Adjust constructor params as needed
        st.header("Remove Account")

        customer_id = st.text_input("Customer ID")
        account_number = st.text_input("Account Number")

        if st.button("Remove Account"):
            # Load all customers from file
            customers = temp_customer.load_customer()

            # Strip inputs to avoid whitespace issues
            customer_id = customer_id.strip()
            account_number = account_number.strip()

            # Validate inputs
            if not customer_id:
                st.error("❌ Please enter Customer ID.")
                st.stop()
            if not account_number:
                st.error("❌ Please enter Account Number.")
                st.stop()

            # Check if customer exists
            customer = customers.get(customer_id)
            if not customer:
                st.error("❌ Customer not found.")
                st.stop()

            # Check if account number is a valid integer
            try:
                acc_num_int = int(account_number)
            except ValueError:
                st.error("❌ Account Number must be a valid integer.")
                st.stop()

            # Check if the account exists for this customer
            if not any(acc.account_number == acc_num_int for acc in customer.accounts):
                st.error("❌ Account not found.")
                st.stop()

            # Remove the account
            customer.remove_account(acc_num_int)
            st.success(f"✅ Account {account_number} removed successfully.")
    elif choice == "Total Balance":
        st.header("Total Balance Overview (Admin)")
        customer_id = st.text_input("Enter Customer ID")

        if st.button("Show Balance"):
            customer = customers.get(customer_id)  # Get customer from loaded dict

            if not customer:
                st.error("Customer not found.")
            else:
                st.subheader(f"Customer: {customer.name} (ID: {customer.ID})")

                # Number of accounts
                total_accounts = customer.number_of_accounts(customer_id)
                st.write("📁 Total Number of Accounts:", total_accounts)

                # Total balance
                total_balance = customer.calculate_balance_from_accounts()
                st.write(f"💰 Total Balance: {total_balance}")

                df = customer.get_balance_over_time()
                if not df.empty:
                    st.line_chart(df)  # df already indexed by datetime, with accounts as columns
                else:
                    st.info("No transaction history found.")

                if not customer:
                    st.error("Customer not found.")
                else:
                    accounts = customer.accounts
                    st.write(f"Accounts: {accounts if accounts else 'No accounts found.'}")
                    transactions = []
                    if os.path.exists("data/transaction.txt"):
                        with open("data/transaction.txt", "r") as file:
                            for line in file:
                                data = line.strip().split(',')
                                if len(data) == 6 and data[0] == userID:
                                    transactions.append({
                                        "Account": data[1],          # Account Number
                                        "Balance": data[2],          # Balance after transaction
                                        "Action": data[3],           # Deposit or Withdraw
                                        "Amount": data[4],           # Transaction amount
                                        "Timestamp": data[5]
                                    })

    elif choice == "Update Password":
        old_Password = st.text_input("Old Password", type="password")
        new_Password = st.text_input("New Password", type="password")
        if st.button("Update Password"):
            success1 = updating_pin("data/admin.txt", userID, old_Password, new_Password)
            if success1:
                st.success("Password updated successfully.")
            else:
                st.error("Incorrect ID or PIN.")

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()

# User Dashboard
def user_dashboard(userID):
    st.title(f"User Dashboard — Logged in as: {userID}")

    menu = ["Deposit", "Withdraw", "Total Balance", "Update PIN", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    customers = load_customers()
    customer = customers.get(userID)

    if not customer:
        st.error("Customer not found.")
        return

    if choice == "Deposit":
        account_number = st.text_input("Account Number")
        amount = st.number_input("Amount", min_value=0.0)
        if st.button("Deposit"):
            customer.deposit(account_number, amount)

    elif choice == "Withdraw":
        account_number = st.text_input("Account Number")
        amount = st.number_input("Amount", min_value=0.0)
        if st.button("Withdraw"):
            customer.withdraw(account_number, amount)

    elif choice == "Total Balance":
        customer = customers.get(userID)
        st.subheader(customer)
        total_accounts = customer.number_of_accounts(userID)
        st.write("Total Number of Accounts:",total_accounts)
        balance = customer.calculate_balance_from_accounts()
        st.write(f"💰 Total Balance: {balance}")
        df = customer.get_balance_over_time()
        if not df.empty:
            st.line_chart(df)  # df already indexed by datetime, with accounts as columns
        else:
            st.info("No transaction history found.")

        if not customer:
            st.error("Customer not found.")
        else:
            accounts = customer.accounts
            st.write(f"Accounts: {accounts if accounts else 'No accounts found.'}")
            transactions = []
            if os.path.exists("data/transaction.txt"):
                with open("data/transaction.txt", "r") as file:
                    for line in file:
                        data = line.strip().split(',')
                        if len(data) == 6 and data[0] == userID:
                            transactions.append({
                                "Account": data[1],          # Account Number
                                "Balance": data[2],          # Balance after transaction
                                "Action": data[3],           # Deposit or Withdraw
                                "Amount": data[4],           # Transaction amount
                                "Timestamp": data[5]
                            })

            if transactions:
                st.table(transactions)
            else:
                st.info("No transactions found for this customer.")


    elif choice == "Update PIN":
        old_pin = st.text_input("Old PIN", type="password")
        new_pin = st.text_input("New PIN", type="password")
        if st.button("Update PIN"):
            success1 = updating_pin("data/user.txt", userID, old_pin, new_pin)
            success2 = updating_pin("data/customer.txt", userID, old_pin, new_pin)
            if success1 or success2:
                st.success("PIN updated successfully.")
            else:
                st.error("Incorrect ID or PIN.")

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()
# Verification function
def verification(username, password, role):
    filename = "data/admin.txt" if role == "admin" else "data/user.txt"
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    stored_username, stored_password = parts
                    if stored_username == username and stored_password == password:
                        return True
    except FileNotFoundError:
        return False
    return False

# Main function with session state
def main():
    st.title("🏦 Bank Management System")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None

    if not st.session_state.logged_in:
        role = st.sidebar.radio("Login as", ("Admin", "User"))
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if verification(username, password, role.lower()):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.session_state.role = role.lower()
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
    else:
        if st.session_state.role == "admin":
            admin_dashboard(st.session_state.user)
        else:
            user_dashboard(st.session_state.user)

if __name__ == "__main__":
    main()
