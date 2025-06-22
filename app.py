from flask import Flask, render_template, request, redirect
from datetime import datetime
from pytz import timezone
import sqlite3
import os
from whatsapp import send_whatsapp_message

app = Flask(__name__)
DATABASE = 'reminders.db'
PORT = int(os.environ.get("PORT", 10000))

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
    # Get current IST time
    utc_now = datetime.utcnow()
    ist_now = utc_now.astimezone(timezone("Asia/Kolkata"))
    now = ist_now.strftime("%H:%M")

    print("🕒 IST Time Check:", now)

    conn = sqlite3.connect(DATABASE)
    reminders = conn.execute("SELECT * FROM reminders WHERE time = ?", (now,)).fetchall()
    conn.close()

    print("🔍 Found reminders:", len(reminders))

    for r in reminders:
        message = f"💊 WhatsApp Reminder: Take {r[1]} ({r[2]})"
        print("📲 Sending WhatsApp message:", message)
        send_whatsapp_message(message)

    return "✅ Reminder check complete", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
