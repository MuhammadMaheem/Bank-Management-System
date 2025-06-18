# Bank-Management-System
 Bank Management System using OOP (All Pillars),FileHandling and Streamlit

---

## 🧠 Object-Oriented Programming Concepts Used

| OOP Concept     | Usage |
|----------------|-------|
| **Class**       | `Person`, `Admin`, `Customer`, `Account` |
| **Inheritance** | `Admin` and `Customer` inherit from `Person` |
| **Encapsulation** | Private attributes with getters/setters (`__address`, `__phone`) |
| **Polymorphism** | Method overriding (e.g., `__str__`, `__repr__`) |
| **Abstraction**  | Simplified interface for dashboard operations |
| **Static/Class Methods** | Used in `Account` and `Customer` for utility logic |

---

## 🧩 Module Explanations

### 🔹 `app.py` — Main Streamlit Application

#### 📌 `main()`
- Handles session-based login for Admin/User.
- Redirects to appropriate dashboard.

#### 📌 `admin_dashboard(userID)`
Admin options:
- ✅ Create Admin
- ✅ Create Customer
- ✅ View/Remove Customers & Accounts
- ✅ View Total Balance with Line Chart
- ✅ Update Password

#### 📌 `user_dashboard(userID)`
User options:
- 💸 Deposit / Withdraw
- 💼 View Total Balance (with chart)
- 🔑 Update PIN

#### 📌 `verification(username, password, role)`
- Authenticates Admin or User by checking `admin.txt` or `user.txt`.

---

### 🔹 `customer.py` — Customer Class

Inherits from `Person` and manages:
- 📌 `add_account()` / `add_account_with_number()`
- 📌 `deposit()` / `withdraw()`
- 📌 `log_transaction()` — appends transaction details to `transaction.txt`
- 📌 `save_customer()` — stores in `customer.txt` and `user.txt`
- 📌 `load_customer()` / `load_accounts()` — reads from files
- 📌 `remove_account()` — deletes account and related transactions
- 📌 `get_balance_over_time()` — returns line chart data using `pandas`
- 📌 `calculate_balance_from_accounts()` — adds balances
- 📌 `number_of_accounts()` — counts accounts from file

---

### 🔹 `account.py` — Account Class

Defines each customer's account:
- Auto-generates `account_number`
- Stores `balance` with properties
- Methods:
  - 📌 `deposit(amount)`
  - 📌 `withdraw(amount)`
  - 📌 `validate_account_number()` — ensures format
  - 📌 `__repr__()` — for display

---

### 🔹 `person.py` — Abstract Base Class

- Holds basic info: `name`, `address`, `phone`
- Uses `@property` for encapsulated access to `address` and `phone`

---

### 🔹 `createadmin.py` — Admin Class

- Inherits from `Person`
- `Create_new_admin()` stores admin to `admin.txt`

---

### 🔹 `pin.py`

- 📌 `updating_pin(file_path, userID, oldPin, newPin)`
  - Searches and updates the PIN in `user.txt` or `admin.txt`

---

### 🔹 `verification.py`

- Duplicate `verification()` function (used in CLI, kept for backward support)
- Also includes `main_verify()` for CLI login (not used in GUI)

---

## 💾 File-Based Data Storage

| File | Purpose |
|------|---------|
| `data/admin.txt` | Admin credentials: `username,pin` |
| `data/user.txt` | User login credentials |
| `data/customer.txt` | Customer info: `ID, name, address, phone, PIN` |
| `data/accounts.txt` | Account data: `customerID, accountNumber, balance` |
| `data/transaction.txt` | Transaction logs: `customerID, account, balance, action, amount, timestamp` |

---

## 📊 Visual Output (Streamlit)

- Sidebar navigation for all roles
- `st.text_input`, `st.button`, `st.table`, `st.line_chart`
- Admin Dashboard:
  - ✅ Create / Remove customers and accounts
  - 📈 View balance trends
- User Dashboard:
  - 💵 Deposit / Withdraw
  - 📊 Total balance with time-series plot

---

## 🧪 Sample Features

- Auto-generated Customer IDs: `C501`, `C502`, etc.
- Account Numbers: Random 5-digit integers
- Transactions are recorded with balance snapshots
- Full PIN update mechanism


---

## 🚀 Run the App

```bash
pip install streamlit pandas
streamlit run app.py
