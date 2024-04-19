import tkinter as tk
from tkinter import ttk
from ui_components import create_widgets  # 引入創建小組件的函數
from finance_calculator import calculate_finances  # 引入財務計算函數

class FinanceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("財務規劃APP")  # 設置應用程式視窗標題
        self.notebook = ttk.Notebook(master)  # 創建一個筆記本小組件，用來管理多個頁面
        self.main_frame = ttk.Frame(self.notebook)  # 創建主頁面的框架
        self.notebook.add(self.main_frame, text='主頁面')  # 將主頁面框架添加到筆記本中
        self.notebook.pack(expand=1, fill="both")  # 放置筆記本並允許擴展和填充空間
        create_widgets(self.main_frame, self)  # 呼叫創建小組件的函數來設置界面
        
        # 初始化四個新頁面
        for i in range(4):
            self.open_new_page()  # 呼叫開新頁面的方法

    def perform_calculation(self):
        try:
            # 將輸入欄位的數據轉換為適當的數字類型
            self.params = {name: float(entry.get()) if name not in ['start_age', 'retirement_age'] else int(entry.get())
                           for name, entry in self.entries.items()}
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

    def open_new_page(self):
        new_frame = ttk.Frame(self.notebook)  # 創建一個新的框架用於新頁面
        self.notebook.add(new_frame, text=f'新頁面 {len(self.notebook.tabs())}')  # 添加新頁面到筆記本
        tk.Label(new_frame, text="這是一個新的頁面").pack(pady=20)  # 新頁面中添加標籤顯示文字
        close_button = tk.Button(new_frame, text="關閉此頁面", command=lambda: self.close_page(new_frame))  # 添加關閉頁面的按鈕
        close_button.pack(pady=20)

    def close_page(self, frame):
        index = self.notebook.index(frame)  # 獲取欲關閉頁面的索引
        self.notebook.forget(index)  # 移除指定索引的頁面
