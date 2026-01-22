"""Обработчики карты и путешествий."""
from aiogram import Router, F, types
from aiogram.types import FSInputFile
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
    if not message.from_user:
        return
    player = player_service.get_or_create(message.from_user.id)
    text = format_location_info(str(player.location))
    
    loc_data = LOCATIONS.get(str(player.location))
    if loc_data and loc_data.image_path:
        photo = FSInputFile(loc_data.image_path)
        await message.answer_photo(photo, caption=text, reply_markup=map_keyboard)
    else:
        await message.answer(text, reply_markup=map_keyboard)


@router.message(F.text.in_(LOCATION_KEYS.keys()))
async def travel_to_location(message: types.Message) -> None:
    """Путешествовать в локацию."""
    if not message.from_user or not message.text:
        return
    location_key = LOCATION_KEYS[message.text]
    player = player_service.get_or_create(message.from_user.id)

    player.location = location_key
    player_service.save_player(player)

    loc_data = LOCATIONS[location_key]
    text = f"🚶 Вы переместились в {loc_data.name}!\n{loc_data.description}"
    
    if loc_data.image_path:
        photo = FSInputFile(loc_data.image_path)
        await message.answer_photo(photo, caption=text)
    else:
        await message.answer(text)
