import os
import requests
from twilio.rest import Client
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import time

load_dotenv()
CHAT_SERVICE_SID = os.getenv("CHAT_SERVICE_SID")
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
API_KEY_SID = os.getenv("API_KEY_SID")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
SENDER_NUMBER = os.getenv("SENDER_NUMBER")
RECEIVER_NUMBER = os.getenv("RECEIVER_NUMBER")

def send_message(message):
    response = requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/Messages.json",
        data={
            "From": f"whatsapp:{SENDER_NUMBER}",
            "To": f"whatsapp:{RECEIVER_NUMBER}",
            "Body": message
        },
        auth=HTTPBasicAuth(API_KEY_SID, API_KEY_SECRET)
    )
    return response

def save_last_message_timestamp(timestamp):
    with open("last_message_timestamp.txt", "w") as file:
        file.write(timestamp)

def load_last_message_timestamp():
    if os.path.exists("last_message_timestamp.txt"):
        with open("last_message_timestamp.txt", "r") as file:
            return file.read()
    return None

def fetch_latest_whatsapp_message():
    client = Client(API_KEY_SID, API_KEY_SECRET, ACCOUNT_SID)
    messages = client.messages.list(limit=5)

    latest_message = None
    latest_timestamp = None

    for message in messages:
        if message.from_ == f"whatsapp:{RECEIVER_NUMBER}":
            message_timestamp = message.date_created.isoformat()
            last_saved_timestamp = load_last_message_timestamp()

            if last_saved_timestamp is None or message_timestamp > last_saved_timestamp:
                latest_message = message.body
                latest_timestamp = message_timestamp
                break

    if latest_message:
        save_last_message_timestamp(latest_timestamp)
        return latest_message
    return None


send_message("Hello! This is an automatic reply from the bot.")

print("Checking for new messages...")
while True:
    new_message = fetch_latest_whatsapp_message()
    if new_message:
        print("New Message:", new_message)
        send_message(f"Thanks for your message: {new_message}")
    time.sleep(1)

