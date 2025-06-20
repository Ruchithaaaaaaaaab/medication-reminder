import os
from twilio.rest import Client

ACCOUNT_SID = os.environ.get("TWILIO_SID")
AUTH_TOKEN = os.environ.get("TWILIO_TOKEN")
FROM_WHATSAPP_NUMBER = "whatsapp:+14155238886"

def send_whatsapp(to_number, name, dosage):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    body = f"💊 Reminder:\nTake {name} - {dosage}"
    message = client.messages.create(
        body=body,
        from_=FROM_WHATSAPP_NUMBER,
        to=f"whatsapp:{to_number}"
    )
    print("✅ WhatsApp sent:", message.sid)
