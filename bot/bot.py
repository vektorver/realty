"""
This module initializes the Telegram bot with Aiogram,
sets up command and cadastral handlers, and starts polling.
"""

import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import commands, cadastral

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.include_router(commands.router)
dp.include_router(cadastral.router)


async def main():
    """
    Entry point for the bot polling loop.
    Starts the dispatcher polling to receive updates from Telegram.
    """
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
