"""Обработчики команд."""
from aiogram import Router, types
from aiogram.filters import Command
from services import get_player_service
from keyboards import main_keyboard
from game_logic import equip_item
from game_logic.story import get_current_chapter
from utils import format_top_players

router = Router()

player_service = get_player_service()


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """Команда /start - начало игры."""
    if not message.from_user:
        return
    player = player_service.get_or_create(message.from_user.id)

    # Получаем текущую главу сюжета
    current_chapter = get_current_chapter(player)

    welcome_msg = "🕹️ Добро пожаловать в Termux RPG!\n\n"

    if current_chapter:
        welcome_msg += f"📖 {current_chapter.title}\n\n"
        welcome_msg += f"{current_chapter.description}\n\n"
        welcome_msg += "⚔️ Используйте кнопки ниже для взаимодействия с игрой!"
    else:
        welcome_msg += "Исследуй мир, сражайся и прокачивайся!"

    await message.answer(welcome_msg, reply_markup=main_keyboard)


@router.message(Command("equip"))
async def cmd_equip(message: types.Message) -> None:
    """Команда /equip - экипировать предмет."""
    if not message.from_user or not message.text:
        return
    player = player_service.get_or_create(message.from_user.id)

    # Получаем название предмета из команды
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Укажите предмет для экипирования!\nПример: /equip Стальной меч")
        return

    item_name = args[1]

    success, msg = equip_item(player, item_name)
    if success:
        player_service.save_player(player)

    await message.answer(msg)


@router.message(Command("top"))
async def cmd_top(message: types.Message) -> None:
    """Команда /top - топ игроков."""
    top_players = player_service.get_top_players(10)

    if not top_players:
        await message.answer("📊 Пока нет игроков в рейтинге.")
        return

    text = format_top_players(top_players)
    await message.answer(text)
