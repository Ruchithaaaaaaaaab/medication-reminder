import sqlite3
conn = sqlite3.connect('reminder.db')
conn.execute('''CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine TEXT NOT NULL,
    dosage TEXT NOT NULL,
    time TEXT NOT NULL
)''')
conn.commit()
conn.close()
