import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = "data.csv"

# Initialize data file
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Amount", "Note"])

class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense & Budget Tracker")
        self.budget = tk.DoubleVar()
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.root, text="Set Monthly Budget:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.budget).grid(row=0, column=1, padx=10)
        ttk.Button(self.root, text="Set Budget", command=self.set_budget).grid(row=0, column=2)

        ttk.Label(self.root, text="Category:").grid(row=1, column=0)
        self.category_entry = ttk.Entry(self.root)
        self.category_entry.grid(row=1, column=1)

        ttk.Label(self.root, text="Amount:").grid(row=2, column=0)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1)

        ttk.Label(self.root, text="Note:").grid(row=3, column=0)
        self.note_entry = ttk.Entry(self.root)
        self.note_entry.grid(row=3, column=1)

        ttk.Button(self.root, text="Add Expense", command=self.add_expense).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="View Report", command=self.view_report).grid(row=5, column=0, pady=5)
        ttk.Button(self.root, text="Show Chart", command=self.show_chart).grid(row=5, column=1, pady=5)

    def set_budget(self):
        try:
            amount = float(self.budget.get())
            messagebox.showinfo("Success", f"Monthly budget set to ₹{amount}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def add_expense(self):
        category = self.category_entry.get()
        note = self.note_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Enter a valid number.")
            return

        with open(DATA_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d"), category, amount, note])

        messagebox.showinfo("Expense Added", f"Added ₹{amount} for {category}")

        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)

    def view_report(self):
        total = 0
        report = {}
        with open(DATA_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += float(row["Amount"])
                cat = row["Category"]
                report[cat] = report.get(cat, 0) + float(row["Amount"])

        output = f"Total Spent: ₹{total:.2f}\n"
        if self.budget.get() > 0:
            output += f"Budget: ₹{self.budget.get()}\n"
            output += f"Remaining: ₹{self.budget.get() - total:.2f}\n"

        output += "\nCategory-wise Breakdown:\n"
        for k, v in report.items():
            output += f" - {k}: ₹{v:.2f}\n"

        messagebox.showinfo("Report", output)

    def show_chart(self):
        report = {}
        with open(DATA_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cat = row["Category"]
                report[cat] = report.get(cat, 0) + float(row["Amount"])

        if not report:
            messagebox.showinfo("No Data", "No expenses found.")
            return

        plt.figure(figsize=(6, 6))
        plt.pie(report.values(), labels=report.keys(), autopct="%1.1f%%", startangle=140)
        plt.title("Expenses by Category")
        plt.show()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTracker(root)
    root.mainloop()

