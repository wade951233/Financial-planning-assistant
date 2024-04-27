import sqlite3

def init_db():
    conn = sqlite3.connect('finance_app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year TEXT NOT NULL,
            month TEXT NOT NULL,
            taiwan_stocks REAL,
            taiwan_stocks_percentage REAL,
            us_stocks REAL,
            us_stocks_percentage REAL,
            cryptocurrency REAL,
            cryptocurrency_percentage REAL,
            savings REAL,
            savings_percentage REAL,
            total_assets REAL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
