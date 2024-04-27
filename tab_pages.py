from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from matplotlib.figure import Figure
import sqlite3
import numpy as np
import customtkinter
class TabPageOne(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app  # 儲存對App類的引用
        parent.add(self, text='資產規劃')
        
        # 定義標籤、變數名稱和預設值的列表
        labels_and_defaults = [
            ("起始年齡：", "start_age", 27),
            ("目標退休年齡：", "retirement_age", 50),
            ("退休每月支出 ($)：", "monthly_expense", 30000),
            ("通脹率 (%)：", "inflation_rate", 3),
            ("每月規劃投資 ($)：", "monthly_investment", 15000),
            ("投資金額漲幅(每月 %)：", "monthly_growth", 1),
            ("年度投資-單筆 ($)：", "annual_investment", 50000),
            ("年度漲幅 (%)：", "annual_growth", 5),
            ("起始金額 ($)：", "initial_amount", 100000),
            ("股息回報率 (%)：", "dividend_yield", 3),
            ("投資增值率 (%)：", "capital_gain_rate", 5)
        ]

        self.entries = {}
        # 動態生成標籤和輸入框
        for i, (label_text, var_name, default) in enumerate(labels_and_defaults):
            label = ttk.Label(self, text=label_text)
            label.grid(column=0, row=i, padx=(50, 10), pady=5, sticky="e")
            # 創建輸入框
            entry = ttk.Entry(self)
            entry.grid(column=1, row=i, padx=(5, 10), pady=5, sticky="w")
            entry.insert(0, str(default))
            self.entries[var_name] = entry  # 將輸入框存儲到字典中
        # 設置列的配置以確保元件可以居中
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 添加按鈕
        action_frame = ttk.Frame(self)
        action_frame.grid(column=0, row=len(labels_and_defaults) + 1, columnspan=2, pady=10)
        #btn_calculate = ttk.Button(action_frame, text="計算", command=self.calculate)
        btn_calculate = customtkinter.CTkButton(action_frame, text="計算", command=self.calculate)
        btn_calculate.grid(column=0, row=0, padx=10)

        # 初始化TreeView
        self.tree = ttk.Treeview(self, columns=("age","accumulated_investment", "dividend_income", "monthly_expense"), show="headings")
        self.tree.grid(column=0, row=len(labels_and_defaults) + 2, columnspan=2, pady=10, sticky='ew')
        # 添加并设置新列的标题和宽度
        self.tree.heading("age", text="年齡")
        
        self.tree.column("age",width=40, minwidth=40, stretch=tk.NO, anchor='center')

        self.tree.heading("accumulated_investment", text="累積投資金額 ($)")
        self.tree.column("accumulated_investment", width=80, anchor='center')

        self.tree.heading("dividend_income", text="股息收入 ($)")
        self.tree.column("dividend_income", width=80, anchor='center')

        self.tree.heading("monthly_expense", text="未來預計支出/每月($)")
        self.tree.column("monthly_expense", width=80, anchor='center')

        # 設置列的自適應寬度
        self.columnconfigure(1, weight=1)

    def calculate(self):
        # 執行財務計算的方法
        try:
            # 從輸入欄位獲取數據並轉換成適當的數字類型
            self.params = {var_name: int(self.entries[var_name].get()) for var_name in self.entries}
            print("Parameters:", self.params)  # 輸出當前參數設定，用於檢查
            self.calculation_results = self.calculate_finances(**self.params)  # 根據參數進行財務計算
            self.update_tree(self.calculation_results)  # 根據計算結果更新樹狀視圖
        except ValueError:
            # 處理數據輸入錯誤，清空結果並提示錯誤信息
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=("請輸入有效的數值",))

        self.app.tab2.plot_planning(self.calculation_results)  # 調用TabPageTwo的plot_planning方法

    def calculate_finances(self, start_age, retirement_age, monthly_expense, inflation_rate, monthly_investment, monthly_growth,
                           annual_investment, annual_growth, initial_amount, dividend_yield, capital_gain_rate):
        # 計算資產增長的邏輯
        years = retirement_age - start_age  # 計算退休年限
        results = []  # 創建一個列表來保存每一年的財務狀況
        future_value = initial_amount  # 初始化未來價值為起始金額
        accumulated_investment = initial_amount  # 累積投資金額初值為起始金額

        for year in range(years + 1):  # 遍歷從起始年齡到目標退休年齡的每一年
           
            annual_dividend_income = accumulated_investment * (dividend_yield / 100) + monthly_investment * 12 * (dividend_yield / 100) * 0.5
            # 增值收益
            annual_capital_gain = accumulated_investment * (capital_gain_rate / 100) + monthly_investment * 12 * (capital_gain_rate / 100) * 0.5
            #累積投資金額
            accumulated_investment += (monthly_investment * 12 + annual_dividend_income + annual_capital_gain + annual_investment)
            #未來每月支出
            monthly_expense = monthly_expense * (1+(inflation_rate/100))
            # 將當前年份的財務狀況添加到結果列表中
            results.append({'year': start_age + year, 'accumulated_investment': accumulated_investment, 'dividend_income': annual_dividend_income, 'monthly_expense': monthly_expense})

        return results

    def update_tree(self, results):
        # 清空並更新樹狀視圖的方法
        self.tree.delete(*self.tree.get_children())  # 清除現有項目
        for result in results:
            # 根據計算結果逐年更新顯示
            self.tree.insert("", "end", values=(
                result['year'],  # 年龄数据
                f"${result['accumulated_investment']:.0f}",
                f"${result['dividend_income']:.0f}",
                f"${result['monthly_expense']:.0f}"
        ))


