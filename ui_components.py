import tkinter as tk
from tkinter import ttk

def create_widgets(frame, app):
    app.entries = {}
    parameters = [
        ("起始年齡", "start_age", 27),
        ("目標退休年齡", "retirement_age", 50),
        ("退休每月支出 ($)", "monthly_expense", 30000),
        ("通脹率 (%)", "inflation_rate", 3),
        ("每月規劃投資 ($)", "monthly_investment", 15000),
        ("投資金額漲幅（每月 %）", "monthly_growth", 0),
        ("年度投資-單筆 ($)", "annual_investment", 50000),
        ("年度漲幅 (%)", "annual_growth", 0),
        ("起始金額 ($)", "initial_amount", 100000),
        ("股息回報率 (%)", "dividend_yield", 3),
        ("投資增值率 (%)", "capital_gain_rate", 5)
    ]
    row = 0
    for label_text, name, default_value in parameters:
        label = tk.Label(frame, text=label_text)
        entry = tk.Entry(frame)
        entry.insert(0, default_value)
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry.grid(row=row, column=1, padx=10, pady=5)
        app.entries[name] = entry
        row += 1

    app.calc_button = tk.Button(frame, text="計算", command=app.perform_calculation)
    app.calc_button.grid(row=row, column=0, columnspan=2, pady=10)

    app.open_new_page_button = tk.Button(frame, text="進入新頁面", command=app.open_new_page)
    app.open_new_page_button.grid(row=row+1, column=0, columnspan=2, pady=10)

    app.tree = ttk.Treeview(frame, columns=("accumulated_investment", "dividend_income", "monthly_expense"))
    app.tree.heading("#0", text="年齡")
    app.tree.heading("accumulated_investment", text="累積投資金額 ($)")
    app.tree.heading("dividend_income", text="股息收入 ($)")
    app.tree.heading("monthly_expense", text="未來預計支出/每月($)")
    app.tree.grid(row=row+2, column=0, columnspan=2, padx=10, pady=5)
