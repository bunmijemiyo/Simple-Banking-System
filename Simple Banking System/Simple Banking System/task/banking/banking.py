import sqlite3
import random

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()


class BankApp:
    def __init__(self):
        self.pin = "pin"
        self.account_num = "account_num"
        self.balance = 0
        self.my_pin = "my_pin"
        self.my_account = "my_account"
        self.data_bank = {}

    def home_page(self):
        print("1. Create an account\n2. Log into account\n0. Exit")

    def save_card_info(self):
        cur.execute(f"INSERT INTO card (number, pin) VALUES ({self.account_num}, {self.pin});")
        conn.commit()

    def create_account(self):
        password = random.sample(range(10), 4)
        self.pin = "".join((str(num) for num in password))
        account1_ = "400000"
        account2 = random.randint(100000000, 999999999)
        account_num_ = account1_ + str(account2)
        num_sum = [int(num) for num in account_num_]
        num_sum7 = []
        for i, num in enumerate(num_sum):
            if i % 2 != 0:
                num_sum7.append(num)
            else:
                num_sum7.append(num * 2)
        num_sum3 = [num - 9 if num > 9 else num for num in num_sum7]
        num_sum4 = sum(num_sum3)
        count = 0
        while num_sum4 % 10 != 0:
            num_sum4 += 1
            count += 1

        self.account_num = account_num_ + str(count)
        BankApp.save_card_info(self)
        print(f"\nYour card has been created\nYour card number:\n{self.account_num}\nYour card PIN:\n{self.pin}")

    def login_info(self):
        print("\nEnter your card number:")
        self.my_account = input()
        print("Enter your PIN:")
        self.my_pin = input()

    def verify_login(self):
        BankApp.retrieve_data(self)
        if bool(cur.fetchone()) is not False:
            print("\nYou have successfully logged in!")
            while True:
                print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close acccount \n5. Log out\n0. Exit")
                choices = input()
                if choices == "1":
                    BankApp.acc_balance(self)
                elif choices == "5":
                    print("\nYou have successfully logged out!")
                    break
                elif choices == "3":
                    BankApp.transfer(self)
                elif choices == "4":
                    BankApp.close_account(self)
                    break
                elif choices == "2":
                    BankApp.add_money(self)
                elif choices == "0":
                    print("\nBye!")
                    exit()
        else:
            print("\nWrong card number or PIN!")

    def create_table(self):
        cur.execute(
            "CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
        conn.commit()

    def save_card_info(self):
        cur.execute(f"INSERT INTO card (number, pin) VALUES ({self.account_num}, {self.pin});")
        conn.commit()

    def retrieve_data(self):
        cur.execute(f"SELECT number, pin FROM card WHERE number = {self.my_account} AND pin = {self.my_pin};")
        conn.commit()

    def acc_balance(self):
        cur.execute(f"SELECT balance from card WHERE number = {self.my_account};")
        acct = cur.fetchall()
        for i in acct:
            print("Balance:", *i)
        conn.commit()

    def transfer(self):
        print("Enter card number")
        acct = input()
        acct_luhn = [int(x) * 2 if i % 2 == 0 else int(x) for i, x in enumerate(acct[:-1])]
        num_sum3 = [num - 9 if num > 9 else num for num in acct_luhn]
        num_sum4 = sum(num_sum3)
        total2 = num_sum4 + int(acct[-1])
        cur.execute(f"SELECT id from card WHERE number = {acct};")
        outcome = cur.fetchone()
        conn.commit()
        if total2 % 10 != 0:
            print("Probably you made a mistake in the card number. Please try again!")
        elif outcome is None:
            print("Such a card does not exist.")
        elif acct == self.my_account:
            print("You can't transfer money to the same account!")
        else:
            print("Enter how much money you want to transfer:")
            amount = int(input())
            cur.execute(f"SELECT balance from card WHERE number = {self.my_account};")
            result = cur.fetchone()
            conn.commit()
            if amount > max(result):
                print("Not enough money!")
            else:
                print("Success!")
                cur.execute(f"UPDATE card SET balance = balance - {amount} WHERE number = {self.my_account};")
                cur.execute(f"UPDATE card SET balance = balance + {amount} WHERE number = {acct};")
                conn.commit()

    def close_account(self):
        cur.execute(f"DELETE FROM card WHERE number = {self.my_account};")
        conn.commit()
        print("The account has been closed!")

    def add_money(self):
        print("Enter income:")
        amount = int(input())
        cur.execute(f"UPDATE card SET balance = balance + {amount} WHERE number = {self.my_account};")
        conn.commit()
        print("Income was added!")


bank = BankApp()
cur.execute("DELETE FROM card")
conn.commit()

while True:
    bank.create_table()
    bank.home_page()
    choice = input()
    if choice == "1":
        bank.create_account()
    elif choice == "2":
        bank.login_info()
        bank.verify_login()
    elif choice == "0":
        print("\nBye!")
        break