class TabPageTwo(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        parent.add(self, text='資產規劃報表')
    
         # 初始化界面的標籤
        self.label = ttk.Label(self, text='請在前一頁先做規劃')  # 保存標籤引用
        self.label.grid(column=0, row=0, padx=450, pady=10, sticky='nsew')
        
        self.grid_columnconfigure(0, weight=1)  # 使列能夠擴展，將標籤置中
        self.grid_rowconfigure(0, weight=1)
        
        self.canvas = None  # 用於保存圖表的Canvas
        

    def plot_planning(self, results):
        # 在繪製圖表前移除標籤
        self.label.destroy()  # 或使用 self.label.grid_remove() 隱藏而不是銷毀

        # 使用matplotlib的深色主題來繪製圖表
        plt.style.use('dark_background')
        # 創建 Figure 對象，設置 DPI 和大小
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), dpi=80)  # DPI 可根據實際情況調整
        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.1)  # 减少边距
        fig.patch.set_facecolor('#333333')  # 設置背景色

        # 從 results 提取數據
        years = [result['year'] for result in results]
        accumulated_investments = [result['accumulated_investment'] for result in results]
        dividend_incomes = [result['dividend_income']/12 for result in results]
        monthly_expenses = [result['monthly_expense'] for result in results]

        # 繪製第一張圖表：股息收入和月支出
        bars = ax1.bar(years, dividend_incomes, color='#ff7f0e', width=0.4, label='Dividend Income/M')
        line1, = ax1.plot(years, monthly_expenses, color='#ffffff', marker='x', linestyle='-', label='Monthly Expense')
        ax1.set_ylabel('Values ($)', color='white')
        ax1.legend(loc='upper left', frameon=False, fontsize=8)
        ax1.set_title('Dividend Income and Monthly Expenses Over Years', fontsize=8, color='white')
        
        
        # 標註股息收入和年度支出的數據點
        for bar, div, exp in zip(bars, dividend_incomes, monthly_expenses):
            ax1.text(bar.get_x() + bar.get_width()/2, div, f"{int(div)}", ha='center', va='bottom', color='white', fontsize=8)
            ax1.text(bar.get_x() + bar.get_width()/2, exp, f"{int(exp)}", ha='center', va='bottom', color='white', fontsize=8)
        
        # 繪製第二張圖表：累積投資
        bars2 = ax2.bar(years, accumulated_investments, color='#1f77b4', width=0.4, label='Accumulated Investment')
        ax2.set_xlabel('Age', fontsize=12, fontweight='bold', color='white')
        ax2.set_ylabel('Accumulated Investment ($)', color='white')
        ax2.legend(loc='upper left', frameon=False, fontsize=8)
        ax2.set_title('Accumulated Investments Over Years', fontsize=8, color='white')

        # 標註累積投資的數據點
        for bar in bars2:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{int(bar.get_height())}", ha='center', va='bottom', color='white', fontsize=8)

        # 設定 X 軸刻度為整數
        ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        # 如果已經有canvas, 先銷毀再重建
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # 將 matplotlib 圖表添加到 Tkinter 窗口
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, sticky='nsew', pady=5, padx=5)

        # 配置 frame 的 grid 以填滿 canvas
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)


