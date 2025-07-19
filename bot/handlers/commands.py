"""
Telegram bot router for handling /start and /help commands.

Sends a welcome message with instructions on how to use the bot.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["start", "help"]))
async def send_welcome(message: Message):
    """
    Responds to /start and /help commands with a welcome message
    and instructions for using the bot.

    Args:
        message (Message): Incoming Telegram message.
    """
    await message.reply(
        "Привет! 👋 Пришли мне кадастровый номер "
        "(например: 77:06:0012018:1000), и я выведу информацию об объекте из Росреестра."
    )
