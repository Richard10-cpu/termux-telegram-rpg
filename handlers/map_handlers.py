"""Обработчики карты и путешествий."""
from aiogram import Router, F, types
from services import get_player_service
from keyboards import map_keyboard
from utils import format_location_info
from data import LOCATIONS

router = Router()

player_service = get_player_service()


# Карта локаций
LOCATION_KEYS = {
    "🏘️ Деревня": "village",
    "🌲 Тёмный лес": "forest",
    "🕳️ Пещера": "cave",
    "⛰️ Гора": "mountain"
}


@router.message(F.text == "🗺️ Карта")
async def show_map(message: types.Message) -> None:
    """Показать карту."""
    player = player_service.get_or_create(message.from_user.id)
    text = format_location_info(player.location)
    await message.answer(text, reply_markup=map_keyboard)


@router.message(F.text.in_(LOCATION_KEYS.keys()))
async def travel_to_location(message: types.Message) -> None:
    """Путешествовать в локацию."""
    location_key = LOCATION_KEYS[message.text]
    player = player_service.get_or_create(message.from_user.id)

    old_location = player.location
    player.location = location_key
    player_service.save_player(player)

    loc_data = LOCATIONS[location_key]
    await message.answer(f"🚶 Вы переместились в {loc_data.name}!\n{loc_data.description}")