class TabPageThree(ttk.Frame):
    def __init__(self, parent, db ):
        super().__init__(parent)
        parent.add(self, text='財務紀錄')
        # ttk.Label(self, text='這是第三頁的內容').grid(column=0, row=0, padx=10, pady=10)
        # 初始化数据库控制器
        self.db = db

        self.entries = {}
        self.labels = {}
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        recording_parameters = [
            ("西元年", "Year", 2024, "entry"),# 
            ("月份", "Month", months, "combobox"),  # Changed from 'entry' to 'combobox' and provided the list of months as default values
            ("台股", "Taiwan Stocks", 124000, "entry"),
            ("台股佔比 (%)", "Taiwan Stocks Percentage", 0, "label"),
            ("美股", "US Stocks", 44100, "entry"),
            ("美股佔比 (%)", "US Stocks Percentage", 0, "label"),
            ("虛擬貨幣", "Cryptocurrency", 180000, "entry"),
            ("虛擬貨幣佔比 (%)", "Cryptocurrency Percentage", 0, "label"),
            ("活存", "Savings", 280000, "entry"),
            ("活存佔比 (%)", "Savings Percentage", 0, "label"),
            ("總資產 ($)", "Total Assets", 0, "label"),
        ]

        row = 1
        for label_text, name, default_value, widget_type in recording_parameters:
            label = ttk.Label(self, text=label_text)
            label.grid(row=row, column=0, padx=(10, 2), pady=2, sticky="e")

            if widget_type == "entry":
                widget = ttk.Entry(self)
                widget.insert(0, default_value)
                widget.grid(row=row, column=1, padx=(2, 10), pady=2, sticky="w")
                self.entries[name] = widget
            elif widget_type == "combobox":
                widget = ttk.Combobox(self, values=default_value)
                widget.set(default_value[0])  # Set the default value to the first month
                widget.grid(row=row, column=1, padx=(2, 9), pady=2, sticky="w")
                self.entries[name] = widget
            elif widget_type == "label":
                widget = ttk.Label(self,text=f"{default_value:.2f}")
                widget.grid(row=row, column=1, padx=(2, 10), pady=2, sticky="w")
                self.labels[name] = widget
            row += 1

        # ttk.update_button = tk.Button(self, text="紀錄資料", command=self.db_add_data)
        # ttk.update_button.grid(row=row, column=0, columnspan=2, pady=10, sticky="w")
        
        # 設置列的配置以確保元件可以居中
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # ttk.calculate_button = tk.Button(self, text="計算佔比和總資產", command=self.calculate_percentages_and_total)
        # ttk.calculate_button.grid(row=row, column=1, columnspan=2, pady=10, sticky="w")
        ttk.update_button = customtkinter.CTkButton(self, text="紀錄資料", command=lambda: [self.calculate_percentages_and_total(), self.db_add_data()])
        ttk.update_button.grid(row=row, column=0, pady=10)

        ttk.delete_record_button = customtkinter.CTkButton(self, text="刪除資料", command=lambda: self.db_delete_data(self.get_selected_id()))
        ttk.delete_record_button.grid(row=row, column=1, pady=10)

        
        # 配置 Treeview 控件，用於顯示各項資產數據
        columns = ("西元年","月份", "台股", "台股佔比 (%)", "美股", "美股佔比 (%)", "虛擬貨幣", "虛擬貨幣佔比 (%)", "活存", "活存佔比 (%)", "總資產 ($)")
        self.portfolio_tree = ttk.Treeview(self, columns=columns, height=8, padding=5)
        self.portfolio_tree.heading("#0", text="資料 ID", anchor='w')
        self.portfolio_tree.column("#0",width=40, minwidth=40, stretch=tk.NO)
        # 為 Treeview 的每一列設置標題和列寬等屬性
        for col in columns:
            # 設置列標題，將列名中的底線替換為空格，並設置文本對齊方式為左對齊
            self.portfolio_tree.heading(col, text=col, anchor='w')
            # 設置列的寬度、最小寬度，並禁用伸縮
            self.portfolio_tree.column(col, width=90, minwidth=80, stretch=tk.NO, anchor='center')
        self.db_update_portfolio_tree()
        
        # 將 Treeview 控件添加到布局中，放置於按鈕下方
        row += 1  # 增加 row 變數，以使 Treeview 在按鈕下方的新行開始
        self.portfolio_tree.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # 設定框架的列配置，使第二列有彈性（權重為1），可以隨窗口大小調整而伸縮
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def db_add_data(self):
        data = {
            'Year': self.entries['Year'].get(),
            'Month': self.entries['Month'].get(),
            'Taiwan Stocks': self.entries['Taiwan Stocks'].get(),
            'Taiwan Stocks Percentage': self.labels['Taiwan Stocks Percentage'].cget('text'),
            'US Stocks': self.entries['US Stocks'].get(),
            'US Stocks Percentage': self.labels['US Stocks Percentage'].cget('text'),
            'Cryptocurrency': self.entries['Cryptocurrency'].get(),
            'Cryptocurrency Percentage': self.labels['Cryptocurrency Percentage'].cget('text'),
            'Savings': self.entries['Savings'].get(),
            'Savings Percentage': self.labels['Savings Percentage'].cget('text'),
            'Total Assets': self.labels['Total Assets'].cget('text')
        }
        self.db.add_data(data)
        self.db_update_portfolio_tree()

    def db_delete_data(self, id):
        if id:
            self.db.delete_data(id)
            self.db_update_portfolio_tree()
        else:
            print("No item selected or invalid ID")

    def get_selected_id(self):
            """獲取選中項目的ID"""
            selected_item = self.portfolio_tree.selection()
            if selected_item:
                return self.portfolio_tree.item(selected_item[0])['text']
            return None
    
    def db_update_portfolio_tree(self):
        data = self.db.fetch_all_data()
        self.portfolio_tree.delete(*self.portfolio_tree.get_children())
        for row in data:
            self.portfolio_tree.insert('', 'end', text=row[0], values=row[1:])

    def calculate_percentages_and_total(self):
        '''計算百分比和總資產'''
        print("計算百分比和總資產")
        try:
            taiwan_stocks = float(self.entries["Taiwan Stocks"].get())
            us_stocks = float(self.entries["US Stocks"].get())
            cryptocurrency = float(self.entries["Cryptocurrency"].get())
            savings = float(self.entries["Savings"].get())

            total_assets = taiwan_stocks + us_stocks + cryptocurrency + savings
            self.labels["Total Assets"].config(text=f"{total_assets:.0f}")  # Update label text correctly

            if total_assets > 0:
                self.labels["Taiwan Stocks Percentage"].config(text=f"{(taiwan_stocks / total_assets * 100):.0f}%")
                self.labels["US Stocks Percentage"].config(text=f"{(us_stocks / total_assets * 100):.0f}%")
                self.labels["Cryptocurrency Percentage"].config(text=f"{(cryptocurrency / total_assets * 100):.0f}%")
                self.labels["Savings Percentage"].config(text=f"{(savings / total_assets * 100):.0f}%")
        except ValueError:
            print("請確保輸入的是有效的數字。")

        
