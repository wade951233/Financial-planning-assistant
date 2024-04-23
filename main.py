import tkinter as tk
from tkinter import ttk
from ui_components import planning_widgets, recording_widgets  # 引入創建小組件的函數
from ui_components import plot_financial_growth_tk  # 引入繪製圖表的函數
# from finance_calculator import calculate_finances  # 引入財務計算函數
import sqlite3

class Asset_Planning_page:
    def __init__(self, master):
        # 初始化類別，設定主視窗參數
        self.master = master
        self.master.title("財務規劃APP")  # 為主視窗設定標題

        # 創建一個筆記本小組件，用於顯示多個分頁
        self.notebook = ttk.Notebook(master)  

        # 創建一個資料庫管理對象，用於處理資產記錄
        self.db_manager = recording_page('finance_app.db')  
        self.labels = {}  # 創建一個字典來儲存標籤組件

        # 定義不同分頁的設定，包括分頁標題和相應的函數調用
        pages = {
            '規劃趨勢': ('expenses_frame', plot_financial_growth_tk),  # 目前不添加任何小組件
            '資產規劃': ('planning_frame', planning_widgets),
            '資產紀錄': ('recording_frame', lambda frame, self: recording_widgets(frame, self, self.db_manager)),
            
            '紀錄報告': ('investments_frame', None)  # 目前不添加任何小組件
        }

        # 動態生成每個分頁，並關聯相應的框架和小組件
        for text, (attr, func) in pages.items():
            frame = ttk.Frame(self.notebook)  # 為每個分頁創建一個框架
            self.notebook.add(frame, text=text)  # 將框架加入筆記本，設定標籤
            if func:
                func(frame, self)  # 如果有指定函數，則呼叫此函數來填充框架
            setattr(self, attr, frame)  # 為框架設定屬性，便於後續訪問

        self.notebook.pack(expand=1, fill="both")  # 將筆記本展開填充整個視窗
    

    def perform_calculation(self):
        # 執行財務計算的方法
        try:
            # 從輸入欄位獲取數據並轉換成適當的數字類型
            self.params = {
                "start_age": int(self.entries["start_age"].get()),  # 起始年齡
                "retirement_age": int(self.entries["retirement_age"].get()),  # 退休年齡
                "monthly_expense": int(self.entries["monthly_expense"].get()),  # 每月支出
                "inflation_rate": int(self.entries["inflation_rate"].get()),  # 通脹率
                "monthly_investment": int(self.entries["monthly_investment"].get()),  # 每月投資額
                "monthly_growth": int(self.entries["monthly_growth"].get()),  # 每月增長率
                "annual_investment": int(self.entries["annual_investment"].get()),  # 年度一次性投資額
                "annual_growth": int(self.entries["annual_growth"].get()),  # 年度增長率
                "initial_amount": int(self.entries["initial_amount"].get()),  # 初始投資金額
                "dividend_yield": int(self.entries["dividend_yield"].get()),  # 股息收益率
                "capital_gain_rate": int(self.entries["capital_gain_rate"].get())  # 資本增值率
            }

            print("Parameters:", self.params)  # 輸出當前參數設定，用於檢查
            results = self.calculate_finances(**self.params)  # 根據參數進行財務計算
            self.update_tree(results, self.params['start_age'])  # 根據計算結果更新樹狀視圖

        except ValueError:
            # 處理數據輸入錯誤，清空結果並提示錯誤信息
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", text="錯誤", values=("請輸入有效的數值", ""))

    def calculate_finances(self, start_age, retirement_age, monthly_expense, inflation_rate, monthly_investment, monthly_growth,
                           annual_investment, annual_growth, initial_amount, dividend_yield, capital_gain_rate):
                years = retirement_age - start_age  # 計算退休年限
                results = []  # 創建一個列表來保存每一年的財務狀況
                future_value = initial_amount  # 初始化未來價值為起始金額
                print("起始金額 = ", initial_amount)
                print("每月投資金額*12 = ", monthly_investment * 12)
                print("股息收入 = ", (initial_amount * (dividend_yield / 100) + monthly_investment * 12 * (dividend_yield / 100) * 0.5))
                print("增值金額 = ", (initial_amount * (capital_gain_rate / 100) + monthly_investment * 12 * (capital_gain_rate / 100) * 0.5))
                print("未來每月支出 = ", monthly_expense)
                print("-------------")
                accumulated_investment = initial_amount  # 累積投資金額初值為起始金額
                monthly_expense = monthly_expense
                for year in range(start_age, retirement_age + 1):  # 遍歷從起始年齡到目標退休年齡的每一年
                    # 股息收入
                    annual_dividend_income = accumulated_investment * (dividend_yield / 100) + monthly_investment * 12 * (dividend_yield / 100) * 0.5
                    # 增值收益
                    annual_capital_gain = accumulated_investment * (capital_gain_rate / 100) + monthly_investment * 12 * (capital_gain_rate / 100) * 0.5
                    #累積投資金額
                    accumulated_investment += (monthly_investment * 12 + annual_dividend_income + annual_capital_gain + annual_investment)
                    #未來每月支出
                    monthly_expense = monthly_expense * (1+(inflation_rate/100))
                    # 將當前年份的財務狀況添加到結果列表中
                    results.append({'year': year, 'accumulated_investment': accumulated_investment, 'dividend_income': annual_dividend_income, 'monthly_expense': monthly_expense })
                    print(f"Year {year}: 累積投資金額 = {accumulated_investment}, 股息收入 = {annual_dividend_income}, 增值金額 = {annual_capital_gain}, 未來每月支出 = {monthly_expense}")
                    print("-------------")
                # print("results = ", results)

                return results
    
    def update_tree(self, results, start_age):
        # 清空並更新樹狀視圖的方法
        for item in self.tree.get_children():
            self.tree.delete(item)  # 清除現有項目
        # 根據計算結果逐年更新顯示
        for year, finances in enumerate(results, start=start_age):
            self.tree.insert("", "end", text=str(year), values=(
                f"${finances['accumulated_investment']:.0f}",
                f"${finances['dividend_income']:.0f}",
                f"${finances['monthly_expense']:.0f}"
            ))


class recording_page:
    def __init__(self, db_name):
        """ 初始化資料庫管理員類 """
        self.db_name = db_name
        self.entries = {}  # Initialize the entries dictionary
        self.labels = {}  

    def db_connect(self):
        """ 建立並返回資料庫連接 """
        return sqlite3.connect(self.db_name)

    def db_add_data(self):
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
        self.db_update_portfolio_tree()

    def db_fetch_all_data(self):
        """ 從資料庫獲取所有資產資料 """
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM assets')
            return c.fetchall()

    def db_delete_data(self, id):
        """刪除指定ID的資產記錄"""
        conn = sqlite3.connect('finance_app.db')
        c = conn.cursor()
        c.execute('DELETE FROM assets WHERE id=?', (id,))
        conn.commit()
        conn.close()
        self.db_update_portfolio_tree()

    def db_update_portfolio_tree(self):
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

###########
# 計算百分比和總資產
###########
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

        self.db_update_portfolio_tree()

def main():
   
    
    window = tk.Tk()
    planning = Asset_Planning_page(window)
    recording = recording_page('finance_app.db')
    
    window.mainloop()

if __name__ == "__main__":
    main()
