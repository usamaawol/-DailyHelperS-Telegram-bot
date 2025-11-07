import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
from datetime import datetime

# -------------------------
# Load .env keys
# -------------------------
bot_folder = Path(__file__).parent
load_dotenv(bot_folder / ".env")

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not WEATHER_API_KEY or not TELEGRAM_TOKEN:
    print("❌ Missing API keys in .env")
    exit(1)

# -------------------------
# City coordinates for prayer times
# -------------------------
CITY_COORDS = {
    "Addis Ababa": {"lat": 9.03, "lon": 38.74},
    "Haramaya": {"lat": 9.36, "lon": 42.03},
    "Bale Robe": {"lat": 6.98, "lon": 39.84}
}

# -------------------------
# Helper function to convert 24h to AM/PM
# -------------------------
def convert_to_ampm(time_str):
    t = datetime.strptime(time_str, "%H:%M")
    return t.strftime("%I:%M %p")

# -------------------------
# Weather function
# -------------------------
def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        res = requests.get(url).json()
        if res.get("cod") == 200:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"].capitalize()
            humidity = res["main"]["humidity"]
            return f"🌦️ {city} Weather: {temp}°C, {desc}, Humidity: {humidity}%"
        else:
            return f"⚠️ Could not fetch weather: {res.get('message')}"
    except Exception as e:
        return f"❌ Error fetching weather: {e}"

# -------------------------
# Prayer times function
# -------------------------
def get_prayer_times(city: str):
    lat = CITY_COORDS[city]["lat"]
    lon = CITY_COORDS[city]["lon"]
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=2"

    try:
        res = requests.get(url).json()
        if res.get("code") == 200:
            timings = res["data"]["timings"]
            response = f"🕌 Prayer times for {city} today:\n"
            response += f"Fajr: {convert_to_ampm(timings['Fajr'])}\n"
            response += f"Dhuhr: {convert_to_ampm(timings['Dhuhr'])}\n"
            response += f"Asr: {convert_to_ampm(timings['Asr'])}\n"
            response += f"Maghrib: {convert_to_ampm(timings['Maghrib'])}\n"
            response += f"Isha: {convert_to_ampm(timings['Isha'])}"
            return response
        else:
            return "⚠️ Could not fetch prayer times."
    except Exception as e:
        return f"❌ Error fetching prayer times: {e}"

# -------------------------
# Islamic quotes
# -------------------------
QUOTES = [
    "The best among you are those who learn the Qur'an and teach it.",
    "Pray as if it's your last day on earth.",
    "Good deeds erase bad deeds.",
    "Patience is light.",
    "Charity does not decrease wealth."
]

def get_quote():
    return "📿 " + random.choice(QUOTES)

# -------------------------
# Command handlers
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌙 Welcome to DailyHelperS Bot!\n\n"
        "Available commands:\n"
        "/weather_addis - Weather for Addis Ababa\n"
        "/weather_haramaya - Weather for Haramaya\n"
        "/weather_balerobe - Weather for Bale Robe\n"
        "/prayer_addis - Prayer times for Addis Ababa\n"
        "/prayer_haramaya - Prayer times for Haramaya\n"
        "/prayer_balerobe - Prayer times for Bale Robe\n"
        "/quote - Daily Islamic quote\n"
        "/reminder - Set a study/prayer reminder (demo)"
    )

# Weather commands
async def weather_addis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_weather("Addis Ababa"))

async def weather_haramaya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_weather("Haramaya"))

async def weather_balerobe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_weather("Bale Robe"))

# Prayer commands
async def prayer_addis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_prayer_times("Addis Ababa"))

async def prayer_haramaya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_prayer_times("Haramaya"))

async def prayer_balerobe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_prayer_times("Bale Robe"))

# Quote & reminder
async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_quote())

async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏰ Reminder feature coming soon! (Demo)")

# -------------------------
# Run bot
# -------------------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Start
    app.add_handler(CommandHandler("start", start))

    # Weather
    app.add_handler(CommandHandler("weather_addis", weather_addis))
    app.add_handler(CommandHandler("weather_haramaya", weather_haramaya))
    app.add_handler(CommandHandler("weather_balerobe", weather_balerobe))

    # Prayer
    app.add_handler(CommandHandler("prayer_addis", prayer_addis))
    app.add_handler(CommandHandler("prayer_haramaya", prayer_haramaya))
    app.add_handler(CommandHandler("prayer_balerobe", prayer_balerobe))

    # Quote & reminder
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("reminder", reminder))

    print("✅ Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()










































































