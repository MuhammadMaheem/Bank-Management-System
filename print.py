from account import Account
from customer import Customer
from createadmin import Admin
from pin import updating_pin
class Print:

    @staticmethod
    def print_menu(role, userID):
        dummy_customer = Customer("dummy", "dummy", "000")
        customers = dummy_customer.load_customer()
        for customer in customers.values():
            customer.load_accounts()

        while True:
            print("\n===== Bank Management System =====")

            if role == "admin":
                print("1. Create Admin")
                print("2. Create Customer")
                print("3. Details about Customer")
                print("4. Remove Customer")
                print("5. Add Account")
                print("6. Remove Account")
                print("7. Total Balance")
                print("9. Exit")
            elif role == "user":
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Total Balance")
                print("4. Update Pin")
                print("9. Exit")

            try:
                choice = int(input("Enter Choice: "))
            except ValueError:
                print("❌ Invalid input. Enter a number.")
                continue

            if choice == 9:
                print("🚪 Exiting...")
                break

            if role == "user" and choice not in [1, 2, 3,4, 9]:
                print("❌ You are not authorized to perform this action.")
                continue
            if role == "admin" and choice not in [1, 2, 3, 4, 5, 6,7, 9]:
                print("❌ Invalid admin choice.")
                continue

            if role == "admin":
                if choice == 1:
                    print("Create New Admin")
                    name = input("Enter Name: ")
                    address = input("Enter Address: ")
                    phone = input("Enter Phone: ")
                    pin = input("Enter Pin: ")
                    if pin == "":
                        print("❌ Pin cannot be empty.")
                        return
                    if len(pin) != 4:
                        print("❌ Pin must be 4 digits.")
                        return
                    if not pin.isdigit():
                        print("❌ Pin must be numeric.")
                        return
                    admin = Admin(name, address, phone, pin)
                    admin.Create_new_admin()

                elif choice == 2:
                    name = input("Enter Name: ")
                    address = input("Enter Address: ")
                    phone = input("Enter Phone: ")

                    customer = Customer(name, address, phone)
                    customers[customer.ID] = customer
                    customer.save_customer()

                elif choice == 3:
                    customer_id = input("Enter Customer ID: ")
                    customer = customers.get(customer_id)
                    
                    if customer:
                        # Display customer information
                        print(f"✅ Customer found: {customer}")
                        
                        # Customer ID
                        print(f"Customer ID: {customer.ID}")
                        
                        # Read accounts from data/accounts.txt and count the accounts for the customer
                        accounts = []
                        try:
                            with open("data/accounts.txt", "r") as file:
                                for line in file:
                                    data = line.strip().split(',')
                                    if data[0] == customer_id:  # Match customer ID
                                        account_number = int(data[1])
                                        accounts.append(account_number)
                        except FileNotFoundError:
                            print("❌ Accounts file not found.")
                        
                        # Number of accounts the customer has
                        print(f"Number of accounts: {len(accounts)}")
                        
                        # Displaying account details (account number)
                        print("Accounts:")
                        if accounts:
                            for acc_number in accounts:
                                print(f"  Account Number: {acc_number}")
                        else:
                            print("  ❌ No accounts found.")
                        
                        # Displaying transaction history
                        print("Transaction History:")
                        transactions = []
                        try:
                            with open("data/transaction.txt", "r") as file:
                                for line in file:
                                    data = line.strip().split(',')
                                    if data[0] == customer_id:  # Match customer ID
                                        txn = {
                                            'account_number': data[1],
                                            'action': data[3],
                                            'amount': float(data[4]),
                                            'timestamp': data[5]
                                        }
                                        transactions.append(txn)
                        except FileNotFoundError:
                            print("❌ Transaction file not found.")
                        
                        if transactions:
                            for txn in transactions:
                                print(f"  Account Number: {txn['account_number']}, Action: {txn['action']}, Amount: {txn['amount']}, Timestamp: {txn['timestamp']}")
                        else:
                            print("  ❌ No transactions found.")
                    else:
                        print("❌ Customer not found.")


                elif choice == 4:
                    customer_id = input("Enter Customer ID: ")
                    if customer_id in customers:
                        del customers[customer_id]
                        
                        # Update data/customer.txt
                        with open("data/customer.txt", "w") as file:
                            for cust in customers.values():
                                file.write(f"{cust.ID} {cust.name} {cust.address} {cust.phone} 0000\n")
                        
                        # Update data/accounts.txt (remove accounts of deleted customer)
                        try:
                            with open("data/accounts.txt", "r") as file:
                                lines = file.readlines()
                            with open("data/accounts.txt", "w") as file:
                                for line in lines:
                                    if not line.startswith(customer_id):
                                        file.write(line)
                        except FileNotFoundError:
                            print("⚠️ data/accounts.txt file not found while trying to remove accounts.")

                        # Update data/user.txt (remove login credentials of deleted customer)
                        try:
                            with open("data/user.txt", "r") as file:
                                lines = file.readlines()
                            with open("data/user.txt", "w") as file:
                                for line in lines:
                                    if not line.startswith(customer_id):
                                        file.write(line)
                        except FileNotFoundError:
                            print("⚠️ data/user.txt file not found while trying to remove user.")

                        # Update data/transaction.txt (remove all transactions of deleted customer)
                        try:
                            with open("data/transaction.txt", "r") as file:
                                lines = file.readlines()
                            with open("data/transaction.txt", "w") as file:
                                for line in lines:
                                    if not line.startswith(customer_id):
                                        file.write(line)
                        except FileNotFoundError:
                            print("⚠️ data/transaction.txt file not found while trying to remove transactions.")

                        print("✅ Customer and all related data removed successfully.")
                    else:
                        print("❌ Customer not found.")

                elif choice == 5:
                    customer_id = input("Enter Customer ID: ")
                    customer = customers.get(customer_id)
                    if customer:
                        customer.add_account(0)  # Add an account with 0 balance
                    else:
                        print("❌ Customer not found.")
                elif choice == 6:
                    customer_id = input("Enter Customer ID: ")
                    account_number = int(input("Enter Account Number: "))
                    customer = customers.get(customer_id)
                    if customer:
                        customer.remove_account(account_number)
                    else:
                        print("❌ Customer not found.")
                elif choice == 7:
                    customer_id = input("Enter Customer ID: ")
                    customer = customers.get(customer_id)
                    if customer:
                        balance = customer.calculate_balance_from_transactions()
                        print(f"💰 Total Balance from transactions: {balance}")
                    else:
                        print("❌ Customer not found.")
                        
            if role == "user":
           
                if choice == 1:
                    account_number = int(input("Enter Account Number: "))
                    amount = float(input("Enter Amount to Deposit: "))

                    customer = customers.get(userID)
                    if customer:
                        customer.deposit(account_number, amount)
                    else:
                        print("❌ Customer not found.")


                elif choice == 2:
                    account_number = int(input("Enter Account Number: "))
                    amount = float(input("Enter Amount to Withdraw: "))

                    customer = customers.get(userID)
                    if customer:
                        customer.withdraw(account_number, amount)
                    else:
                        print("❌ Customer not found.")


                elif choice == 3:
                    customer = customers.get(userID)
                    if customer:
                        balance = customer.calculate_balance_from_transactions()
                        print(f"💰 Total Balance from transactions: {balance}")
                    else:
                        print("❌ Customer not found.")
                        
                elif choice== 4:
                    oldPin= str(input("Enter Old Pin:"))
                    newPin= str(input("Enter New Pin:"))
                    userPin = updating_pin("data/user.txt", userID, oldPin, newPin)
                    customerPin = updating_pin("data/customer.txt", userID, oldPin, newPin)

                    if customerPin or userPin:
                        print("✅ PIN updated successfully in:")
                        if customerPin:
                            print("- data/customer.txt")
                        if userPin:
                            print("- data/user.txt")
                    else:
                        print("❌ User ID or Old PIN not found in either file.")
                else:
                    print("❌ Invalid choice.")