from flask import Flask
from check_reminders import check_and_send_reminders

app = Flask(__name__)

@app.route('/')
def home():
    return 'Medication Reminder is running! 💊'

@app.route('/remind')
def remind():
    check_and_send_reminders()
    return 'Reminder check triggered successfully! ✅'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
