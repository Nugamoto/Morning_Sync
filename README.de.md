<p align="center">
  <img src="assets/Morning_Sync_Logo.jpg" alt="MorningSync Logo" width="400"/>
</p>


🇬🇧 [English Version](README.md) | 🇩🇪 Deutsch

# MorningSync ☕️

WhatsApp-gestützter Tagesplan-Assistent

> **"Wie sieht mein Tag heute aus?"**

**MorningSync** ist ein smarter WhatsApp-Bot, der dir jeden Morgen automatisch deinen Tagesplan aus dem Google Kalender
schickt – inklusive Wetter und passenden Empfehlungen.
Du kannst ihm schreiben wie einem Freund: "Was steht heute an?", "Was habe ich am Freitag?", oder einfach nur "Hey".
MorningSync antwortet.

---

## 🚀 Features

- ✉️ WhatsApp-Integration via Twilio Conversations API
- 🗓️ Tagesübersicht direkt aus deinem Google Kalender
- ☔️ Wetterdaten aus OpenWeatherMap mit Kleidungstipps
- 💬 Zwei-Wege-Kommunikation via Menü: Auswahl per 1–4
- 📆 Täglicher Reminder zur gewählten Uhrzeit (siehe `.env`)
- ⚙️ Modular aufgebaut & leicht erweiterbar

---

## 🤝 Beispiel-Antworten

**Keine Termine:**

```
📅 Keine Termine für heute.
```

**Keine Termine morgen:**

```
📅 Keine Termine für morgen.
```

**Keine Termine diese Woche:**

```
📅 Keine Termine diese Woche.
```

**Mehrere Termine heute:**

```
📅 Dein Tagesplan für Montag, 1. April:

🕐 09:00 Uhr: Team-Standup (Zoom)
🕓 15:30 Uhr: Arzttermin bei Dr. Müller
🕖 18:00 Uhr: Fitness mit Lisa

📝 Insgesamt 3 Termine heute.
📆 Viel Erfolg!
```

**Mit Wetterintegration:**

```
🌤 Wetter in Berlin:
- 13–17°C, teilweise bewölkt
- Kein Regen
- Leichter Wind

🫕 Empfehlung:
Du brauchst heute keine Jacke – aber vielleicht einen Pulli für den Nachmittag. 👕
```

---

## 🛠️ Installation

### Voraussetzungen

- Python 3.10+
- Ein Google Cloud-Projekt mit aktivierter Calendar API
- Twilio-Account mit Zugriff auf die Conversations API
- OpenWeatherMap API Key

### Setup

1. **Repository klonen:**

```bash
git clone https://github.com/dein-team/morningsync.git
cd morningsync
```

2. **Virtuelle Umgebung & Abhängigkeiten installieren:**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **credentials.json platzieren:**
   Lade deine `credentials.json` von Google Cloud herunter (OAuth2 mit Zugriff auf den Google Kalender) und lege sie im
   Hauptverzeichnis des Projekts ab.

4. **.env-Datei erstellen:**

```env
DAILY_REMINDER_TIME=08:00         # Zeitpunkt für den täglichen Reminder (z. B. 08:00 Uhr)
CITY=Berlin                        # Stadt für Wetterinformationen
INCLUDE_WEATHER_MESSAGE=True      # Wetteranzeige aktivieren
INCLUDE_FUNNY_WEATHER=True        # Humorvolle Wetterkommentare aktivieren
INCLUDE_OUTFIT_TIP=True           # Outfit-Tipps basierend auf Wetter aktivieren

OPENWEATHER_API_KEY=

ACCOUNT_SID=
API_KEY_SID=
API_KEY_SECRET=
CHAT_SERVICE_SID=
MY_PHONE_NUMBER=
TWILIO_WHATSAPP_NUMBER=
```

5. **Starten:**

```bash
python main.py
```

---

## 🔄 Projektstruktur

```
├── main.py                     # Hauptprogramm: verarbeitet eingehende Nachrichten
├── utils/
│   └── formatter.py         # Nachrichtentemplates für WhatsApp
├── services/
│   ├── google_calendar.py   # Kalenderabfrage & Events sortieren
│   ├── new_twilio_api.py    # Kommunikation mit Twilio Conversations API
│   └── weather.py           # Wetterdaten via OpenWeatherMap
├── credentials.json           # Google OAuth2 Client Credentials
```

---

## 📊 Ablauf

1. Der Nutzer schreibt an WhatsApp.
2. Der Bot sendet ein Auswahlmenü mit Optionen:

```
1 - Heutige Termine
2 - Termine für morgen
3 - Termine diese Woche
4 - Nächster Termin
```

3. Der Nutzer antwortet mit einer Zahl (1–4).
4. Das System generiert die entsprechende Antwort:
    - Kalendertermine abrufen
    - Optional: Wetterdaten einbinden (je nach .env-Einstellung)
5. Die Antwort wird über Twilio zurück an WhatsApp gesendet.

---

## 🌟 Erweiterungsideen

- 🕐 Erinnerung 30 Minuten vor Terminen
- 🌐 Zoom-/Videolinks automatisch mitschicken, falls in Terminen enthalten
- 📊 Analyse der Woche ("Du hattest 12 Meetings ...")
- 📅 Termine direkt per WhatsApp anlegen

---

## 👨‍💼 Team MorningSync

- Viktoria
- Tom
- Lukas
- Christian

---

## ✨ Lizenz

MIT License

---

> Hackathon-Projekt für Master School, 2025. Powered by Python 🐍
