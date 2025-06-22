from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3
from whatsapp import send_whatsapp_message  # Make sure this file and function are correct

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('reminder.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route: show all reminders
@app.route('/')
def index():
    conn = get_db_connection()
    reminders = conn.execute('SELECT * FROM reminders').fetchall()
    conn.close()
    return render_template('index.html', reminders=reminders)

# Add new reminder
@app.route('/add-reminder', methods=['POST'])
def add_reminder():
    medicine = request.form['medicine']
    dosage = request.form['dosage']
    time = request.form['time']

    conn = get_db_connection()
    conn.execute('INSERT INTO reminders (medicine, dosage, time) VALUES (?, ?, ?)',
                 (medicine, dosage, time))
    conn.commit()
    conn.close()
    return redirect('/')

# Delete a reminder by ID
@app.route('/delete/<int:id>')
def delete_reminder(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM reminders WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Reminder check: sends WhatsApp if time matches
@app.route('/remind')
def remind():
    now = datetime.now().strftime('%H:%M')
    print(f"[{now}] 🔎 Checking for reminders...")

    conn = get_db_connection()
    reminders = conn.execute('SELECT * FROM reminders WHERE time = ?', (now,)).fetchall()

    if reminders:
        print(f"✅ Found {len(reminders)} reminder(s) for now.")
    else:
        print("⚠️ No reminders match the current time.")

    for reminder in reminders:
        message = f"⏰ Reminder: Take {reminder['medicine']} ({reminder['dosage']})"
        print(f"📤 Sending WhatsApp: {message}")
        try:
            sid = send_whatsapp_message(message)
            print(f"✅ Message sent! SID: {sid}")
        except Exception as e:
            print(f"❌ Error sending WhatsApp: {e}")

    conn.close()
    return "Reminder check complete."

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
