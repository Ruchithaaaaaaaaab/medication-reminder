from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'medicines.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        name = request.form['name']
        dosage = request.form['dosage']
        time = request.form['time']
        medicines = load_data()
        medicines.append({
            'name': name,
            'dosage': dosage,
            'time': time
        })
        save_data(medicines)
        return redirect(url_for('view_medicines'))
    return render_template('add_medicine.html')

@app.route('/medicines')
def view_medicines():
    medicines = load_data()
    return render_template('view_medicines.html', medicines=medicines)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

from check_reminders import check_and_send_reminders

@app.route("/check")
def run_reminder_now():
    check_and_send_reminders()
    return "Reminder check complete"

from check_reminders import check_and_send_reminders

@app.route("/remind")
def remind():
    from check_reminders import run_reminders
    run_reminders()
    return "Reminders checked and messages sent!"


