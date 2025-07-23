import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime

# -------------------- Main Menu --------------------
def show_main_menu():
    clear_window()

    tk.Label(window, text="Smart Finance Toolkit", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=20)

    tk.Button(window, text="1. CTC to In-Hand Salary", command=ctc_ui,
              font=("Helvetica", 12), bg="#4CAF50", fg="white", width=30).pack(pady=10)

    tk.Button(window, text="2. Tax Calculator", command=tax_ui,
              font=("Helvetica", 12), bg="#2196F3", fg="white", width=30).pack(pady=10)

    tk.Button(window, text="3. Monthly Expense Tracker", command=expense_ui,
              font=("Helvetica", 12), bg="#FF9800", fg="white", width=30).pack(pady=10)

    tk.Button(window, text="Exit", command=window.quit,
              font=("Helvetica", 12), bg="#f44336", fg="white", width=30).pack(pady=10)

# -------------------- CTC to In-Hand Salary --------------------
def calculate_salary():
    try:
        global last_ctc_result
        ctc = float(entry_ctc.get())

        pf = ctc * 0.12
        gratuity = ctc * 0.04
        professional_tax = 2400
        estimated_tax = ctc * 0.10

        total_deductions = pf + gratuity + professional_tax + estimated_tax
        inhand_annual = ctc - total_deductions
        inhand_monthly = inhand_annual / 12

        last_ctc_result = {
            "CTC": ctc,
            "PF": pf,
            "Gratuity": gratuity,
            "Professional Tax": professional_tax,
            "Estimated Tax": estimated_tax,
            "In-Hand Annual": inhand_annual,
            "In-Hand Monthly": inhand_monthly
        }

        result_label_ctc.config(
            text=f"CTC Breakdown:\n"
                 f"Provident Fund (12%): ₹{pf:,.2f}\n"
                 f"Gratuity (4%): ₹{gratuity:,.2f}\n"
                 f"Professional Tax: ₹{professional_tax:,.2f}\n"
                 f"Estimated Income Tax (10%): ₹{estimated_tax:,.2f}\n"
                 f"--------------------------------------------\n"
                 f"Net In-Hand Annual: ₹{inhand_annual:,.2f}\n"
                 f"Net In-Hand Monthly: ₹{inhand_monthly:,.2f}"
        )
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number!")

def export_ctc_pdf():
    try:
        data = last_ctc_result
        file = canvas.Canvas("CTC_Report.pdf", pagesize=A4)
        file.setFont("Helvetica-Bold", 16)
        file.drawString(100, 800, "CTC Breakdown Report")

        file.setFont("Helvetica", 12)
        y = 760
        lines = [
            f"Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}",
            f"CTC: ₹{data['CTC']:,.2f}",
            f"Provident Fund (12%): ₹{data['PF']:,.2f}",
            f"Gratuity (4%): ₹{data['Gratuity']:,.2f}",
            f"Professional Tax: ₹{data['Professional Tax']:,.2f}",
            f"Estimated Income Tax: ₹{data['Estimated Tax']:,.2f}",
            "---------------------------------------------",
            f"Net In-Hand (Annual): ₹{data['In-Hand Annual']:,.2f}",
            f"Net In-Hand (Monthly): ₹{data['In-Hand Monthly']:,.2f}"
        ]
        for line in lines:
            file.drawString(100, y, line)
            y -= 20

        file.save()
        messagebox.showinfo("Exported", "CTC_Report.pdf saved successfully.")
    except:
        messagebox.showerror("Error", "Please calculate first.")

