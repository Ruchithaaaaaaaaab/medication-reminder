from twilio.rest import Client
import os

def send_whatsapp_message(message):
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    receiver = os.environ.get("RECEIVER_PHONE_NUMBER")  # Format: whatsapp:+91xxxxxxxxxx

    if not account_sid or not auth_token or not receiver:
        print("❌ Missing environment variables: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, or RECEIVER_PHONE_NUMBER")
        return

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Twilio sandbox number
            to=receiver,
            body=message
        )
        print(f"✅ WhatsApp message sent. SID: {message.sid}")
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")
