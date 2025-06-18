import random
import time
import streamlit as st

class Account:
    def __init__(self, balance):
        self._balance = balance
        self.account_number = random.randint(10000, 99999)

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_bal):
        self._balance = new_bal

    def __repr__(self):
        return f"Account(number={self.account_number}, balance={self._balance})"

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            deposit_details = (f"Deposited ${amount}, Updated balance is: {self._balance}", time.asctime())
            print(deposit_details)
        else:
            print("Enter Valid amount")

    def withdraw(self, amount):
        if amount > 0:
            if self._balance > 0:
                self._balance -= amount
                print(f"Withdrawn ${amount}. Remaining Balance: {self._balance}")
            else:
                print("Insufficent Balance")
        else:
            print("Enter Valid amount")
    @classmethod
    def create_account(cls, balance):
        return cls(balance)

    @staticmethod
    def validate_account_number(account_number):
        return 10000 <= account_number <= 99999
