from flask import Flask, render_template, request
from check_reminders import check_and_send_reminders
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Medication Reminder is running! 💊'

@app.route('/remind')
def remind():
    check_and_send_reminders()
    return 'Reminder check triggered successfully! ✅'

@app.route('/add', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        medicine = request.form['medicine']
        dosage = request.form['dosage']
        time = request.form['time']

        new_entry = {
            "medicine": medicine,
            "dosage": dosage,
            "time": time
        }

        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(new_entry)

        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

        return "Medicine added successfully! 💊"

    return render_template('add.html')
