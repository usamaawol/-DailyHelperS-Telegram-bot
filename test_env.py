from dotenv import load_dotenv
import os

# Load .env from current working directory
load_dotenv(".env")

print(os.getenv("OPENWEATHER_API_KEY"))   # Should print your key
print(os.getenv("TELEGRAM_BOT_TOKEN"))    # Should print your bot token
