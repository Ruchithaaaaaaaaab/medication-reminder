import sqlite3

conn = sqlite3.connect('reminder.db')
rows = conn.execute('SELECT * FROM reminders').fetchall()
for row in rows:
    print(row)
conn.close()
