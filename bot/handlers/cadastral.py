"""
Telegram bot router module for handling cadastral number queries.

It fetches cadastral data with caching, formats and sends info,
and plots cadastral polygons on maps with refresh support.
"""

import asyncio
from datetime import timezone, timedelta

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
    Message,
    CallbackQuery,
)
from aiogram import Router
from pynspd import Nspd

from utils.cache import SimpleCache
from utils.formatter import format_cadastral_info
from utils.plotter import plot_polygon

router = Router()
cache = SimpleCache()

MOSCOW_TZ = timezone(timedelta(hours=3))


async def fetch_and_send_real_data(message: Message, cadastral_number: str):
    """
    Fetch cadastral data for the given number from the external service,
    cache the result, and send formatted info and map to the user.

    Args:
        message (Message): Incoming Telegram message to respond to.
        cadastral_number (str): Cadastral number string to search.
    """

    try:
        with Nspd() as nspd:
            feat = nspd.find(cadastral_number)

            if not feat or (isinstance(feat, dict) and feat.get("code") == 204):
                await message.answer("❌ Объект с таким кадастровым номером не найден.")
                return

            await cache.set(cadastral_number, feat)

            info, coords = format_cadastral_info(feat)
            await message.answer(info, parse_mode="Markdown")

            if coords:
                map_file = plot_polygon(coords, cadastral_number)
                photo = FSInputFile(map_file)
                await message.answer_photo(photo=photo)

    except Exception as e:
        await message.answer(f"❌ Ошибка при получении данных: {str(e)}")
        return



@router.callback_query()
async def process_callback(callback_query: CallbackQuery):
    """
    Handle callback queries from inline keyboard buttons.

    If the callback data starts with 'refresh:', it refreshes the
    cadastral data for the specified cadastral number.

    Args:
        callback_query (CallbackQuery): The incoming callback query.
    """
    data = callback_query.data

    if data.startswith("refresh:"):
        cadastral_number = data[len("refresh:") :]

        await callback_query.answer("🔄 Обновляю информацию...")
        await fetch_and_send_real_data(callback_query.message, cadastral_number)


@router.message()
async def get_cadastral_info(message: Message):
    """
    Handle incoming messages assumed to contain cadastral numbers.

    Checks the cache and sends cached data if available, otherwise fetches fresh data.

    Args:
        message (Message): Incoming Telegram message containing cadastral number.
    """
    cadastral_number = message.text.strip()
    await message.answer(
        f"🔍 Ищу информацию для кадастрового номера: {cadastral_number}"
    )

    cached = await cache.get(cadastral_number)

    if cached:
        feat, created_at = cached
        info, coords = format_cadastral_info(feat)

        created_at_local = created_at.astimezone(MOSCOW_TZ)
        formatted_time = created_at_local.strftime("%Y-%m-%d %H:%M:%S")

        info += f"\n\n🔁 *Данные из кэша от:* `{formatted_time}`"

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔄 Обновить информацию",
                        callback_data=f"refresh:{cadastral_number}",
                    )
                ]
            ]
        )

        await message.answer(info, parse_mode="Markdown", reply_markup=keyboard)

        if coords:
            map_file = plot_polygon(coords, cadastral_number)
            photo = FSInputFile(map_file)
            await message.answer_photo(photo=photo)

    else:
        await fetch_and_send_real_data(message, cadastral_number)
