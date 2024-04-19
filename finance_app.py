import tkinter as tk
from tkinter import ttk
from ui_components import create_widgets
from finance_calculator import calculate_finances

class FinanceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("財務規劃APP")  # 設置應用程式視窗標題
        self.notebook = ttk.Notebook(master)
        self.main_frame = ttk.Frame(self.notebook)  # 主頁面
        self.notebook.add(self.main_frame, text='主頁面')
        self.notebook.pack(expand=1, fill="both")
        create_widgets(self.main_frame, self)

    def perform_calculation(self):
        try:
            self.params = {name: float(entry.get()) if name not in ['start_age', 'retirement_age'] else int(entry.get())
                           for name, entry in self.entries.items()}
            results = calculate_finances(**self.params)
            self.update_tree(results, self.params['start_age'])  # Pass start_age as a parameter
        except ValueError:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", text="錯誤", values=("請輸入有效的數值", ""))

    def update_tree(self, results, start_age):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for year, finances in enumerate(results, start=start_age):
            self.tree.insert("", "end", text=str(year), values=(f"${finances['accumulated_investment']:.0f}", f"${finances['dividend_income']:.0f}", f"${finances['monthly_expense']:.0f}"))

    def open_new_page(self):
        new_frame = ttk.Frame(self.notebook)
        self.notebook.add(new_frame, text=f'新頁面 {len(self.notebook.tabs())}')
        tk.Label(new_frame, text="這是一個新的頁面").pack(pady=20)
        close_button = tk.Button(new_frame, text="關閉此頁面", command=lambda: self.close_page(new_frame))
        close_button.pack(pady=20)

    def close_page(self, frame):
        index = self.notebook.index(frame)
        self.notebook.forget(index)