class TabPageFour(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.add(self, text='財務紀錄報表')
        row = 1
        self.update_button = customtkinter.CTkButton(self, text="更新圖表", command=self.gen_recording)
        # 將按鈕水平置中
        self.update_button.grid(row=row, column=1, pady=10, sticky="ew")
        # 確保中間列能夠擴展，並且使得左右兩側列的權重均等
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def gen_recording(self):
        print("execute gen_recording")
        self.db = db_control()
        data = self.db.fetch_all_data()

        num_data_points = len(data)
        segments = [tuple(entry[i] for i in [3, 5, 7, 9]) for entry in data]
        percentages = [tuple(entry[i] for i in [4, 6, 8, 10]) for entry in data]
        totals = [entry[-1] for entry in data]

        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(num_data_points)
        colors = ['red', 'green', 'blue', 'purple']
        bottom = np.zeros(num_data_points)

        for seg_heights, seg_percentages, color in zip(zip(*segments), zip(*percentages), colors):
            bars = ax.bar(x, seg_heights, bottom=bottom, color=color)
            bottom += seg_heights
            for bar, percentage in zip(bars, seg_percentages):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2, f'{percentage}%', ha='center', va='center', color='white', fontsize=8)

        date = [f"{entry[2]}/{entry[1]}" for entry in data]
        ax.set_xticks(x)
        ax.set_xticklabels(date, rotation=30, fontsize='small')
        ax.plot(x, totals, 'o-', color='gold', label='Total', linewidth=2, markersize=8)

        for i, total in enumerate(totals):
            ax.text(x[i], total, f'{total:.0f}', ha='center', va='bottom', color='black', fontsize=8)
        
        ax.set_xlabel('Month')
        ax.set_ylabel('Value')
        ax.legend(loc='upper left')

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=3, sticky='nsew', pady=10, padx=10)
        self.grid_columnconfigure(0, weight=1)
        # 設置第 2 行的 rowconfigure 確保圖表區域可以擴展
        self.grid_rowconfigure(2, weight=1)



