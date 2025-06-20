from Person.person import Person
from Account.account import Account
from datetime import datetime
import pandas as pd
import streamlit as st
import os


class Customer(Person):
    _id_counter = 500

    def __init__(self, name, address, phone):
        super().__init__(name, address, phone)
        self.accounts = []
        self.ID = self.generate_ID()
        self.load_accounts()

    @classmethod
    def generate_ID(cls):
        cls._id_counter += 1
        return f"C{cls._id_counter}"

    def add_account(self, balance=0):
        # Ensure account number is unique
        existing_account_numbers = {acc.account_number for acc in self.accounts}
        while True:
            new_account = Account.create_account(balance)
            if new_account.account_number not in existing_account_numbers:
                self.accounts.append(new_account)
                self.save_accounts()  # Save accounts after adding a new one
                break
    def remove_account(self, account_number):
        # Remove from in-memory list
        self.accounts = [acc for acc in self.accounts if acc.account_number != account_number]
        self.save_accounts()

        # Remove from data/accounts.txt
        try:
            with open("data/accounts.txt", "r") as file:
                lines = file.readlines()
            with open("data/accounts.txt", "w") as file:
                for line in lines:
                    if not line.startswith(f"{self.ID},{account_number}"):
                        file.write(line)
        except FileNotFoundError:
            print("⚠️ data/accounts.txt file not found while trying to remove account.")

        # Remove from data/transaction.txt
        try:
            with open("data/transaction.txt", "r") as file:
                lines = file.readlines()
            with open("data/transaction.txt", "w") as file:
                for line in lines:
                    if not line.startswith(f"{self.ID},{account_number}"):
                        file.write(line)
        except FileNotFoundError:
            print("⚠️ data/transaction.txt file not found while trying to remove transactions.")

        print(f"✅ Account {account_number} and related data removed successfully.")


        

    def save_customer(self):
        # ----- Check if customer ID already exists in data/customer.txt -----
        customer_exists = False
        if os.path.exists("data/customer.txt"):
            with open("data/customer.txt", "r") as file:
                for line in file:
                    fields = line.strip().split(",")
                    if fields and fields[0].strip() == self.ID:
                        customer_exists = True
                        break

        if not customer_exists:
            with open("data/customer.txt", "a") as file:
                file.write(f"{self.ID},{self.name},{self.address},{self.phone},0000\n")
            print(f"✅ Customer {self.name} saved successfully.")
        else:
            print(f"⚠️ Customer ID {self.ID} already exists in data/customer.txt. Skipping save.")

        # ----- Check if user ID already exists in data/user.txt -----
        user_exists = False
        if os.path.exists("data/users.txt"):
            with open("data/users.txt", "r") as file:
                for line in file:
                    fields = line.strip().split(",")
                    if fields and fields[0].strip() == self.ID:
                        user_exists = True
                        break

        if not user_exists:
            with open("data/users.txt", "a") as file:
                file.write(f"{self.ID},0000,user\n")
            print(f"✅ User {self.name} saved successfully.")
        else:
            print(f"⚠️ User ID {self.ID} already exists in data/users.txt. Skipping save.")


    def load_customer(self):
        customers = {}
        try:
            with open("data/customer.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    customer_id = data[0]
                    name = data[1]
                    address = data[2]
                    phone = data[3]

                    customer = Customer(name, address, phone)
                    customer.ID = customer_id

                    # Load accounts for this customer AFTER setting ID
                    customer.accounts = []  # clear existing accounts
                    customer.load_accounts()

                    customers[customer_id] = customer
        except FileNotFoundError:
            print("⚠️ data/customer.txt not found.")
        return customers



    def add_account_with_number(self, account_number, balance=0.0):
        # Check if the account number already exists for this customer
        if any(acc.account_number == account_number for acc in self.accounts):
            return False, "Account number already exists for this customer."

        # Also check globally to ensure uniqueness
        try:
            with open("data/accounts.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        _, acc_num = parts[:2]
                        if int(acc_num) == account_number:
                            return False, "❌ This account number is already used by another customer."
        except FileNotFoundError:
            pass  # Safe to proceed if no file yet

        # Create and add the account
        
        new_acc = Account(balance)
        new_acc.account_number = account_number
        self.accounts.append(new_acc)
        self.log_transaction(account_number,"deposit",amount=0,balance=0)

        self.save_accounts()
        return True, "✅ Account added successfully."




    def save_accounts(self):
        try:
            # Load all accounts from file to dict {(cust_id, acc_number): balance}
            all_accounts = {}
            try:
                with open("data/accounts.txt", "r") as file:
                    for line in file:
                        parts = line.strip().split(',')
                        if len(parts) == 3:
                            cust_id, acc_num, bal = parts
                            all_accounts[(cust_id, int(acc_num))] = float(bal)
            except FileNotFoundError:
                pass

            # Update balances for this customer's accounts
            for acc in self.accounts:
                all_accounts[(self.ID, acc.account_number)] = acc.balance

            # Write all accounts back (overwrite file)
            with open("data/accounts.txt", "w") as file:
                for (cust_id, acc_num), bal in all_accounts.items():
                    file.write(f"{cust_id},{acc_num},{bal}\n")
            print("✅ All accounts saved with updated balances.")


        except Exception as e:
            print(f"❌ Error saving accounts: {e}")

    def load_accounts(self):
        self.accounts = []
        try:
            with open("data/accounts.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        cust_id, acc_number, bal = line.split(",")
                        print(f"Checking account line: {cust_id}, {acc_number}, {bal}")  # debug

                        if cust_id == self.ID:
                            print(f"Matched customer ID: {cust_id}")
                            if not any(acc.account_number == int(acc_number) for acc in self.accounts):
                                acc = Account(float(bal))
                                acc.account_number = int(acc_number)
                                self.accounts.append(acc)
                                print(f"Added account {acc.account_number} with balance {acc.balance}")
                    except ValueError:
                        print(f"Skipping invalid line: {line}")
        except FileNotFoundError:
            print("data/accounts.txt not found")



    def deposit(self, account_number, amount):
        account = next((acc for acc in self.accounts if acc.account_number == int(account_number)), None)

        if account:
            if amount > 0:
                account.deposit(amount)  # Update balance
                self.save_accounts()     # Save account balances to data/accounts.txt
                self.log_transaction(account_number, "Deposit", amount, account.balance)  # Log with updated balance
                st.success(f"Deposited {amount} into {account_number}")
            else:
                st.error("Invalid Amount")
        else:
            st.error("❌ Account not found.")






    def withdraw(self, account_number, amount):
        account = next((acc for acc in self.accounts if acc.account_number == int(account_number)), None)

        if account:
            if amount > 0:
                if account.balance >= amount:
                    account.withdraw(amount)  # Update balance
                    self.save_accounts()
                    updated_balance = account.balance  # Updated balance
                    self.log_transaction(account_number, "Withdraw", amount, account.balance)
                    st.success(f"Withdrew {amount} from {account_number}")
                else:
                    st.error("Insufficient Balance")
            else:
                st.error("Invalid Amount")
        else:
            print("❌ Account not found.")





        

    def log_transaction(self, account_number, action, amount, balance):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("data/transaction.txt", "a") as file:
            file.write(f"{self.ID},{account_number},{balance},{action},{amount},{timestamp}\n")


   # Log the transaction with timestamp
    def calculate_balance_from_transactions(self):
        total_balance = 0.0
        try:
            with open("data/transaction.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) < 6:
                        continue  # Skip invalid lines

                    cust_id = data[0]
                    acc_number = data[1]
                    action = data[3].lower()
                    try:
                        amount = float(data[4])
                    except ValueError:
                        continue  # Skip lines with invalid amount

                    if cust_id == self.ID:
                        if action == "deposit":
                            total_balance += amount
                        elif action == "withdraw":
                            total_balance -= amount
        except FileNotFoundError:
            pass

        return total_balance

    def calculate_balance_from_accounts(self):
        return sum(acc.balance for acc in self.accounts)

    def get_customer_transactions(self):
        transactions = []
        try:
            with open("data/transaction.txt", "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 6:  # Ensure the line has the correct number of elements
                        customer_id, account_number, balance, action, amount, timestamp = data
                        if customer_id == self.ID:
                            transactions.append({
                                'account_number': account_number,
                                'action': action,
                                'amount': float(amount),
                                'timestamp': timestamp
                            })
        except FileNotFoundError:
            print("❌ Transaction file not found.")
        return transactions
   

    def get_balance_over_time(self):
        records = []

        try:
            with open("data/transaction.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) < 6:
                        continue

                    cust_id = data[0]
                    acc_number = data[1]
                    balance_str = data[2]
                    timestamp_str = data[5]

                    if cust_id == self.ID:
                        try:
                            balance = float(balance_str)
                            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                            records.append({
                                "datetime": timestamp,
                                "account": acc_number,
                                "balance": balance
                            })
                        except ValueError:
                            continue

        except FileNotFoundError:
            return pd.DataFrame()

        if not records:
            return pd.DataFrame()

        # Create DataFrame
        df = pd.DataFrame(records)
                                    
        # ✅ Fix: Aggregate by taking the last balance per datetime/account
        df = df.groupby(["datetime", "account"]).agg({"balance": "last"}).reset_index()

        # Pivot the DataFrame so each account becomes a column
        df_pivot = df.pivot(index="datetime", columns="account", values="balance")

        # Sort by datetime
        df_pivot = df_pivot.sort_index()

        return df_pivot



    def number_of_accounts(self,account_num):
        count = 0
        with open("data/accounts.txt","r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) < 2:
                    continue
                cust_id = data[0]
                acc_number = data[1]
                if account_num == cust_id:
                    count+=1
        print(count)
        return count
                                


    def __str__(self):
        return f"Customer(ID={self.ID}, name={self.name}, address={self.address}, phone={self.phone})"

    def __repr__(self):
        return f"Customer(ID={self.ID}, name={self.name}, accounts={len(self.accounts)})"
