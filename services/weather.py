import os

import requests
from dotenv import load_dotenv


def get_weather_forecast():
    """
    Fetches the current weather data and generates a summary string.

    Optionally includes a funny comment and a clothing tip based on environment variables.
    Weather output can be disabled entirely using the INCLUDE_WEATHER_MESSAGE variable.

    Returns:
        str: Weather information as a formatted string, or an empty string if disabled.
    """
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = os.getenv("CITY", "Berlin")
    include_weather = os.getenv("INCLUDE_WEATHER_MESSAGE", "").lower() == "true"
    if not include_weather:
        return ""
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={api_key}&units=metric&lang=de"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            description = data["weather"][0]["description"].lower()
            temp = round(data["main"]["temp"])
            include_funny = os.getenv("INCLUDE_FUNNY_WEATHER", "").lower() == "true"
            include_outfit = os.getenv("INCLUDE_OUTFIT_TIP", "").lower() == "true"
            result = f"{description.capitalize()}, {temp}°C"
            extra_lines = ""
            if include_funny:
                funny_comment = get_funny_weather_comment(description, temp)
                extra_lines += f"{funny_comment}"
            if include_outfit:
                outfit_tip = get_weather_outfit_tip(description, temp)
                extra_lines += f"Hinweis: {outfit_tip}"
            if extra_lines:
                result += f"\n{extra_lines.strip()}"
            return result
        else:
            return "Wetterdaten konnten nicht geladen werden."
    except Exception as e:
        return f"Fehler beim Abrufen der Wetterdaten: {e}"


def get_funny_weather_comment(description, temp):
    """
    Generates a humorous weather-related comment based on description and temperature.

    Args:
        description (str): The weather description (e.g., "sonnig", "regen").
        temp (int): The temperature in degrees Celsius.

    Returns:
        str: A funny comment string in German with an emoji.
    """
    if "regen" in description:
        return "\u2614 Kostenlos duschen heute – ganz ohne Handtuch!\n"
    elif "wolke" in description:
        return "\u2601 Bestes Wetter, um alles auf die Wolken zu schieben.\n"
    elif "sonnig" in description or "klar" in description:
        return "\U0001F60E Sonnenbrillenmodus: aktiviert.\n"
    elif temp > 28:
        return "\U0001F525 Zeit, eins mit dem Grill zu werden.\n"
    elif temp < 5:
        return "\u2744 Extra Kaffee mitnehmen. Und vielleicht eine zweite Jacke.\n"
    else:
        return "\U0001F308 Wetter passt zu allem – außer zu Entscheidungen.\n"


def get_weather_outfit_tip(description, temp):
    """
    Suggests clothing tips based on the current weather description and temperature.

    Args:
        description (str): The weather description (e.g., "klar", "regen").
        temp (int): The temperature in degrees Celsius.

    Returns:
        str: A practical clothing suggestion in German.
    """
    if "regen" in description:
        return "Vergiss den Regenschirm nicht und zieh eine wasserfeste Jacke an.\n"
    elif "wolke" in description:
        return "Ein Pullover oder eine leichte Jacke könnte sinnvoll sein.\n"
    elif "sonnig" in description or "klar" in description:
        return "Denk an Sonnencreme und eine Sonnenbrille!\n"
    elif temp > 28:
        return "Leichte Kleidung und viel Wasser sind heute angesagt.\n"
    elif temp < 5:
        return "Zieh dich warm an – Mütze, Schal und Handschuhe nicht vergessen.\n"
    else:
        return "Am besten im Zwiebellook anziehen – so bist du flexibel.\n"