class db_control:
    def __init__(self, dbname="finance_app.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year TEXT,
                month TEXT,
                taiwan_stocks REAL,
                taiwan_stocks_percentage TEXT,
                us_stocks REAL,
                us_stocks_percentage TEXT,
                cryptocurrency REAL,
                cryptocurrency_percentage TEXT,
                savings REAL,
                savings_percentage TEXT,
                total_assets REAL
            )
        ''')
        self.conn.commit()

    def add_data(self, data):
        self.cursor.execute('''
            INSERT INTO assets (
                year, month, taiwan_stocks, taiwan_stocks_percentage, us_stocks, us_stocks_percentage,
                cryptocurrency, cryptocurrency_percentage, savings, savings_percentage, total_assets
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['Year'],
            data['Month'],
            data['Taiwan Stocks'], data['Taiwan Stocks Percentage'],
            data['US Stocks'], data['US Stocks Percentage'],
            data['Cryptocurrency'], data['Cryptocurrency Percentage'],
            data['Savings'], data['Savings Percentage'],
            data['Total Assets']
        ))
        self.conn.commit()

    def fetch_all_data(self):
        self.cursor.execute('SELECT * FROM assets')
        return self.cursor.fetchall()

    def delete_data(self, id):
        self.cursor.execute('DELETE FROM assets WHERE id=?', (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
