from datetime import datetime
import json
import os
from utils.whatsapp import send_whatsapp

DATA_FILE = 'medicines.json'
USER_PHONE = "+91xxxxxxxxxx"  # Replace with your WhatsApp number

def check_reminders():
    now = datetime.now().strftime('%H:%M')
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, 'r') as f:
        medicines = json.load(f)
    for med in medicines:
        if med['time'] == now:
            send_whatsapp(USER_PHONE, med['name'], med['dosage'])

if __name__ == "__main__":
    check_reminders()
