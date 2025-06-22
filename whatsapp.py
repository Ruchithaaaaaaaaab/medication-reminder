from twilio.rest import Client
import os

def send_whatsapp_message(body):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    from_number = os.environ['TWILIO_PHONE_NUMBER']
    to_number = os.environ['RECEIVER_PHONE_NUMBER']

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=f'whatsapp:{from_number}',
        to=f'whatsapp:{to_number}'
    )

    return message.sid

