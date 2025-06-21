import os
from twilio.rest import Client
import json
from datetime import datetime

def check_and_send_reminders():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)

        now = datetime.now().strftime("%H:%M")

        for item in data:
            if item["time"] == now:
                send_sms(item["medicine"], item["dosage"])

    except Exception as e:
        print("Error in check_and_send_reminders:", str(e))

def send_sms(medicine, dosage):
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_PHONE_NUMBER")
    to_number = os.environ.get("TO_PHONE_NUMBER")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Reminder: Take {medicine} ({dosage}) 💊",
        from_=from_number,
        to=to_number
    )

    print("Message sent:", message.sid)
