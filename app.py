from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from whatsapp import send_whatsapp_message  # This must be in the same directory
import os

app = Flask(__name__)

DATABASE = 'reminders.db'
PORT = int(os.environ.get("PORT", 10000))  # for Render to detect

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS reminders
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         medicine TEXT NOT NULL,
                         dosage TEXT NOT NULL,
                         time TEXT NOT NULL)''')
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminders")
    reminders = cursor.fetchall()
    conn.close()
    return render_template('index.html', reminders=reminders)

@app.route('/add-reminder', methods=['POST'])
def add_reminder():
    medicine = request.form['medicine']
    dosage = request.form['dosage']
    time = request.form['time']

    with sqlite3.connect(DATABASE) as conn:
        conn.execute("INSERT INTO reminders (medicine, dosage, time) VALUES (?, ?, ?)",
                     (medicine, dosage, time))
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_reminder(id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("DELETE FROM reminders WHERE id = ?", (id,))
    return redirect('/')

@app.route('/remind')
def check_reminders():
    now = datetime.now().strftime("%H:%M")
    print(f"🔍 Checking reminders at {now}")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminders WHERE time = ?", (now,))
    reminders = cursor.fetchall()
    conn.close()

    if reminders:
        for reminder in reminders:
            msg = f"💊 Reminder: Take {reminder[1]} ({reminder[2]}) now!"
            print(f"📤 Sending: {msg}")
            send_whatsapp_message(msg)
    else:
        print("⏰ No reminders to send now.")

    return "Notification check complete"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
