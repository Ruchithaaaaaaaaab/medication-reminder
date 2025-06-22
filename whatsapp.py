from twilio.rest import Client
import os

def send_whatsapp_message(message):
    
    try:
        client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',
        to=receiver_number
        )
        print("✅ Message sent")
    
    except Exception as e:
        print("❌ Error sending WhatsApp message:", e)
        print("⚠️ Attempting to send WhatsApp message...")
    
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    receiver_number = os.environ.get('RECEIVER_PHONE_NUMBER')
    print(f"📨 Sending to: {receiver_number}")
    print(f"📨 Message content: {message}")

    client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',  # Twilio sandbox number
        to=receiver_number
    )
    print("✅ WhatsApp message sent.")
