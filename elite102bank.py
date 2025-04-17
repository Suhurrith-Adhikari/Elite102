from decimal import Decimal
import mysql.connector

conn = mysql.connector.connect(user = 'root', database = 'banking', password = 'g0SUHUg0')

def execute_query_edit(query):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

def record_transaction(name, trans_type, amount):
    execute_query_edit(
        f"INSERT INTO transactions (name, type, amount) VALUES ('{name}', '{trans_type}', {amount})"
    )

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
        print(f"Deposited ${amount:.2f}. New balance: ${new_balance:.2f}")
    else:
        print("Invalid name or password.")
    cursor.close()

def withdraw_funds():


def delete_account():

def modify_account():


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
            print(f"{trans[0].capitalize()}: ${trans[1]:.2f}")
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


conn.close()