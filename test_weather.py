from dotenv import load_dotenv
import os
import requests
from pathlib import Path

# -------------------------
# Absolute path to your bot folder
# -------------------------
bot_folder = r"C:\Users\hp\bot with py"  # <- change this to your folder
dotenv_path = Path(bot_folder) / ".env"
load_dotenv(dotenv_path)

# -------------------------
# Read keys
# -------------------------
WEATHER_API_KEY = os.getenv("4493e812849d7f5bab780e9a95bb9de5")
TELEGRAM_TOKEN = os.getenv("7938645145:AAG4Vb6bGp2w_fl0b7iG19xigjGkSW-QVwo")

# -------------------------
# Check keys
# -------------------------
if not WEATHER_API_KEY:
    print("❌ OpenWeather API key not found! Check your .env file.")
    exit(1)
else:
    print("✅ OpenWeather API key loaded.")

if not TELEGRAM_TOKEN:
    print("❌ Telegram Bot token not found! Check your .env file.")
else:
    print("✅ Telegram Bot token loaded.")

# -------------------------
# Fetch weather for Addis Ababa
# -------------------------
city = "Addis Ababa"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

try:
    res = requests.get(url).json()
    if res.get("cod") == 200:
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"].capitalize()
        humidity = res["main"]["humidity"]
        print(f"🌦️ {city} Weather: {temp}°C, {desc}, Humidity: {humidity}%")
    else:
        print("⚠️ Could not fetch weather:", res.get("message"))
except Exception as e:
    print("❌ Error fetching weather:", e)
