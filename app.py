from tkinter import ttk
from tab_pages import TabPageOne, TabPageTwo, TabPageThree, TabPageFour, db_control
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("理財小幫手")  # 設定應用窗口的標題
        
        # 初始化資料庫
        self.db = db_control()  # 創建 db_control 類的實例，用於管理資料庫操作
        
        # 創建標籤頁控件
        self.tab_control = ttk.Notebook(master)  # 在主窗口中創建 Notebook 控件，用於容納多個標籤頁
        
        # 創建各個標籤頁並傳遞必要的參數
        self.tab1 = TabPageOne(self.tab_control, self)  # 創建第一個標籤頁，傳入 App 實例本身
        self.tab2 = TabPageTwo(self.tab_control)  # 創建第二個標籤頁
        self.tab3 = TabPageThree(self.tab_control, self.db)  # 創建第三個標籤頁，並傳入資料庫控制器實例
        self.tab4 = TabPageFour(self.tab_control)  # 創建第四個標籤頁
        
        # 將標籤頁添加到 Notebook 控件中
        self.tab_control.add(self.tab1, text='資產規劃')  # 第一個標籤頁的名稱
        self.tab_control.add(self.tab2, text='資產規劃報表')  # 第二個標籤頁的名稱
        self.tab_control.add(self.tab3, text='財務紀錄')  # 第三個標籤頁的名稱
        self.tab_control.add(self.tab4, text='財務紀錄報表')  # 第四個標籤頁的名稱
        self.tab_control.grid(row=0, column=0, sticky="nsew")  # 使用 grid 布局管理器定位 Notebook 控件
        
        # 設置主窗口的格線配置，使得標籤頁控件能夠隨窗口大小變化自動調整
        self.master.grid_columnconfigure(0, weight=1)  # 設定列的伸縮權重
        self.master.grid_rowconfigure(0, weight=1)  # 設定行的伸縮權重
