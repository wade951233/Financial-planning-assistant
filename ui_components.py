import tkinter as tk
from tkinter import ttk
############
# 資產規劃頁面
############
def planning_widgets(frame, app):
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
        
        # Reduce padx and pady to minimize space between label and entry
        label.grid(row=row, column=0, padx=(10, 2), pady=2, sticky="w")  # Align right to the grid cell end
        entry.grid(row=row, column=1, padx=(2, 10), pady=2, sticky="w")  # Expand entry to fill the cell width
        
        # Save the entry widget in the app entries dictionary with 'name' as the key
        app.entries[name] = entry
        # Increment the row index for the next label-entry pair
        row += 1
    # Configure the column 1 to use extra space by weighting
    frame.grid_columnconfigure(1, weight=1)

    app.calc_button = tk.Button(frame, text="計算", command=app.perform_calculation)
    app.calc_button.grid(row=row, column=1, columnspan=2, pady=10, sticky="w")

    # app.open_new_page_button = tk.Button(frame, text="進入新頁面", command=app.open_new_page)
    # app.open_new_page_button.grid(row=row+1, column=1, columnspan=2, pady=10, sticky="w")

    app.tree = ttk.Treeview(frame, columns=("accumulated_investment", "dividend_income", "monthly_expense"))
    app.tree.heading("#0", text="年齡") 
    app.tree.column("#0", width=80, minwidth=80, stretch=tk.NO)
    app.tree.heading("accumulated_investment", text="累積投資金額 ($)")
    app.tree.heading("dividend_income", text="股息收入 ($)")
    app.tree.heading("monthly_expense", text="未來預計支出/每月($)")
    app.tree.grid(row=row+1, column=0, columnspan=2, padx=5, pady=(2, 10), sticky="ew")  # 修正 padding 和對齊
   
############   
#   資產紀錄頁面  #
############
def recording_widgets(frame, app, db):
    #tk.Label(frame, text="這是一個新的頁面", font=('Arial', 16)).grid(row=0, column=0, columnspan=5, pady=20, padx=10, sticky='ew')

    recording_parameters = [
        ("月份", "Month", 4, "entry"),
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
        label = tk.Label(frame, text=label_text)
        label.grid(row=row, column=0, padx=(10, 2), pady=2, sticky="e")
        
        if widget_type == "entry":
            widget = tk.Entry(frame)
            widget.insert(0, default_value)
            widget.grid(row=row, column=1, padx=(2, 10), pady=2, sticky="w")
            db.entries[name] = widget
        elif widget_type == "label":
            widget = tk.Label(frame, text=f"{default_value:.2f}")
            widget.grid(row=row, column=1, padx=(2, 10), pady=2, sticky="w")
            db.labels[name] = widget
            
        row += 1


    app.update_button = tk.Button(frame, text="紀錄資料", command=db.add_data)
    app.update_button.grid(row=row, column=0, columnspan=2, pady=10, sticky="w")

    app.calculate_button = tk.Button(frame, text="計算佔比和總資產", command=db.calculate_percentages_and_total)
    app.calculate_button.grid(row=row, column=1, columnspan=2, pady=10, sticky="w")

    app.delete_record_button = tk.Button(frame, text="刪除資料", command=lambda: db.delete_data(db.get_selected_id()))
    app.delete_record_button.grid(row=row, column=2, pady=10, sticky="w")

    
    # 配置 Treeview 控件，用於顯示各項資產數據
    columns = ("月份", "台股", "台股佔比 (%)", "美股", "美股佔比 (%)", "虛擬貨幣", "虛擬貨幣佔比 (%)", "活存", "活存佔比 (%)", "總資產 ($)")
    db.portfolio_tree = ttk.Treeview(frame, columns=columns, height=8, padding=5)
    db.portfolio_tree.heading("#0", text="資料 ID", anchor='w')
    db.portfolio_tree.column("#0",width=80, minwidth=80, stretch=tk.NO)
    # 為 Treeview 的每一列設置標題和列寬等屬性
    for col in columns:
        # 設置列標題，將列名中的底線替換為空格，並設置文本對齊方式為左對齊
        db.portfolio_tree.heading(col, text=col, anchor='w')
        # 設置列的寬度、最小寬度，並禁用伸縮
        db.portfolio_tree.column(col, width=80, minwidth=80, stretch=tk.NO)

    
    # 將 Treeview 控件添加到布局中，放置於按鈕下方
    row += 1  # 增加 row 變數，以使 Treeview 在按鈕下方的新行開始
    db.portfolio_tree.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    # 設定框架的列配置，使第二列有彈性（權重為1），可以隨窗口大小調整而伸縮
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
