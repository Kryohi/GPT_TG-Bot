import logging
import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import text
import asyncio

# for DALLE
import requests
from io import BytesIO

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("Environment variable for the openai APIs not found")

# Configure Telegram bot API key
API_TOKEN = os.getenv("TELEGRAM_API_KEY_CHATBOT")
if not API_TOKEN:
    print("Environment variable for the telegram bot token not found")

my_user_id = int(os.getenv("TG_USERID"))
if not API_TOKEN:
    print("Environment variable for the Telegram user ID not found")
else:
    print("user id: ", my_user_id)


logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Set bot_id
bot_id = None
async def on_startup(dp):
    global bot_id
    bot_data = await bot.get_me()
    bot_id = bot_data.id


# Holds the previous messages in memory
conversations = {}


# Function to call the ChatGPT API
async def chat_with_gpt(conversation_history):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history,
        )
    )

    response_text = response.choices[0].message.content
    return response_text


def add_initial_system_message(conversation_history):
    initial_message = {"role": "system", "content": "You are a helpful assistant."}
    if not conversation_history or conversation_history[0]["role"] != "system":
        conversation_history.insert(0, initial_message)
    return conversation_history



# Audio message support
async def transcribe_audio(file_id):
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}"

    # Download the voice file
    response = requests.get(file_url)

    # Save the voice file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(response.content)
        temp_audio_filename = temp_audio.name

    # Call the Whisper ASR API
    with open(temp_audio_filename, "rb") as audio_file:
        response = openai.Speech.create(
            engine="whisper",
            file=audio_file,
            language="en-US",
            sample_rate=16000,
        )

    # Delete the temporary voice file
    os.unlink(temp_audio_filename)

    # Get the transcribed text
    transcribed_text = response["choices"][0]["text"]
    return transcribed_text



# The message handler
async def on_message(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    my_user_id = int(os.getenv("TG_USERID"))

    print(f"Message received from {user_id}")

    if user_id == my_user_id:
        print("User is you")
    else:
        try:
            member = await bot.get_chat_member(chat_id, my_user_id)
            if member.status not in ("left", "kicked"):
                print("User shares a group with you")
            else:
                print("User is neither you nor shares a group with you")
                return
        except Exception as e:
            print(f"Error while checking chat member: {e}")
            return

    mentioned_bot = (await bot.get_me()).username in message.text
    is_direct_reply = (
        message.reply_to_message and message.reply_to_message.from_user.id == bot_id
    )


    if is_direct_reply or mentioned_bot:
        input_text = message.text

        # Save the user's message
        if chat_id not in conversations:
            conversations[chat_id] = []
        conversations[chat_id].append({"role": "user", "content": input_text})

        # Call the ChatGPT API with conversation history, including an initial system message
        conversation_history = add_initial_system_message(conversations[chat_id])
        response_text = await chat_with_gpt(conversation_history)

        # Save the bot's response
        conversations[chat_id].append({"role": "assistant", "content": response_text})

        # Print received messages
        print(f"User {user_id} ({message.from_user.first_name}): {input_text}")
        print(f"Bot: {response_text}")

        await message.reply(response_text)

# Register the message handler
dp.register_message_handler(on_message, content_types=types.ContentTypes.TEXT)



if __name__ == "__main__":
    from aiogram import executor

    # Start the bot
    executor.start_polling(dp, on_startup=on_startup)

