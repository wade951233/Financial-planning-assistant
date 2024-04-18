import tkinter as tk
from tkinter import ttk

class FinanceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("財務規劃APP")  # 設置應用程式視窗標題
        self.create_widgets()

    def create_widgets(self):
        self.entries = {}  # 創建一個字典來保存所有的Entry小部件
        parameters = [  # 設置財務計算所需的參數，包括標籤文字、參數名稱和預設值
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
        # 逐行創建標籤和輸入框，並將其添加到字典中
        for label_text, name, default_value in parameters:
            label = tk.Label(self.master, text=label_text)
            entry = tk.Entry(self.master)
            entry.insert(0, default_value)  # 插入預設值
            label.grid(row=row, column=0, padx=10, pady=5, sticky="e")  # 使用黏性布局設置對齊方式
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.entries[name] = entry
            row += 1

        self.calc_button = tk.Button(self.master, text="計算", command=self.perform_calculation)
        self.calc_button.grid(row=row, column=0, columnspan=2, pady=10)

        # 創建一個樹狀結構的小部件來顯示財務狀況
        self.tree = ttk.Treeview(self.master, columns=("accumulated_investment", "dividend_income"))
        self.tree.heading("#0", text="年齡")  # 第一列為年齡
        self.tree.heading("accumulated_investment", text="累積投資金額 ($)")  # 第二列為累積投資金額
        self.tree.heading("dividend_income", text="股息收入 ($)")  # 第三列為股息收入
        self.tree.grid(row=row+1, column=0, columnspan=2, padx=10, pady=5)

    def perform_calculation(self):
        try:
            # 從輸入框中獲取參數值，並轉換成相應的數據類型
            params = {name: float(entry.get()) if name not in ['start_age', 'retirement_age'] else int(entry.get())
                      for name, entry in self.entries.items()}
            
            results = self.calculate_finances(**params)  # 執行財務計算
            
            # 清空樹狀結構的所有項目
            for item in self.tree.get_children():
                self.tree.delete(item)

            # 將每一年的財務狀況添加到樹狀結構中
            for year, finances in enumerate(results, start=params['start_age']):
                self.tree.insert("", "end", text=str(year), values=(f"${finances['accumulated_investment']:.2f}", f"${finances['dividend_income']:.2f}"))

        except ValueError:
            self.tree.delete(*self.tree.get_children())  # 如果出現錯誤，清空樹狀結構的所有項目
            self.tree.insert("", "end", text="錯誤", values=("請輸入有效的數值", ""))

#########################需要修改
    def calculate_finances(self, start_age, retirement_age, monthly_expense, inflation_rate,monthly_investment, monthly_growth,
                           annual_investment,annual_growth, initial_amount, dividend_yield, capital_gain_rate):
        
        years = retirement_age - start_age  # 計算退休年限

        results = []  # 創建一個列表來保存每一年的財務狀況

        future_value = initial_amount  # 初始化未來價值為起始金額

        for year in range(start_age, retirement_age + 1):  # 遍歷從起始年齡到目標退休年齡的每一年
            # 計算投資增長和股息收入
            future_value = future_value * (1 + annual_growth / 100) + annual_investment
            dividend_income = future_value * dividend_yield / 100
            accumulated_investment = future_value - initial_amount
            # 將當前年份的財務狀況添加到結果列表中
            results.append({'accumulated_investment': accumulated_investment, 'dividend_income': dividend_income})
        return results

def main():
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
