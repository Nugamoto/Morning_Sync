import os.path
import pickle
from datetime import datetime, timedelta

import pytz
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
timezone = pytz.timezone("Europe/Berlin")


def authenticate_google():
    """
    Authenticates the user with the Google Calendar API using OAuth2.

    This function checks if valid credentials are stored in 'token.pkl'. If found,
    these credentials are used to build a service object for the Google Calendar API.
    Otherwise, it prompts the user to authenticate via a web browser and stores the new credentials.

    Returns:
        googleapiclient.discovery.Resource: A service object for interacting with the Google Calendar API.
    """
    creds = None

    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def list_calendars():
    """
    Retrieves a list of calendar IDs available to the authenticated user.

    Returns:
        list: A list of calendar ID strings.
    """
    service = authenticate_google()
    calendar_list = service.calendarList().list().execute()
    return [calendar["id"] for calendar in calendar_list["items"]]


def get_events_for_today():
    """
    Retrieves events scheduled for today from all available calendars.

    The function gathers events occurring between the current time and the end of the day
    for each calendar and formats them as a list of strings.

    Returns:
        list: A list of strings representing today's events.
    """
    service = authenticate_google()

    now = datetime.now(timezone)
    end_of_day = now.replace(hour=23, minute=59, second=59)

    today = ["Termine für heute"]

    calendar_ids = list_calendars()
    for cal_id in calendar_ids:
        events_result = service.events().list(
            calendarId=cal_id,
            timeMin=now.isoformat(),
            timeMax=end_of_day.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get("items", [])

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'Kein Titel')
            today.append(f"– {start} Uhr: {summary}")

    if not today:
        return ["Keine Termine"]

    return today


def get_events_for_tomorrow():
    """
    Retrieves events scheduled for tomorrow from all available calendars.

    The function gathers events occurring between the start and end of tomorrow for each
    calendar and formats them as a list of strings.

    Returns:
        list: A list of strings representing tomorrow's events.
    """
    service = authenticate_google()

    now = datetime.now(timezone)
    tomorrow = now + timedelta(days=1)
    start_of_tomorrow = timezone.localize(datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0))
    end_of_tomorrow = timezone.localize(datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59))

    tomorrow = ["Termine für morgen"]

    calendar_ids = list_calendars()
    for cal_id in calendar_ids:
        events_result = service.events().list(
            calendarId=cal_id,
            timeMin=start_of_tomorrow.isoformat(),
            timeMax=end_of_tomorrow.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get("items", [])

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'Kein Titel')
            tomorrow.append(f"– {start} Uhr: {summary}")

    return tomorrow


def get_events_for_the_week():
    """
    Retrieves events for the week starting seven days from today from all available calendars.

    The function gathers events occurring within the week and formats them as a list of strings.

    Returns:
        list: A list of strings representing the events for the week.
    """
    service = authenticate_google()

    now = datetime.now(timezone)
    today = timezone.localize(datetime(now.year, now.month, now.day, 0, 0, 0))
    start_of_week = today + timedelta(days=7)
    end_of_week = timezone.localize(datetime(start_of_week.year, start_of_week.month, start_of_week.day, 23, 59, 59))

    week = ["Termine der Woche"]

    calendar_ids = list_calendars()
    for cal_id in calendar_ids:
        events_result = service.events().list(
            calendarId=cal_id,
            timeMin=start_of_week.isoformat(),
            timeMax=end_of_week.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get("items", [])

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'Kein Titel')
            week.append(f"– {start} Uhr: {summary}")

    return week


def get_next_event():
    """
    Retrieves the next upcoming event from all available calendars.

    The function collects the next event from each calendar, determines the soonest event,
    and returns it formatted as a list of strings.

    Returns:
        list: A list containing a header and the next event's details. If no events are found,
              a list with a message indicating that no events were found is returned.
    """
    service = authenticate_google()

    now = datetime.now(timezone)

    all_events = []

    calendar_ids = list_calendars()
    for cal_id in calendar_ids:
        events_result = service.events().list(
            calendarId=cal_id,
            timeMin=now.isoformat(),
            maxResults=1,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get("items", [])
        if events:
            event = events[0]
            start_str = event['start'].get('dateTime', event['start'].get('date'))
            start_dt = datetime.fromisoformat(start_str).astimezone(timezone)
            all_events.append((start_dt, event))

    if not all_events:
        return ["Keine Termine gefunden"]

    all_events.sort(key=lambda x: x[0])

    next_event = all_events[0][1]
    start = next_event['start'].get('dateTime', event['start'].get('date'))
    summary = next_event.get("summary", "kein titel")

    return ["Nächster Termin", f"– {start} Uhr: {summary}"]