def ctc_ui():
    clear_window()
    tk.Label(window, text="CTC to In-Hand Salary", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)

    global entry_ctc, result_label_ctc, last_ctc_result
    entry_ctc = tk.Entry(window, font=("Helvetica", 12), justify="center")
    entry_ctc.pack(pady=5)

    tk.Button(window, text="Calculate", command=calculate_salary,
              font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=10)

    result_label_ctc = tk.Label(window, text="", font=("Helvetica", 12), bg="#f0f0f0", fg="black")
    result_label_ctc.pack(pady=10)

    tk.Button(window, text="Export as PDF", command=export_ctc_pdf,
              font=("Helvetica", 11), bg="#9C27B0", fg="white").pack(pady=5)

    tk.Button(window, text="Back", command=show_main_menu,
              font=("Helvetica", 10), bg="#dddddd").pack(pady=5)

# -------------------- Tax Calculator --------------------
def calculate_tax():
    try:
        global last_tax_result
        income = float(entry_income.get())
        slab1 = slab2 = slab3 = 0

        if income <= 250000:
            tax = 0
        elif income <= 500000:
            slab1 = (income - 250000) * 0.05
            tax = slab1
        elif income <= 1000000:
            slab1 = 250000 * 0.05
            slab2 = (income - 500000) * 0.2
            tax = slab1 + slab2
        else:
            slab1 = 250000 * 0.05
            slab2 = 500000 * 0.2
            slab3 = (income - 1000000) * 0.3
            tax = slab1 + slab2 + slab3

        last_tax_result = {
            "Slab1": slab1,
            "Slab2": slab2,
            "Slab3": slab3,
            "Total Tax": tax,
            "Income": income
        }

        result_label_tax.config(
            text=f"Tax Breakdown:\n"
                 f"5% on ₹2.5L: ₹{slab1:,.2f}\n"
                 f"20% on ₹5L: ₹{slab2:,.2f}\n"
                 f"30% above ₹10L: ₹{slab3:,.2f}\n"
                 f"--------------------------------------------\n"
                 f"Total Tax Payable: ₹{tax:,.2f}"
        )
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid income!")

def export_tax_pdf():
    try:
        data = last_tax_result
        file = canvas.Canvas("Tax_Report.pdf", pagesize=A4)
        file.setFont("Helvetica-Bold", 16)
        file.drawString(100, 800, "Income Tax Breakdown Report")

        file.setFont("Helvetica", 12)
        y = 760
        lines = [
            f"Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}",
            f"Income: ₹{data['Income']:,.2f}",
            f"5% Slab: ₹{data['Slab1']:,.2f}",
            f"20% Slab: ₹{data['Slab2']:,.2f}",
            f"30% Slab: ₹{data['Slab3']:,.2f}",
            "---------------------------------------------",
            f"Total Tax Payable: ₹{data['Total Tax']:,.2f}"
        ]
        for line in lines:
            file.drawString(100, y, line)
            y -= 20

        file.save()
        messagebox.showinfo("Exported", "Tax_Report.pdf saved successfully.")
    except:
        messagebox.showerror("Error", "Please calculate first.")

def tax_ui():
    clear_window()

    tk.Label(window, text="Income Tax Calculator", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)

    global entry_income, result_label_tax, last_tax_result
    entry_income = tk.Entry(window, font=("Helvetica", 12), justify="center")
    entry_income.pack(pady=5)

    tk.Button(window, text="Calculate", command=calculate_tax,
              font=("Helvetica", 12), bg="#2196F3", fg="white").pack(pady=10)

    result_label_tax = tk.Label(window, text="", font=("Helvetica", 12), bg="#f0f0f0", fg="black")
    result_label_tax.pack(pady=10)

    tk.Button(window, text="Export as PDF", command=export_tax_pdf,
              font=("Helvetica", 11), bg="#9C27B0", fg="white").pack(pady=5)

    tk.Button(window, text="Back", command=show_main_menu,
              font=("Helvetica", 10), bg="#dddddd").pack(pady=5)

