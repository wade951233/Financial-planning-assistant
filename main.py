import tkinter as tk
from tkinter import ttk
from ui_components import planning_widgets  # 引入創建小組件的函數
from ui_components import recording_widgets  # 引入創建小組件的函數
from finance_calculator import calculate_finances  # 引入財務計算函數

class FinanceApp:
    def __init__(self, master):

        self.master = master
        self.master.title("財務規劃APP")  # 設置應用程式視窗標題
        self.notebook = ttk.Notebook(master)  # 創建一個筆記本小組件，用來管理多個頁面

        # 在筆記本中設立4個分頁
        self.planning_frame = ttk.Frame(self.notebook)  # 創建「資產規劃」的框架
        self.notebook.add(self.planning_frame, text='資產規劃')  # 將「資產規劃」框架添加到筆記本中
        planning_widgets(self.planning_frame, self)  # 呼叫創建小組件的函數來設置界面


        self.recording_frame = ttk.Frame(self.notebook)  # 創建「資產紀錄」分頁的框架
        self.notebook.add(self.recording_frame, text='資產紀錄')  # 將「資產紀錄」分頁添加到筆記本中
        recording_widgets(self.recording_frame, self)

        self.expenses_frame = ttk.Frame(self.notebook)  # 創建「支出」分頁的框架
        self.notebook.add(self.expenses_frame, text='支出')  # 將「支出」分頁添加到筆記本中
        
        self.investments_frame = ttk.Frame(self.notebook)  # 創建「投資」分頁的框架
        self.notebook.add(self.investments_frame, text='投資')  # 將「投資」分頁添加到筆記本中

        self.reports_frame = ttk.Frame(self.notebook)  # 創建「報告」分頁的框架
        self.notebook.add(self.reports_frame, text='報告')  # 將「報告」分頁添加到筆記本中

        self.notebook.pack(expand=1, fill="both")  # 放置筆記本並允許擴展和填充空間

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
####################


####################



def main():
    root = tk.Tk()
    app = FinanceApp(root)
  
    root.mainloop()

if __name__ == "__main__":
    main()
