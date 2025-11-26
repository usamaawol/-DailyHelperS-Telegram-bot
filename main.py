import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
from datetime import datetime
import asyncio
from flask import Flask

# ------------------ Load environment ------------------
bot_folder = Path(__file__).parent
load_dotenv(bot_folder / ".env")

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not WEATHER_API_KEY or not TELEGRAM_TOKEN:
    print("❌ Missing API keys in .env")
    exit(1)

# ------------------ Telegram Bot Data ------------------
CITY_COORDS = {
    "Addis Ababa": {"lat": 9.03, "lon": 38.74},
    "Haramaya": {"lat": 9.36, "lon": 42.03},
    "Bale Robe": {"lat": 6.98, "lon": 39.84}
}

QUOTES = [
    "The best among you are those who learn the Qur'an and teach it.",
    "Pray as if it's your last day on earth.",
    "Good deeds erase bad deeds.",
    "Patience is light.",
    "Charity does not decrease wealth."
]

# ------------------ Helper functions ------------------
def convert_to_ampm(time_str: str) -> str:
    t = datetime.strptime(time_str, "%H:%M")
    return t.strftime("%I:%M %p")

def get_weather(city: str) -> str:
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

def get_prayer_times(city: str) -> str:
    lat = CITY_COORDS[city]["lat"]
    lon = CITY_COORDS[city]["lon"]
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=2"
    try:
        res = requests.get(url).json()
        if res.get("code") == 200:
            timings = res["data"]["timings"]
            return (
                f"🕌 Prayer times for {city} today:\n"
                f"Fajr: {convert_to_ampm(timings['Fajr'])}\n"
                f"Dhuhr: {convert_to_ampm(timings['Dhuhr'])}\n"
                f"Asr: {convert_to_ampm(timings['Asr'])}\n"
                f"Maghrib: {convert_to_ampm(timings['Maghrib'])}\n"
                f"Isha: {convert_to_ampm(timings['Isha'])}"
            )
        else:
            return "⚠️ Could not fetch prayer times."
    except Exception as e:
        return f"❌ Error fetching prayer times: {e}"

def get_quote() -> str:
    return "📿 " + random.choice(QUOTES)

# ------------------ Telegram Handlers ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌙 Welcome to DailyHelperS Bot!\n"
        "Available commands:\n"
        "/weather_addis\n"
        "/prayer_addis\n"
        "/prayer_haramaya\n"
        "/prayer_balerobe\n"
        "/quote\n"
        "/reminder (demo)"
    )

async def weather_addis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_weather("Addis Ababa"))

async def prayer_addis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_prayer_times("Addis Ababa"))

async def prayer_haramaya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_prayer_times("Haramaya"))

async def prayer_balerobe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_prayer_times("Bale Robe"))

async def quote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_quote())

async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏰ Reminder feature coming soon! (Demo)")

# ------------------ Flask web server for UptimeRobot ------------------
flask_app = Flask("web")

@flask_app.route("/")
def home():
    return "Bot is alive ✅", 200

async def run_flask():
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:8080"]  # Replit default port
    await serve(flask_app, config)

# ------------------ MAIN ------------------
async def main():
    # Start Telegram Bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather_addis", weather_addis))
    app.add_handler(CommandHandler("prayer_addis", prayer_addis))
    app.add_handler(CommandHandler("prayer_haramaya", prayer_haramaya))
    app.add_handler(CommandHandler("prayer_balerobe", prayer_balerobe))
    app.add_handler(CommandHandler("quote", quote_cmd))
    app.add_handler(CommandHandler("reminder", reminder))

    print("✅ Bot started!")

    # Run both Telegram and Flask concurrently
    await asyncio.gather(
        app.run_polling(),
        run_flask()
    )

if __name__ == "__main__":
    asyncio.run(main())




































































