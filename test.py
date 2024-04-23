import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def plot_financial_growth_tk(results, window):
    # 使用深色主題
    plt.style.use('dark_background')

    # 設定matplotlib圖表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), dpi=100)
    fig.patch.set_facecolor('#333333')  # 深色背景

    # 從results提取數據
    years = [result['year'] for result in results]
    accumulated_investments = [result['accumulated_investment'] for result in results]
    dividend_incomes = [result['dividend_income'] for result in results]
    monthly_expenses = [result['monthly_expense']*12 for result in results]

    # 第一張圖顯示 dividend_income 和 monthly_expense
    bars = ax1.bar(years, dividend_incomes, color='#ff7f0e', width=0.4, label='Dividend Income')
    line1, = ax1.plot(years, monthly_expenses, color='#ffffff', marker='x', linestyle='-', label='Monthly Expense')
    
    # 標註dividend_income和monthly_expense的數據點
    for bar, div, exp in zip(bars, dividend_incomes, monthly_expenses):
        ax1.text(bar.get_x() + bar.get_width()/2, div, f"{int(div)}", ha='center', va='bottom', color='white', fontsize=8)
        ax1.text(bar.get_x() + bar.get_width()/2, exp, f"{int(exp)}", ha='center', va='bottom', color='white', fontsize=8)
    
    ax1.set_ylabel('Values ($)', color='white')
    ax1.legend(loc='upper left', frameon=False, fontsize=8)
    ax1.set_title('Dividend Income and Monthly Expenses Over Years', fontsize=12, color='white')

    # 第二張圖顯示 accumulated_investments
    bars2 = ax2.bar(years, accumulated_investments, color='#1f77b4', width=0.4, label='Accumulated Investment')
    
    # 標註accumulated_investments的數據點
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{int(bar.get_height())}", ha='center', va='bottom', color='white', fontsize=8)

    ax2.set_xlabel('Age', fontsize=12, fontweight='bold', color='white')
    ax2.set_ylabel('Accumulated Investment ($)', color='white')
    ax2.legend(loc='upper left', frameon=False, fontsize=8)
    ax2.set_title('Accumulated Investments Over Years', fontsize=12, color='white')

    # 設定X軸的刻度，以顯示每一個年齡
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))

    # 將matplotlib繪製的圖表添加到Tkinter窗口
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def main():
    # 創建Tkinter主窗口
    window = tk.Tk()
    window.title("Financial Growth Visualization")

    # 示範數據
    # Example usage
    results =  [{'year': 27, 'accumulated_investment': 345200.0, 'dividend_income': 5700.0, 'monthly_expense': 30900.0}, 
                {'year': 28, 'accumulated_investment': 610016.0, 'dividend_income': 13056.0, 'monthly_expense': 31827.0}, 
                {'year': 29, 'accumulated_investment': 896017.28, 'dividend_income': 21000.48, 'monthly_expense': 32781.81},
                {'year': 30, 'accumulated_investment': 1204898.6624, 'dividend_income': 29580.5184, 'monthly_expense': 33765.264299999995}, 
                {'year': 31, 'accumulated_investment': 1538490.555392, 'dividend_income': 38846.959872, 'monthly_expense': 34778.222229}, 
                {'year': 32, 'accumulated_investment': 1898769.7998233598, 'dividend_income': 48854.716661759994, 'monthly_expense': 35821.56889587}, 
                {'year': 33, 'accumulated_investment': 2287871.3838092284, 'dividend_income': 59663.093994700794, 'monthly_expense': 36896.2159627461}, 
                {'year': 34, 'accumulated_investment': 2708101.0945139667, 'dividend_income': 71336.14151427685, 'monthly_expense': 38003.102441628485}, 
                {'year': 35, 'accumulated_investment': 3161949.182075084, 'dividend_income': 83943.032835419, 'monthly_expense': 39143.19551487734}, 
                {'year': 36, 'accumulated_investment': 3652105.116641091, 'dividend_income': 97558.47546225252, 'monthly_expense': 40317.49138032366}, 
                {'year': 37, 'accumulated_investment': 4181473.5259723784, 'dividend_income': 112263.15349923274, 'monthly_expense': 41527.01612173337}, 
                {'year': 38, 'accumulated_investment': 4753191.408050168, 'dividend_income': 128144.20577917135, 'monthly_expense': 42772.82660538537}, 
                {'year': 39, 'accumulated_investment': 5370646.7206941815, 'dividend_income': 145295.74224150504, 'monthly_expense': 44056.01140354694}, 
                {'year': 40, 'accumulated_investment': 6037498.458349716, 'dividend_income': 163819.40162082543, 'monthly_expense': 45377.69174565335}, 
                {'year': 41, 'accumulated_investment': 6757698.335017693, 'dividend_income': 183824.95375049146, 'monthly_expense': 46739.02249802295}, 
                {'year': 42, 'accumulated_investment': 7535514.201819109, 'dividend_income': 205430.95005053078, 'monthly_expense': 48141.193172963634}, 
                {'year': 43, 'accumulated_investment': 8375555.337964637, 'dividend_income': 228765.42605457327, 'monthly_expense': 49585.42896815255}, 
                {'year': 44, 'accumulated_investment': 9282799.765001807, 'dividend_income': 253966.6601389391, 'monthly_expense': 51072.99183719713}, 
                {'year': 45, 'accumulated_investment': 10262623.746201951, 'dividend_income': 281183.99295005423, 'monthly_expense': 52605.18159231304}, 
                {'year': 46, 'accumulated_investment': 11320833.645898107, 'dividend_income': 310578.7123860585, 'monthly_expense': 54183.337040082435}, 
                {'year': 47, 'accumulated_investment': 12463700.337569956, 'dividend_income': 342325.0093769432, 'monthly_expense': 55808.83715128491}, 
                {'year': 48, 'accumulated_investment': 13697996.364575552, 'dividend_income': 376611.01012709865, 'monthly_expense': 57483.10226582346}, 
                {'year': 49, 'accumulated_investment': 15031036.073741596, 'dividend_income': 413639.8909372665, 'monthly_expense': 59207.59533379816}, 
                {'year': 50, 'accumulated_investment': 16470718.959640924, 'dividend_income': 453631.0822122479, 'monthly_expense': 60983.82319381211}
                ]

    # 呼叫繪圖函數
    plot_financial_growth_tk(results, window)

    # 開始Tkinter事件循環
    window.mainloop()

if __name__ == "__main__":
    main()



# https://medium.com/@fareedkhandev/modern-gui-using-tkinter-12da0b983e22