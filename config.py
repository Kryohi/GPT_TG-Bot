 
import os

# Configure OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Environment variable for the openai APIs not found")

# Configure Telegram bot API key
TELEGRAM_API_KEY_CHATBOT = os.getenv("TELEGRAM_API_KEY_CHATBOT")
if not TELEGRAM_API_KEY_CHATBOT:
    print("Environment variable for the telegram bot token not found")

# my userid
TG_USERID = int(os.getenv("TG_USERID"))
if not TG_USERID:
    print("Environment variable for the Telegram user ID not found")
else:
    print("user id: ", TG_USERID)
