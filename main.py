"""
main.py

This module starts the WhatsApp bot and the reminder service.
It uses threads to run the reminder loop in parallel with message checking.
"""

from services.new_twilio_api import check_new_messages, send_message
from services.google_calendar import reminder_loop
import threading

def main():
    """
    Starts the WhatsApp bot and the reminder service.

    - Initializes the reminder loop in a separate thread.
    - Starts checking for incoming WhatsApp messages.
    """
    print("🤖 WhatsApp-Bot wird gestartet...")
    threading.Thread(target=lambda: reminder_loop(send_message), daemon=True).start()
    print("💬 Warte auf eingehende Nachrichten...")
    check_new_messages()

if __name__ == "__main__":
    main()