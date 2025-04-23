from decimal import Decimal
import tkinter as tk
import mysql.connector


conn = mysql.connector.connect(user = 'root', database = 'banking', password = 'g0SUHUg0')

def execute_query_edit(query):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

def record_transaction(name, trans_type, amount):
    execute_query_edit(f"INSERT INTO transactions (name, type, amount) VALUES ('{name}', '{trans_type}', {amount})")

def create_account():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter a password: ")
    execute_query_edit(f"INSERT INTO  users (name, password, email, balance) VALUES ('{name}', '{password}', '{email}', 0.0)")
    print("Created account successfully!")

def check_balance():
    name = input("Enter your name: ")
    password = input("Enter your password to login: ")
    cursor = conn.cursor()
    cursor.execute(f"SELECT balance FROM users WHERE name = '{name}' AND password = '{password}'")
    result = cursor.fetchone()
    cursor.close()

    if result:
        print(f"Your current balance is: ${result[0]}")
    else:
        print("Invalid name or password. Please retry again")

def deposit_funds():
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    amount = Decimal(input("Enter amount to deposit: "))

    cursor = conn.cursor()
    cursor.execute(f"SELECT balance FROM users WHERE name = '{name}' AND password = '{password}'")
    result = cursor.fetchone()

    if result:
        new_balance = result[0] + amount
        cursor.execute(f"UPDATE users SET balance = {new_balance} WHERE name = '{name}' AND password = '{password}'")
        conn.commit()
        record_transaction(name, "deposit", amount)
        print(f"Deposited ${amount}. New balance: ${new_balance}")
    else:
        print("Invalid name or password.")
    cursor.close()

def withdraw_funds():
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    amount = Decimal(input("Enter amount to withdraw: "))
    cursor = conn.cursor()
    cursor.execute(f"SELECT balance FROM users WHERE name = '{name}' AND password = '{password}'")
    result = cursor.fetchone()

    if result:
        if result[0] >= amount:
            new_balance = result[0] - amount
            cursor.execute(f" UPDATE users SET balance = {new_balance} WHERE name = '{name}' AND password = '{password}'")
            conn.commit()
            record_transaction(name, "withdrawal", amount) 
            print(f"Withdrew ${amount}. New balance: ${new_balance}")
        else:
            print("Insufficient funds. Please try again")
    cursor.close()


def delete_account():
    name = input("Enter your name: ")
    password = input("Enter your password to confirm: ")
    confirm = input("Are you sure you want to delete your account? (yes/no): ").lower()

    if confirm == "yes":
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE name = '{name}' AND password = '{password}'")
        if cursor.fetchone():
            cursor.execute(f"DELETE FROM users WHERE name = '{name}' AND password = '{password}'")
            cursor.execute(f"DELETE FROM transactions WHERE name = '{name}'")
            conn.commit()
            print("Account deleted.")
        else:
            print("Invalid name or password.")
        cursor.close()
    else:
        print("Account deletion cancelled.")

def modify_account():
    name = input("Enter your current name: ")
    password = input("Enter your current password: ")
    new_name = input("Enter new name (leave blank to keep unchanged): ")
    new_email = input("Enter new email (leave blank to keep unchanged): ")
    new_password = input("Enter new password (leave blank to keep unchanged): ")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE name = '{name}' AND password = '{password}'")
    if cursor.fetchone():
        updates = []
        if new_name:
            updates.append(f"name = '{new_name}'")
        if new_email:
            updates.append(f"email = '{new_email}'")
        if new_password:
            updates.append(f"password = '{new_password}'")
        if updates:
            update_query = ", ".join(updates)
            cursor.execute(f" UPDATE users SET {update_query} WHERE name = '{name}' AND password = '{password}'")
            conn.commit()
            print("Account information updated.")
        else:
            print("No changes made.")
    else:
        print("Invalid name or password.")
    cursor.close()


def view_transactions():
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE name = '{name}' AND password = '{password}'")
    if cursor.fetchone():
        cursor.execute(f"SELECT type, amount FROM transactions WHERE name = '{name}'")
        history = cursor.fetchall()
        print("\nTransaction History:")
        if not history:
            print("No transactions found.")
        for trans in history:
            print(f"{trans[0].capitalize()}: ${trans[1]}")
    else:
        print("Invalid name or password.")
    cursor.close()

  

while True:
    print("")
    print("Hello! Welcome to your C2C local bank!")
    print("")
    print("[0] Exit bank. ")
    print("[1] Create a new account. ")
    print("[2] Check account balance. ")
    print("[3] Deposit funds. ")
    print("[4] Withdraw funds. ")
    print("[5] Delete account. ")
    print("[6] Modify account details. ")
    print("[7] View transaction history. ")

    try:
        user_input = int(input("Command: "))
    except ValueError:
        print("")
        print("Please enter a valid number. ")
        continue

'''
    if (user_input == 0):
        print("Thank you for banking with us!")
        break
    elif (user_input == 1):
        print("")
        create_account()
    elif (user_input == 2):
        print("Checking your balance by entering the below info. ")
        check_balance()
    elif (user_input == 3):
        deposit_funds()
    elif (user_input == 4):
        withdraw_funds()
    elif (user_input == 5):
        delete_account()
    elif (user_input == 6):
        print("Modify account details. ")
        modify_account()
    elif (user_input == 7):
        print("View your old transactions. ")
        view_transactions()
    else:
        print("Invalid option. Please choose a valid command.")
'''
conn.close()