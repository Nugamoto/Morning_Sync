import time
from datetime import datetime
from colorama import Fore, Style
from dotenv import load_dotenv
import os

from services.google_calendar import (
    get_events_for_today,
    get_events_for_tomorrow,
    get_events_for_the_week,
    get_next_event,
)

from utils.formatter import (
    format_today,
    format_tomorrow,
    format_week,
    format_next_event,
)
from services.twilio_api import send_message, fetch_message

load_dotenv()
DAILY_REMINDER_TIME = os.getenv("DAILY_REMINDER_TIME")


def show_menu():
    """
    Sends the main menu to the user via WhatsApp.

    This function formats and sends a menu message that displays
    the available calendar options the user can interact with:
        1 - View today's appointments
        2 - View tomorrow's appointments
        3 - View this week's appointments
        4 - View the next upcoming appointment

    The menu is sent using the Twilio API's send_message() function.
    """
    menu = ("\n\U0001F4F1 WhatsApp Kalendar Menü\n"
            "\u0031\uFE0F\u20E3 Heutige Termine\n"
            "\u0032\uFE0F\u20E3 Termine für morgen\n"
            "\u0033\uFE0F\u20E3 Termine für die Woche\n"
            "\u0034\uFE0F\u20E3 Nächster Termin\n")
    send_message(menu)


def main_loop():
    """
    Continuously runs the main application loop for the WhatsApp Calendar bot.
    This function performs the following tasks every second:
        - Checks whether the current time matches the configured daily reminder time
            (as set in the .env file). If so, and if the reminder hasn't already been sent
            today, it sends the list of today's calendar events.
        - Listens for new incoming WhatsApp messages via fetch_message().
            If a valid command (1–4) is received, the corresponding calendar
            information is retrieved and sent as a message.
        - Sends an error message and re-displays the menu for invalid inputs.

    The function ensures that daily reminders are only sent once per day
    and gracefully handles exceptions to prevent the loop from crashing.
    """
    valid_choices = {'1', '2', '3', '4'}
    last_message = None
    last_reminder_sent_date = None

    while True:
        try:
            now = datetime.now()
            current_time_str = now.strftime("%H:%M")
            today_str = now.strftime("%Y-%m-%d")

            if current_time_str == DAILY_REMINDER_TIME and last_reminder_sent_date != today_str:
                send_message(format_today(get_events_for_today()))
                last_reminder_sent_date = today_str

            message = fetch_message()
            if message and message != last_message:
                last_message = message
                if message in valid_choices:
                    if message == '1':
                        send_message(format_today(get_events_for_today()))
                    elif message == '2':
                        send_message(format_tomorrow(get_events_for_tomorrow()))
                    elif message == '3':
                        send_message(format_week(get_events_for_the_week()))
                    elif message == '4':
                        send_message(format_next_event(get_next_event()))
                else:
                    send_message("Ungültige Eingabe. Bitte 1-4 senden.")
                    show_menu()

            time.sleep(1)

        except Exception as e:
            print(Fore.RED + f"Fehler im main_loop: {e}" + Style.RESET_ALL)
            time.sleep(1)


if __name__ == "__main__":
    show_menu()
    try:
        main_loop()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgramm wurde vom Benutzer beendet." + Style.RESET_ALL)
