"""Обработчики профиля."""
from aiogram import Router, F, types
from services import get_player_service
from utils import format_profile

router = Router()

player_service = get_player_service()


@router.message(F.text == "👤 Профиль")
async def show_profile(message: types.Message) -> None:
    """Показать профиль игрока."""
    player = player_service.get_or_create(message.from_user.id)
    text = format_profile(player)
    await message.answer(text)
