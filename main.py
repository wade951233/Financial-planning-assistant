import tkinter as tk
from tkinter import ttk
from ui_components import planning_widgets  # 引入創建小組件的函數
from ui_components import recording_widgets  # 引入創建小組件的函數
from finance_calculator import calculate_finances  # 引入財務計算函數
import sqlite3

class FinanceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("財務規劃APP")  # 設置應用程式視窗標題
        self.notebook = ttk.Notebook(master)  # 創建一個筆記本小組件，用來管理多個頁面
        self.db_manager = DatabaseManager('finance_app.db')  # 創建資料庫管理對象
   
        # self.entries = {}  # Initialize the entries dictionary
        self.labels = {}   # Initialize the labels dictionary

        # 在筆記本中設立4個分頁
        self.planning_frame = ttk.Frame(self.notebook)  # 創建「資產規劃」的框架
        self.notebook.add(self.planning_frame, text='資產規劃')  # 將「資產規劃」框架添加到筆記本中
        planning_widgets(self.planning_frame, self)  # 呼叫創建小組件的函數來設置界面

        self.recording_frame = ttk.Frame(self.notebook)  # 創建「資產紀錄」分頁的框架
        self.notebook.add(self.recording_frame, text='資產紀錄')  # 將「資產紀錄」分頁添加到筆記本中
        recording_widgets(self.recording_frame, self, self.db_manager)  # 呼叫創建小組件的函數來設置界面

        self.expenses_frame = ttk.Frame(self.notebook)  # 創建「支出」分頁的框架
        self.notebook.add(self.expenses_frame, text='支出')  # 將「支出」分頁添加到筆記本中
        
        self.investments_frame = ttk.Frame(self.notebook)  # 創建「投資」分頁的框架
        self.notebook.add(self.investments_frame, text='投資')  # 將「投資」分頁添加到筆記本中

        self.reports_frame = ttk.Frame(self.notebook)  # 創建「報告」分頁的框架
        self.notebook.add(self.reports_frame, text='報告')  # 將「報告」分頁添加到筆記本中

        self.notebook.pack(expand=1, fill="both")  # 放置筆記本並允許擴展和填充空間

        # 更新 GUI 顯示
        #self.update_portfolio_tree()

    def perform_calculation(self):
        try:
            # 將輸入欄位的數據轉換為適當的數字類型
            self.params = {
                "start_age": int(self.entries["start_age"].get()),  # 起始年齡
                "retirement_age": int(self.entries["retirement_age"].get()),  # 目標退休年齡
                "monthly_expense": float(self.entries["monthly_expense"].get()),  # 退休每月支出
                "inflation_rate": float(self.entries["inflation_rate"].get()),  # 通脹率
                "monthly_investment": float(self.entries["monthly_investment"].get()),  # 每月規劃投資
                "monthly_growth": float(self.entries["monthly_growth"].get()),  # 投資金額漲幅（每月）
                "annual_investment": float(self.entries["annual_investment"].get()),  # 年度投資-單筆
                "annual_growth": float(self.entries["annual_growth"].get()),  # 年度漲幅
                "initial_amount": float(self.entries["initial_amount"].get()),  # 起始金額
                "dividend_yield": float(self.entries["dividend_yield"].get()),  # 股息回報率
                "capital_gain_rate": float(self.entries["capital_gain_rate"].get())  # 投資增值率
            }

            print("Parameters:", self.params)  # 打印 self.params 以檢查其值

            results = calculate_finances(**self.params)  # 進行財務計算
            self.update_tree(results, self.params['start_age'])  # 更新顯示結果

        except ValueError:
            # 處理輸入錯誤，清除現有結果並顯示錯誤信息
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", text="錯誤", values=("請輸入有效的數值", ""))


    def update_tree(self, results, start_age):
        # 清空現有的樹狀視圖項目
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 根據計算結果更新樹狀視圖
        for year, finances in enumerate(results, start=start_age):
            self.tree.insert("", "end", text=str(year), values=(f"${finances['accumulated_investment']:.0f}", f"${finances['dividend_income']:.0f}", f"${finances['monthly_expense']:.0f}"))

    # def opens_new_page(self):
    #     new_frame = ttk.Frame(self.notebook)  # 創建一個新的框架用於新頁面
    #     self.notebook.add(new_frame, text=f'新頁面 {len(self.notebook.tabs())}')  # 添加新頁面到筆記本
    #     tk.Label(new_frame, text="這是一個新的頁面").pack(pady=20)  # 新頁面中添加標籤顯示文字
    #     close_button = tk.Button(new_frame, text="關閉此頁面", command=lambda: self.close_page(new_frame))  # 添加關閉頁面的按鈕
    #     close_button.pack(pady=20)

    # def close_page(self, frame):
    #     index = self.notebook.index(frame)  # 獲取欲關閉頁面的索引
    #     self.notebook.forget(index)  # 移除指定索引的頁面


class DatabaseManager:
    def __init__(self, db_name):
        """ 初始化資料庫管理員類 """
        self.db_name = db_name
        self.entries = {}  # Initialize the entries dictionary
        self.labels = {}  

    def connect(self):
        """ 建立並返回資料庫連接 """
        return sqlite3.connect(self.db_name)

    def add_data(self):
        # 從界面獲取數據
        data = {name: self.entries[name].get() for name in self.entries}
        data.update({name: self.labels[name].cget("text") for name in self.labels})  # 對於labels使用 cget("text") 獲取顯示的文本
        print("data:", data)
        # 連接到數據庫
        conn = sqlite3.connect('finance_app.db')
        c = conn.cursor()
        
        # 插入數據
        c.execute('''
            INSERT INTO assets (
                month, taiwan_stocks, taiwan_stocks_percentage, us_stocks, us_stocks_percentage, 
                cryptocurrency, cryptocurrency_percentage, savings, savings_percentage, total_assets
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['Month'],
            data['Taiwan Stocks'], data['Taiwan Stocks Percentage'],
            data['US Stocks'], data['US Stocks Percentage'],
            data['Cryptocurrency'], data['Cryptocurrency Percentage'],
            data['Savings'], data['Savings Percentage'],
            data['Total Assets']
        ))
        
        conn.commit()  # 提交事務
        conn.close()  # 關閉連接
        
        # # 更新 GUI 顯示
        self.update_portfolio_tree()

    def fetch_all_data(self):
        """ 從資料庫獲取所有資產資料 """
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM assets')
            return c.fetchall()

    def delete_data(self, id):
        """刪除指定ID的資產記錄"""
        conn = sqlite3.connect('finance_app.db')
        c = conn.cursor()
        c.execute('DELETE FROM assets WHERE id=?', (id,))
        conn.commit()
        conn.close()
        self.update_portfolio_tree()

    def update_portfolio_tree(self):
        """更新資產清單的顯示"""
        self.portfolio_tree.delete(*self.portfolio_tree.get_children())  # 清除現有的樹狀視圖項目
        conn = sqlite3.connect('finance_app.db')
        c = conn.cursor()
        c.execute('SELECT * FROM assets')
        for row in c.fetchall():
            self.portfolio_tree.insert('', 'end', text=row[0], values=row[1:])
        conn.close()

    def get_selected_id(self):
            """獲取選中項目的ID"""
            selected_item = self.portfolio_tree.selection()
            if selected_item:
                return self.portfolio_tree.item(selected_item[0])['text']
            return None

###########計算百分比和總資產############
    def calculate_percentages_and_total(self):
    
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

####################
def main():
    root = tk.Tk()
    app = FinanceApp(root)
    db = DatabaseManager('finance_app.db')
    
    root.mainloop()

if __name__ == "__main__":
    main()