# -------------------- Expense Tracker --------------------
def calculate_expenses():
    try:
        global last_expense_result
        salary = float(entry_salary.get())
        rent = float(entry_rent.get())
        food = float(entry_food.get())
        travel = float(entry_travel.get())
        entertainment = float(entry_entertainment.get())
        bills = float(entry_bills.get())
        other = float(entry_other.get())

        total_exp = rent + food + travel + entertainment + bills + other
        balance = salary - total_exp

        last_expense_result = {
            "Salary": salary,
            "Rent": rent,
            "Food": food,
            "Travel": travel,
            "Entertainment": entertainment,
            "Bills": bills,
            "Other": other,
            "Total": total_exp,
            "Balance": balance
        }

        result_label_exp.config(
            text=f"Total Expenses: ₹{total_exp:,.2f}\nRemaining Balance: ₹{balance:,.2f}"
        )

        labels = ["Rent", "Food", "Travel", "Entertainment", "Bills", "Other"]
        values = [rent, food, travel, entertainment, bills, other]

        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Monthly Expense Breakdown")
        plt.axis("equal")
        plt.show()

    except ValueError:
        messagebox.showerror("Invalid Input", "Enter all values properly!")

def export_expense_pdf():
    try:
        data = last_expense_result
        file = canvas.Canvas("Expense_Report.pdf", pagesize=A4)
        file.setFont("Helvetica-Bold", 16)
        file.drawString(100, 800, "Monthly Expense Report")

        file.setFont("Helvetica", 12)
        y = 760
        lines = [
            f"Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}",
            f"Salary: ₹{data['Salary']:,.2f}",
            f"Rent: ₹{data['Rent']:,.2f}",
            f"Food: ₹{data['Food']:,.2f}",
            f"Travel: ₹{data['Travel']:,.2f}",
            f"Entertainment: ₹{data['Entertainment']:,.2f}",
            f"Bills: ₹{data['Bills']:,.2f}",
            f"Other: ₹{data['Other']:,.2f}",
            "---------------------------------------------",
            f"Total Expenses: ₹{data['Total']:,.2f}",
            f"Remaining Balance: ₹{data['Balance']:,.2f}"
        ]
        for line in lines:
            file.drawString(100, y, line)
            y -= 20

        file.save()
        messagebox.showinfo("Exported", "Expense_Report.pdf saved successfully.")
    except:
        messagebox.showerror("Error", "Please calculate first.")

def expense_ui():
    clear_window()

    tk.Label(window, text="Monthly Expense Tracker", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)

    global entry_salary, entry_rent, entry_food, entry_travel
    global entry_entertainment, entry_bills, entry_other, result_label_exp, last_expense_result

    entry_salary = create_entry("Monthly Salary:")
    entry_rent = create_entry("Rent:")
    entry_food = create_entry("Food:")
    entry_travel = create_entry("Travel:")
    entry_entertainment = create_entry("Entertainment:")
    entry_bills = create_entry("Bills & Utilities:")
    entry_other = create_entry("Other Expenses:")

    tk.Button(window, text="Calculate & Show Pie Chart", command=calculate_expenses,
              font=("Helvetica", 12), bg="#FF9800", fg="white").pack(pady=10)

    result_label_exp = tk.Label(window, text="", font=("Helvetica", 12), bg="#f0f0f0", fg="black")
    result_label_exp.pack(pady=10)

    tk.Button(window, text="Export as PDF", command=export_expense_pdf,
              font=("Helvetica", 11), bg="#9C27B0", fg="white").pack(pady=5)

    tk.Button(window, text="Back", command=show_main_menu,
              font=("Helvetica", 10), bg="#dddddd").pack(pady=5)

# -------------------- Helpers --------------------
def create_entry(label_text):
    tk.Label(window, text=label_text, font=("Helvetica", 11), bg="#f0f0f0").pack()
    entry = tk.Entry(window, font=("Helvetica", 11), justify="center")
    entry.pack(pady=3)
    return entry

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

# -------------------- App Launch --------------------
window = tk.Tk()
window.title("Smart Finance Toolkit")
window.geometry("420x800")
window.config(bg="#f0f0f0")

show_main_menu()
window.mainloop()