import datetime
from collections import defaultdict


def format_today(event_list):
    """
    Generate a formatted message for today's events.

    :param event_list: List of event entries.
    :return: A formatted message string for today's events.
    """
    events = []
    for entry in event_list:
        if not entry.startswith("–"):
            continue
        entry = entry.lstrip("– ").strip()
        timestamp, description = entry.split(" Uhr: ", 1)
        if timestamp.endswith("Z"):
            timestamp = timestamp[:-1] + "+00:00"
        dt = datetime.datetime.fromisoformat(timestamp)
        time_str = dt.strftime("%H:%M")
        events.append((dt, time_str, description))

    events.sort(key=lambda x: x[0])

    if not events:
        return "\U0001F4C5 Keine Termine für heute."

    dt0 = events[0][0]
    weekday = dt0.strftime("%A")
    day = dt0.day
    month = dt0.strftime("%B")

    weekday_map = {
        "Monday": "Montag", "Tuesday": "Dienstag", "Wednesday": "Mittwoch",
        "Thursday": "Donnerstag", "Friday": "Freitag", "Saturday": "Samstag", "Sunday": "Sonntag"
    }
    month_map = {
        "January": "Januar", "February": "Februar", "March": "März", "April": "April",
        "May": "Mai", "June": "Juni", "July": "Juli", "August": "August",
        "September": "September", "October": "Oktober", "November": "November", "December": "Dezember"
    }

    weekday_de = weekday_map[weekday]
    month_de = month_map[month]

    header = f"\U0001F4C5 Dein Tagesplan für {weekday_de}, {day}. {month_de}:\n\n"
    body = ""
    for _, time_str, description in events:
        body += f"\U0001F552 {time_str} – {description}\n"
    footer = f"\n\U0001F4DD Insgesamt {len(events)} Termine heute.\n\u2705 Viel Erfolg!"
    final_message = header + body + footer

    return final_message


def format_tomorrow(event_list):
    """
    Generate a formatted message for tomorrow's events.

    :param event_list: List of event entries.
    :return: A formatted message string for tomorrow's events.
    """
    events = []
    for entry in event_list:
        if not entry.startswith("–"):
            continue
        entry = entry.lstrip("– ").strip()
        timestamp, description = entry.split(" Uhr: ", 1)
        if timestamp.endswith("Z"):
            timestamp = timestamp[:-1] + "+00:00"
        dt = datetime.datetime.fromisoformat(timestamp)
        time_str = dt.strftime("%H:%M")
        events.append((dt, time_str, description))

    events.sort(key=lambda x: x[0])

    if not events:
        return "\U0001F4C5 Keine Termine für morgen."

    dt0 = events[0][0]
    weekday = dt0.strftime("%A")
    day = dt0.day
    month = dt0.strftime("%B")

    weekday_map = {
        "Monday": "Montag", "Tuesday": "Dienstag", "Wednesday": "Mittwoch",
        "Thursday": "Donnerstag", "Friday": "Freitag", "Saturday": "Samstag", "Sunday": "Sonntag"
    }
    month_map = {
        "January": "Januar", "February": "Februar", "March": "März", "April": "April",
        "May": "Mai", "June": "Juni", "July": "Juli", "August": "August",
        "September": "September", "October": "Oktober", "November": "November", "December": "Dezember"
    }

    weekday_de = weekday_map[weekday]
    month_de = month_map[month]

    header = f"\U0001F4C5 Dein Tagesplan für {weekday_de}, {day}. {month_de}:\n\n"
    body = ""
    for _, time_str, description in events:
        body += f"\U0001F552 {time_str} – {description}\n"
    footer = f"\n\U0001F4DD Insgesamt {len(events)} Termine morgen.\n\u2705 Viel Erfolg!"
    final_message = header + body + footer

    return final_message


def format_week(event_list):
    """
    Generate a formatted message for all events in the current week.

    :param event_list: List of event entries.
    :return: A formatted message string representing the week's events.
    """
    events = []
    for entry in event_list:
        if not entry.startswith("–"):
            continue
        entry = entry.lstrip("– ").strip()
        timestamp, description = entry.split(" Uhr: ", 1)
        if timestamp.endswith("Z"):
            timestamp = timestamp[:-1] + "+00:00"
        dt = datetime.datetime.fromisoformat(timestamp)
        time_str = dt.strftime("%H:%M")
        events.append((dt, time_str, description))

    events.sort(key=lambda x: x[0])

    if not events:
        return "\U0001F4C5 Keine Termine diese Woche."

    weekday_map = {
        "Monday": "Montag", "Tuesday": "Dienstag", "Wednesday": "Mittwoch",
        "Thursday": "Donnerstag", "Friday": "Freitag", "Saturday": "Samstag", "Sunday": "Sonntag"
    }
    month_map = {
        "January": "Januar", "February": "Februar", "March": "März", "April": "April",
        "May": "Mai", "June": "Juni", "July": "Juli", "August": "August",
        "September": "September", "October": "Oktober", "November": "November", "December": "Dezember"
    }

    grouped_events = defaultdict(list)
    for dt, time_str, description in events:
        date_key = dt.date()
        grouped_events[date_key].append((dt, time_str, description))

    header = "\U0001F4C5 Dein Wochenplan:\n"
    body = ""

    for date_key in sorted(grouped_events):
        dt_sample = grouped_events[date_key][0][0]
        weekday = weekday_map[dt_sample.strftime("%A")]
        day = dt_sample.day
        month = month_map[dt_sample.strftime("%B")]
        body += f"\n\U0001F4CC {weekday}, {day}. {month}:\n"
        for _, time_str, description in grouped_events[date_key]:
            body += f"\U0001F552 {time_str} – {description}\n"

    footer = f"\n\U0001F4DD Insgesamt {len(events)} Termine diese Woche.\n\u2705 Viel Erfolg!"
    final_message = header + body + footer

    return final_message


def format_next_event(event_list):
    """
    Generate a formatted message for the next event.

    :param event_list: List of event entries.
    :return: A formatted message string for the next event.
    """
    events = []
    for entry in event_list:
        if not entry.startswith("–"):
            continue
        entry = entry.lstrip("– ").strip()
        timestamp, description = entry.split(" Uhr: ", 1)
        if timestamp.endswith("Z"):
            timestamp = timestamp[:-1] + "+00:00"
        dt = datetime.datetime.fromisoformat(timestamp)
        time_str = dt.strftime("%H:%M")
        events.append((dt, time_str, description))

    if not events:
        return "\U0001F4C5 Keine Termine für heute."

    dt0 = events[0][0]
    weekday = dt0.strftime("%A")
    day = dt0.day
    month = dt0.strftime("%B")

    weekday_map = {
        "Monday": "Montag", "Tuesday": "Dienstag", "Wednesday": "Mittwoch",
        "Thursday": "Donnerstag", "Friday": "Freitag", "Saturday": "Samstag", "Sunday": "Sonntag"
    }
    month_map = {
        "January": "Januar", "February": "Februar", "March": "März", "April": "April",
        "May": "Mai", "June": "Juni", "July": "Juli", "August": "August",
        "September": "September", "October": "Oktober", "November": "November", "December": "Dezember"
    }

    weekday_de = weekday_map[weekday]
    month_de = month_map[month]

    header = f"\U0001F4C5 Dein nächster Termin ist am {weekday_de}, {day}. {month_de}:\n\n"
    body = ""
    for _, time_str, description in events:
        body += f"\U0001F552 {time_str} – {description}\n"
    footer = f"\n\u2705 Viel Erfolg!"
    final_message = header + body + footer

    return final_message
