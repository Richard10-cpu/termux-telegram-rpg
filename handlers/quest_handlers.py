"""Обработчики квестов."""
from aiogram import Router, F, types
from services import get_player_service
from keyboards import quest_keyboard, main_keyboard
from game_logic import claim_daily_reward, format_quest_status, add_experience

router = Router()

player_service = get_player_service()


@router.message(F.text == "📜 Квесты")
async def show_quests(message: types.Message) -> None:
    """Показать квесты."""
    player = player_service.get_or_create(message.from_user.id)
    text = format_quest_status(player)
    player_service.save_player(player)
    await message.answer(text, reply_markup=quest_keyboard)


@router.message(F.text == "📦 Забрать награду")
async def claim_quest_reward(message: types.Message) -> None:
    """Получить награду за квест."""
    player = player_service.get_or_create(message.from_user.id)
    success, msg = claim_daily_reward(player)
    if success:
        # Опыт уже добавлен в claim_daily_reward
        player_service.save_player(player)
        await message.answer(msg, reply_markup=main_keyboard)
    else:
        await message.answer(msg)


@router.message(F.text == "🔄 Обновить")
async def refresh_quests(message: types.Message) -> None:
    """Обновить информацию о квестах."""
    player = player_service.get_or_create(message.from_user.id)
    text = format_quest_status(player)
    player_service.save_player(player)
    await message.answer(text, reply_markup=quest_keyboard)
