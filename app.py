from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3
import os
from email_utils import init_mail, send_email_notification

app = Flask(__name__)
DATABASE = 'reminders.db'
PORT = int(os.environ.get("PORT", 10000))

# Initialize DB and mail
init_mail(app)

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine TEXT NOT NULL,
            dosage TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    reminders = conn.execute("SELECT * FROM reminders").fetchall()
    conn.close()
    return render_template('index.html', reminders=reminders)

@app.route('/add-reminder', methods=['POST'])
def add_reminder():
    medicine = request.form['medicine']
    dosage = request.form['dosage']
    time = request.form['time']
    conn = sqlite3.connect(DATABASE)
    conn.execute("INSERT INTO reminders (medicine, dosage, time) VALUES (?, ?, ?)", (medicine, dosage, time))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_reminder(id):
    conn = sqlite3.connect(DATABASE)
    conn.execute("DELETE FROM reminders WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/remind')
def remind():
    now = datetime.now().strftime("%H:%M")
    conn = sqlite3.connect(DATABASE)
    reminders = conn.execute("SELECT * FROM reminders WHERE time = ?", (now,)).fetchall()
    conn.close()

    for r in reminders:
        message = f"💊 Reminder: Take {r[1]} ({r[2]})"
        send_email_notification("Medication Reminder", message)

    return "✅ Reminder check complete", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
