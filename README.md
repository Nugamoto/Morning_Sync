<p align="center">
  <img src="assets/Morning_Sync_Logo.jpg" alt="MorningSync Logo" width="400"/>
</p>

# MorningSync ☕️

> WhatsApp appointments · Google Calendar

🇬🇧 English | 🇩🇪 [Deutsche Version](README.de.md)

---

## "What’s on my schedule today?"

**MorningSync** is a smart WhatsApp bot that sends you your daily schedule from Google Calendar every morning –
including the weather and helpful tips.  
You can chat with it like a friend: "What’s up today?", "What do I have on Friday?", or simply "Hey". MorningSync will
reply.

---

## 🚀 Features

- ✉️ WhatsApp integration via Twilio Conversations API
- 🗓️ Daily overview pulled directly from your Google Calendar
- ☔️ Weather data from OpenWeatherMap with clothing suggestions
- 💬 Two-way menu-based interaction: choose via 1–4
- 📆 Daily reminder at your preferred time (see `.env`)
- ⚙️ Modular structure & easy to extend

---

## 🤝 Example Replies

**No events:**

```
📅 No events for today.
```

**No events tomorrow:**

```
📅 No events for tomorrow.
```

**No events this week:**

```
📅 No events scheduled this week.
```

**Multiple events today:**

```
📅 Your schedule for Monday, April 1st:

🕐 09:00: Team stand-up (Zoom)  
🕓 15:30: Doctor’s appointment with Dr. Müller  
🕖 18:00: Workout with Lisa  

📝 A total of 3 events today.  
📆 Good luck!
```

**With weather integration:**

```
🌤 Weather in Berlin:
- 13–17°C, partly cloudy  
- No rain  
- Light wind  

🫕 Suggestion:  
No jacket needed today – but maybe bring a sweater for the afternoon. 👕
```

---

## 🛠️ Installation

### Requirements

- Python 3.10+
- A Google Cloud project with Calendar API enabled
- Twilio account with access to the Conversations API
- OpenWeatherMap API key

### Setup

1. **Clone the repository:**

```bash
git clone https://github.com/your-team/morningsync.git
cd morningsync
```

2. **Create virtual environment & install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Add `credentials.json`:**  
   Download your `credentials.json` from Google Cloud (OAuth2 with access to Google Calendar) and place it in the root
   project directory.

4. **Create your `.env` file:**

```env
DAILY_REMINDER_TIME=08:00
CITY=Berlin
INCLUDE_WEATHER_MESSAGE=True
INCLUDE_FUNNY_WEATHER=True
INCLUDE_OUTFIT_TIP=True

OPENWEATHER_API_KEY=

ACCOUNT_SID=
API_KEY_SID=
API_KEY_SECRET=
CHAT_SERVICE_SID=
MY_PHONE_NUMBER=
TWILIO_WHATSAPP_NUMBER=
```

5. **Run the app:**

```bash
python main.py
```

---

## 🔄 Project Structure

```
├── main.py
├── utils/
│   └── formatter.py
├── services/
│   ├── google_calendar.py
│   ├── new_twilio_api.py
│   └── weather.py
├── credentials.json
```

---

## 📊 Flow

1. User sends a WhatsApp message
2. Bot responds with a menu of options:

```
1 - Today’s events  
2 - Tomorrow’s events  
3 - Events this week  
4 - Next event
```

3. User replies with a number (1–4)
4. System generates the appropriate response
5. Twilio sends the reply back via WhatsApp

---

## 🌟 Ideas for Extension

- 🕐 Reminders 30 minutes before each event
- 🌐 Auto-include Zoom/video links
- 📊 Weekly summary ("You had 12 meetings...")
- 📅 Add new events via WhatsApp

---

## 👨‍💼 Team MorningSync

- Viktoria
- Tom
- Lukas
- Christian

---

## ✨ License

MIT License

> Hackathon project for Master School, 2025. Powered by Python 🐍
