import tkinter as tk
from app import App
import customtkinter
# 創建並運行應用程序
def main():
    # root = tk.Tk()
    root = customtkinter.CTk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()