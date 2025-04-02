import os
import time
from datetime import datetime, timezone

from dotenv import load_dotenv
from twilio.rest import Client
from utils.formatter import (
    format_today,
    format_tomorrow,
    format_week,
    format_next_event
)

from services.google_calendar import (
    get_events_for_today,
    get_events_for_tomorrow,
    get_events_for_the_week,
    get_next_event
)

# Load .env file
load_dotenv()

# Timestamp when the bot was started (timezone-aware)
BOT_START_TIME = datetime.now(timezone.utc)

# Environment variables
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
API_KEY_SID = os.getenv("API_KEY_SID")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
CHAT_SERVICE_SID = os.getenv("CHAT_SERVICE_SID")
MY_NUMBER = os.getenv("MY_PHONE_NUMBER")
TWILIO_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Create Twilio client
client = Client(API_KEY_SID, API_KEY_SECRET, ACCOUNT_SID)

MENU_TEXT = (
    "📋 *MorningSync Menü*\n\n"
    "1️⃣ Heutige Termine\n"
    "2️⃣ Termine für morgen\n"
    "3️⃣ Termine für die Woche\n"
    "4️⃣ Nächster Termin\n\n"
    "Bitte wähle eine Option durch Senden der Zahl 1–4."
)


# Create or reuse a conversation
def get_or_create_conversation():
    """
    Creates a new Twilio conversation or reuses an existing one.
    Sends the menu only if a new conversation is created.

    Returns:
        str: The SID of the conversation.
    """
    conversations = client.conversations.v1.services(CHAT_SERVICE_SID).conversations.list(limit=20)
    for conv in conversations:
        if conv.friendly_name == "HackathonChat":
            return conv.sid  # Bestehende Konversation -> kein Menü senden

    # Neue Konversation erstellen
    conv = client.conversations.v1 \
        .services(CHAT_SERVICE_SID) \
        .conversations \
        .create(friendly_name="HackathonChat")

    client.conversations.v1 \
        .services(CHAT_SERVICE_SID) \
        .conversations(conv.sid) \
        .participants \
        .create(
        messaging_binding_address=MY_NUMBER,
        messaging_binding_proxy_address=TWILIO_NUMBER
    )

    # Send menu only for new conversation
    send_message(MENU_TEXT)
    return conv.sid


# Send message
def send_message(text):
    """
    Sends a message via Twilio Conversations API.

    Args:
        text (str): The message text to send.
    """
    conversation_sid = get_or_create_conversation()
    client.conversations.v1 \
        .services(CHAT_SERVICE_SID) \
        .conversations(conversation_sid) \
        .messages \
        .create(
        author="bot",
        body=text
    )
    print(f"✅ Nachricht gesendet: {text}")


def handle_incoming_message(text):
    """
    Handles incoming text messages by interpreting commands and responding accordingly.

    Args:
        text (str): The incoming message text.
    """
    text = text.strip()

    if text == "1":
        events = get_events_for_today()
        formatted = format_today(events)
    elif text == "2":
        events = get_events_for_tomorrow()
        formatted = format_tomorrow(events)
    elif text == "3":
        events = get_events_for_the_week()
        formatted = format_week(events)
    elif text == "4":
        events = get_next_event()
        formatted = format_next_event(events)
    else:
        send_message(MENU_TEXT)
        return

    send_message(formatted)


def check_new_messages():
    """
    Checks for new incoming messages in a Twilio conversation and handles them.

    Continuously polls for new messages and responds to valid commands.
    """
    conversation_sid = get_or_create_conversation()
    # Start from the time when the bot was started
    last_seen_time = BOT_START_TIME

    while True:
        messages = client.conversations.v1 \
            .services(CHAT_SERVICE_SID) \
            .conversations(conversation_sid) \
            .messages \
            .list(order="asc")

        for msg in messages:
            # Convert to timezone-aware datetime object
            msg_date = msg.date_created if isinstance(msg.date_created, datetime) else datetime.fromisoformat(msg.date_created)
            if msg_date.tzinfo is None:
                msg_date = msg_date.replace(tzinfo=timezone.utc)

            # Process only messages received after the last seen message
            if msg.author != "bot" and msg_date > last_seen_time:
                print(f"📥 Eingehend von {msg.author}: {msg.body}")
                handle_incoming_message(msg.body)
                # Update the timestamp of the last processed message
                last_seen_time = msg_date

        time.sleep(5)
