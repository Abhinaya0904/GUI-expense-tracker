import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILENAME = 'expenses.csv'
MAX_BUDGET = 10000  # You can change this to your desired monthly budget (₹)

# Ensure CSV file exists
def initialize_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])

# Calculate current month's total expenses
def get_current_month_expense():
    total_expense = 0
    current_month = datetime.now().strftime("%Y-%m")

    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Type'] == 'Expense' and row['Date'].startswith(current_month):
                    total_expense += float(row['Amount'])
    return total_expense

# Save entry to CSV
def save_transaction():
    date = date_entry.get()
    t_type = type_var.get()
    category = category_entry.get()
    amount = amount_entry.get()
    desc = desc_entry.get()

    if not amount or not category or not date:
        messagebox.showerror("Error", "Date, Category, and Amount are required.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Date must be in YYYY-MM-DD format.")
        return

    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, t_type, category, amount, desc])

    messagebox.showinfo("Success", f"{t_type} added successfully!")
    clear_inputs()

    # Check budget after adding expense
    if t_type == 'Expense':
        total_expense = get_current_month_expense()
        if total_expense > MAX_BUDGET:
            messagebox.showwarning("Budget Exceeded!", f"Warning: Your expenses for this month have exceeded ₹{MAX_BUDGET}.\nCurrent Expense: ₹{total_expense}")

# Clear form
def clear_inputs():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    type_var.set("Expense")

# Show summary
def show_summary():
    income = 0
    expense = 0
    with open(FILENAME, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            amt = float(row['Amount'])
            if row['Type'] == 'Income':
                income += amt
            elif row['Type'] == 'Expense':
                expense += amt

    result = f"Total Income: ₹{income}\nTotal Expense: ₹{expense}\nSavings: ₹{income - expense}"
    messagebox.showinfo("Summary", result)

# Pie Chart for Income vs Expense
def show_pie_chart():
    income = 0
    expense = 0
    with open(FILENAME, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            amt = float(row['Amount'])
            if row['Type'] == 'Income':
                income += amt
            elif row['Type'] == 'Expense':
                expense += amt

    if income == 0 and expense == 0:
        messagebox.showinfo("No Data", "No transactions to visualize.")
        return

    labels = ['Income', 'Expense']
    values = [income, expense]
    colors = ['green', 'red']

    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title("Income vs Expense Distribution")
    plt.show()

# Bar Chart for Category-wise Expenses
def show_category_expenses():
    category_totals = {}
    with open(FILENAME, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Type'] == 'Expense':
                category = row['Category']
                amt = float(row['Amount'])
                category_totals[category] = category_totals.get(category, 0) + amt

    if not category_totals:
        messagebox.showinfo("No Data", "No expense data to visualize.")
        return

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(8, 5))
    plt.bar(categories, amounts, color='orange')
    plt.xlabel("Category")
    plt.ylabel("Total Expense (₹)")
    plt.title("Category-wise Expense Distribution")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Initialize file
initialize_file()

# Create window
root = tk.Tk()
root.title("Expense Tracker with Budget Alert")

# Date input
tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1)

# Type selector
tk.Label(root, text="Type").grid(row=1, column=0)
type_var = tk.StringVar(value="Expense")
tk.OptionMenu(root, type_var, "Income", "Expense").grid(row=1, column=1)

# Category input
tk.Label(root, text="Category").grid(row=2, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=2, column=1)

# Amount input
tk.Label(root, text="Amount").grid(row=3, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=3, column=1)

# Description input
tk.Label(root, text="Description").grid(row=4, column=0)
desc_entry = tk.Entry(root)
desc_entry.grid(row=4, column=1)

# Buttons
tk.Button(root, text="Add Entry", command=save_transaction, bg="green", fg="white").grid(row=5, column=0, pady=10)
tk.Button(root, text="View Summary", command=show_summary, bg="blue", fg="white").grid(row=5, column=1)

# Visualization Buttons
tk.Button(root, text="Pie Chart (Income vs Expense)", command=show_pie_chart, bg="purple", fg="white").grid(row=6, column=0, pady=5)
tk.Button(root, text="Bar Chart (Category Expenses)", command=show_category_expenses, bg="orange", fg="white").grid(row=6, column=1, pady=5)

# Run GUI
root.mainloop()
