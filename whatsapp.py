from twilio.rest import Client
import os

def send_whatsapp_message(message):
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    receiver = os.environ.get("RECEIVER_PHONE_NUMBER")  # e.g. whatsapp:+91XXXXXXXXXX

    if not all([account_sid, auth_token, receiver]):
        print("❌ Missing environment variables.")
        return

    try:
        client = Client(account_sid, auth_token)
        client.messages.create(
            from_='whatsapp:+14155238886',
            to=receiver,
            body=message
        )
        print("✅ Message sent")
    except Exception as e:
        print(f"❌ Error sending message: {e}")
