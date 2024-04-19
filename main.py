import tkinter as tk
from finance_app import FinanceApp

def main():
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
