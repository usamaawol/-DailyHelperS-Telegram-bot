🌙 RoutineAssistantXBot

Your smart daily-routine assistant on Telegram — providing weather updates, Islamic prayer times, motivational quotes, and study reminders in one simple bot.

✨ Features
☀️ Weather Updates

Get accurate weather information for selected Ethiopian cities.

🕌 Prayer Times

Receive daily Islamic prayer times with a beautiful, clean format.

💬 Motivational Quotes

Daily inspirational quotes to boost your mindset.

⏰ Study/Task Reminder (Demo)

A simple reminder to help you stay productive.

📌 Available Bot Commands
/start – Show bot menu
/weather_addis – Weather for Addis Ababa
/prayer_addis – Prayer times for Addis Ababa
/prayer_haramaya – Prayer times for Haramaya
/prayer_balerobe – Prayer times for Bale Robe
/quote – Get a motivational quote
/reminder – Demo reminder system

🔧 Tech Stack

Python 3.10+

python-telegram-bot v21+

OpenWeatherMap API

Aladhan Prayer API

dotenv for managing environment variables

📁 Project Structure
.
├── main.py            # Main bot code
├── .gitignore         # Hidden files list (.env is excluded)
├── requirements.txt   # Python dependencies
└── .env (not uploaded)  # Contains secret API keys

🔐 Environment Variables

Create a .env file in your project root:

TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
OPENWEATHER_API_KEY=YOUR_API_KEY_HERE


⚠️ Never upload .env to GitHub!

▶️ How to Run the Bot

Install dependencies:

pip install -r requirements.txt


Run the bot:

python main.py


Enjoy using your RoutineAssistantXBot 🎉

🛡️ Security Notes

✔️ .env file is ignored by GitHub
✔️ API keys remain private
✔️ Safe commit history after cleanup

⭐ Support the Project

If you like this bot, feel free to star ⭐ the repository or suggest new features!
