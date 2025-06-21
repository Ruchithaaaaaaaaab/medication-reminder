from flask import Flask, render_template, request, redirect, url_for
from check_reminders import check_and_send_reminders
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            data = json.load(f)
    else:
        data = []

    return render_template('index.html', reminders=data)

@app.route('/add', methods=['POST'])
def add():
    medicine = request.form['medicine']
    dosage = request.form['dosage']
    time = request.form['time']

    new_entry = {"medicine": medicine, "dosage": dosage, "time": time}

    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(new_entry)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete(index):
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            data = json.load(f)

        if 0 <= index < len(data):
            del data[index]

            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)

    return redirect(url_for('index'))

@app.route('/remind')
def remind():
    check_and_send_reminders()
    return 'Reminder check triggered ✅'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
