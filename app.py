from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3
from whatsapp import send_whatsapp_message



app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('reminder.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    reminders = conn.execute('SELECT * FROM reminders').fetchall()
    conn.close()
    return render_template('index.html', reminders=reminders)

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

@app.route('/delete/<int:id>')
def delete_reminder(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM reminders WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/remind')
def remind():
    now = datetime.now().strftime('%H:%M')
    conn = get_db_connection()
    reminders = conn.execute('SELECT * FROM reminders WHERE time = ?', (now,)).fetchall()
    for reminder in reminders:
        message = f"⏰ Reminder: Take {reminder['medicine']} ({reminder['dosage']})"
        send_whatsapp_message(message)

    conn.close()
    return "Reminder check triggered ✅"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
