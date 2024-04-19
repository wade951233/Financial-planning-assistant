# 計算投資增長和股息收入
def calculate_finances(start_age, retirement_age, monthly_expense, inflation_rate, monthly_investment, monthly_growth,
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

    return results