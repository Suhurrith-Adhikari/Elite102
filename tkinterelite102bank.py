import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
import mysql.connector

conn = mysql.connector.connect(user='root', database='banking', password='g0SUHUg0')
current_user = {'name': None, 'password': None}

def run_query(query, fetch=False):
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall() if fetch else None
    while cur.nextset():
        pass  # clear any unread results
    conn.commit()
    cur.close()
    return result

def check_login(name, password):
    result = run_query(f"SELECT * FROM users WHERE name='{name}' AND password='{password}'", fetch=True)
    return bool(result)

def login_page():
    win = tk.Tk()
    win.title("Login")
    tk.Label(win, text="Name").pack()
    name = tk.Entry(win)
    name.pack()
    tk.Label(win, text="Password").pack()
    pwd = tk.Entry(win, show="*")
    pwd.pack()

    def try_login():
        if check_login(name.get(), pwd.get()):
            current_user['name'], current_user['password'] = name.get(), pwd.get()
            win.destroy()
            main_menu()
        else:
            messagebox.showerror("Error", "Wrong login info")

    def open_create():
        win.destroy()
        create_account()

    tk.Button(win, text="Login", command=try_login).pack()
    tk.Button(win, text="Create Account", command=open_create).pack()
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

    def submit():
        run_query(f"INSERT INTO users (name, email, password, balance) VALUES ('{name.get()}', '{email.get()}', '{pwd.get()}', 0.0)")
        messagebox.showinfo("Done", "Account created")
        win.destroy()
        login_page()

    tk.Button(win, text="Submit", command=submit).pack()
    win.mainloop()

def show_balance():
    result = run_query(f"SELECT balance FROM users WHERE name='{current_user['name']}' AND password='{current_user['password']}'", fetch=True)
    bal = result[0][0] if result else 0.0
    messagebox.showinfo("Balance", f"Balance: ${bal}")

def deposit():
    win = tk.Toplevel()
    win.title("Deposit")
    tk.Label(win, text="Amount").pack()
    amt = tk.Entry(win)
    amt.pack()

    def go():
        amount = Decimal(amt.get())
        result = run_query(f"SELECT balance FROM users WHERE name='{current_user['name']}' AND password='{current_user['password']}'", fetch=True)
        bal = result[0][0] + amount if result else amount
        run_query(f"UPDATE users SET balance={bal} WHERE name='{current_user['name']}' AND password='{current_user['password']}'")
        run_query(f"INSERT INTO transactions (name, type, amount) VALUES ('{current_user['name']}', 'deposit', {amount})")
        messagebox.showinfo("Deposited", f"New balance: ${bal}")
        win.destroy()

    tk.Button(win, text="Submit", command=go).pack()

def withdraw():
    win = tk.Toplevel()
    win.title("Withdraw")
    tk.Label(win, text="Amount").pack()
    amt = tk.Entry(win)
    amt.pack()

    def go():
        amount = Decimal(amt.get())
        result = run_query(f"SELECT balance FROM users WHERE name='{current_user['name']}' AND password='{current_user['password']}'", fetch=True)
        bal = result[0][0] if result else 0.0
        if bal >= amount:
            new_bal = bal - amount
            run_query(f"UPDATE users SET balance={new_bal} WHERE name='{current_user['name']}' AND password='{current_user['password']}'")
            run_query(f"INSERT INTO transactions (name, type, amount) VALUES ('{current_user['name']}', 'withdraw', {amount})")
            messagebox.showinfo("Withdrawn", f"New balance: ${new_bal}")
        else:
            messagebox.showerror("Error", "Not enough money")
        win.destroy()

    tk.Button(win, text="Submit", command=go).pack()

def show_history():
    records = run_query(f"SELECT type, amount FROM transactions WHERE name='{current_user['name']}'", fetch=True)
    history = "\n".join([f"{r[0].title()}: ${r[1]}" for r in records]) or "No transactions"
    messagebox.showinfo("Transactions", history)

def main_menu():
    win = tk.Tk()
    win.title("Bank")
    for label, func in [("Check Balance", show_balance), ("Deposit", deposit), ("Withdraw", withdraw), ("Transactions", show_history)]:
        tk.Button(win, text=label, width=20, command=func).pack(pady=5)
    win.mainloop()

login_page()
conn.close()