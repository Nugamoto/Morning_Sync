import requests
from requests.auth import HTTPBasicAuth

def send_message(message):
    requests.post(f"https://api.twilio.com/2010-04-01/Accounts/{os.get(ACCOUNT_SID)}/Messages.json", data={"From": "whatsapp:" + os.get(SENDER_WHATSAPP_NUMBER), "To": "whatsapp:" + receiver_whatsapp_number, "Body": message}, auth=HTTPBasicAuth(os.get(API_KEY_SID), os.get(API_KEY_SECRET)))