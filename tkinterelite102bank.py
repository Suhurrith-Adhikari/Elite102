import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
import mysql.connector

conn = mysql.connector.connect(user='root', database='banking', password='g0SUHUg0')

current_user = {'name': None, 'password': None}

def run_query(query, fetch=False):
    cur = conn.cursor()
    cur.execute(query)
    if fetch:
        data = cur.fetchall()
    else:
        data = None
    while cur.nextset():
        pass
    conn.commit()
    cur.close()
    return data

def check_login(name, password):
    q = f"SELECT * FROM users WHERE name='{name}' AND password='{password}'"
    result = run_query(q, fetch=True)
    if result:
        return True
    else:
        return False

def login_page():
    win = tk.Tk()
    win.title("Login")

    tk.Label(win, text="Name").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Password").pack()
    pass_entry = tk.Entry(win, show="*")
    pass_entry.pack()

    def handle_login():
        if check_login(name_entry.get(), pass_entry.get()):
            current_user['name'] = name_entry.get()
            current_user['password'] = pass_entry.get()
            win.destroy()
            main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid name or password.")

    def go_to_signup():
        win.destroy()
        create_account()

    tk.Button(win, text="Login", command=handle_login).pack()
    tk.Button(win, text="Create Account", command=go_to_signup).pack()

    win.mainloop()

def create_account():
    win = tk.Tk()
    win.title("Create Account")

    tk.Label(win, text="Name").pack()
    name = tk.Entry(win)
    name.pack()

    tk.Label(win, text="Email").pack()
    email = tk.Entry(win)
    email.pack()

    tk.Label(win, text="Password").pack()
    pwd = tk.Entry(win, show="*")
    pwd.pack()

    def handle_signup():
        q = f"INSERT INTO users (name, email, password, balance) VALUES ('{name.get()}', '{email.get()}', '{pwd.get()}', 0.0)"
        run_query(q)
        messagebox.showinfo("Success", "Account created.")
        win.destroy()
        login_page()

    tk.Button(win, text="Sign Up", command=handle_signup).pack()
    win.mainloop()

def show_balance():
    q = f"SELECT balance FROM users WHERE name='{current_user['name']}' AND password='{current_user['password']}'"
    result = run_query(q, fetch=True)
    if result:
        balance = result[0][0]
    else:
        balance = 0.0
    messagebox.showinfo("Your Balance", f"${balance}")

def deposit():
    win = tk.Toplevel()
    win.title("Deposit")

    tk.Label(win, text="Amount").pack()
    amt_entry = tk.Entry(win)
    amt_entry.pack()

    def submit_deposit():
        amt = Decimal(amt_entry.get())
        bal_query = f"SELECT balance FROM users WHERE name='{current_user['name']}' AND password='{current_user['password']}'"
        result = run_query(bal_query, fetch=True)

        if result:
            new_bal = result[0][0] + amt
        else:
            new_bal = amt

        update_q = f"UPDATE users SET balance={new_bal} WHERE name='{current_user['name']}' AND password='{current_user['password']}'"
        trans_q = f"INSERT INTO transactions (name, type, amount) VALUES ('{current_user['name']}', 'deposit', {amt})"

        run_query(update_q)
        run_query(trans_q)

        messagebox.showinfo("Success", f"New Balance: ${new_bal}")
        win.destroy()

    tk.Button(win, text="Submit", command=submit_deposit).pack()

def withdraw():
    win = tk.Toplevel()
    win.title("Withdraw")

    tk.Label(win, text="Amount").pack()
    amt_entry = tk.Entry(win)
    amt_entry.pack()

    def submit_withdrawal():
        amt = Decimal(amt_entry.get())
        q = f"SELECT balance FROM users WHERE name='{current_user['name']}' AND password='{current_user['password']}'"
        result = run_query(q, fetch=True)

        if result:
            bal = result[0][0]
        else:
            bal = 0.0

        if bal >= amt:
            new_bal = bal - amt
            update_q = f"UPDATE users SET balance={new_bal} WHERE name='{current_user['name']}' AND password='{current_user['password']}'"
            trans_q = f"INSERT INTO transactions (name, type, amount) VALUES ('{current_user['name']}', 'withdraw', {amt})"
            run_query(update_q)
            run_query(trans_q)
            messagebox.showinfo("Success", f"New Balance: ${new_bal}")
        else:
            messagebox.showerror("Error", "Not Enough Money")

        win.destroy()

    tk.Button(win, text="Submit", command=submit_withdrawal).pack()

def show_history():
    q = f"SELECT type, amount FROM transactions WHERE name='{current_user['name']}'"
    records = run_query(q, fetch=True)
    if records:
        history = "\n".join(f"{t.title()}: ${a}" for t, a in records)
    else:
        history = "No transactions found."
    messagebox.showinfo("Transaction History", history)

def main_menu():
    win = tk.Tk()
    win.title("Bank Menu")

    options = [
        ("Check Balance", show_balance),
        ("Deposit", deposit),
        ("Withdraw", withdraw),
        ("Transaction History", show_history)
    ]

    for label, action in options:
        btn = tk.Button(win, text=label, width=20, command=action)
        btn.pack(pady=5)

    win.mainloop()

login_page()
conn.close()
