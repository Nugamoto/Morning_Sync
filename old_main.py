import time
from colorama import Fore, Style

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
from services.twilio_api import send_message, fetch_latest_whatsapp_message


def show_menu():
    menu = ("\n\U0001F4F1 WhatsApp Kalendar Menü\n"
            "\u0031\uFE0F\u20E3 Heutige Termine\n"
            "\u0032\uFE0F\u20E3 Termine für morgen\n"
            "\u0033\uFE0F\u20E3 Termine für die Woche\n"
            "\u0034\uFE0F\u20E3 Nächster Termin\n")
    send_message(menu)


def main_loop():
    valid_choices = {'1', '2', '3', '4'}
    last_message = None

    while True:
        try:
            message = fetch_latest_whatsapp_message()
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
