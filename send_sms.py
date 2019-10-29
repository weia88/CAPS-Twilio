import os
from twilio.rest import Client


account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

client = client(account_sid, auth_token)

client.messages.creat(
    to=os.environ["MY_PHONE_NUMBER"],
    from_="14159219412",
    body="This is a test message"
)
