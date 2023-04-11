 
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TELEGRAM_API_KEY_CHATBOT, TG_USERID
from handlers import on_message

logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_API_KEY_CHATBOT)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Set bot_id
bot_id = None

async def on_startup(dp):
    global bot_id
    bot_data = await bot.get_me()
    bot_id = bot_data.id


if __name__ == "__main__":
    from aiogram import executor

    # Register the message handler
    # dp.register_message_handler(on_message, content_types=types.ContentTypes.TEXT | types.ContentTypes.PHOTO)
    dp.register_message_handler(lambda message: on_message(message, bot), content_types=types.ContentTypes.TEXT | types.ContentTypes.PHOTO)

    # Start the bot
    executor.start_polling(dp, on_startup=on_startup)

