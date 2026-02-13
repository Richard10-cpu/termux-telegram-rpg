"""Обработчики команд."""
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from services import get_player_service
from keyboards import main_keyboard
from game_logic import equip_item
from game_logic.story import get_current_chapter
from utils import format_top_players
import os

router = Router()

player_service = get_player_service()

# URL веб-приложения
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-domain.com")  # Замените на ваш домен


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
        welcome_msg += f"📖 {current_chapter.title}\n"
        welcome_msg += f"📍 Цель: Победить {current_chapter.boss_name}\n\n"
        welcome_msg += "📜 Откройте 'Квесты' для деталей сюжета"
    else:
        welcome_msg += "🏆 Вы прошли все главы сюжета!\n"
        welcome_msg += "Продолжайте сражаться и выполнять ежедневные квесты!"

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


@router.message(Command("webapp"))
async def cmd_webapp(message: types.Message) -> None:
    """Команда /webapp - открыть веб-приложение."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎮 Открыть Mini App",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])

    await message.answer(
        "🌟 <b>Termux RPG Mini App</b>\n\n"
        "Играйте в улучшенной версии с красивым интерфейсом!\n\n"
        "✨ Что нового:\n"
        "• 🎨 Современный дизайн\n"
        "• ⚔️ Визуализация боёв\n"
        "• 🗺️ Интерактивная карта\n"
        "• 📊 Подробная статистика\n"
        "• 🎒 Удобный инвентарь\n\n"
        "Нажмите кнопку ниже чтобы открыть!",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    """Команда /help - помощь."""
    help_text = """
🎮 <b>TERMUX RPG - ПОМОЩЬ</b>

📱 <b>Основные команды:</b>
/start - Начать игру
/webapp - Открыть Mini App 🌟
/profile - Ваш профиль
/inventory - Инвентарь
/map - Карта мира
/fight - Сразиться с врагом
/shop - Магазин
/equip <предмет> - Экипировать
/top - Рейтинг игроков

🎯 <b>Дополнительные команды:</b>
/achievements - Достижения
/pets - Питомцы
/casino - Казино
/craft - Крафт
/fishing - Рыбалка
/arena - Арена

📖 <b>Сюжет:</b>
/story - Продолжить историю
/quests - Активные квесты

💡 <b>Совет:</b>
Используйте /webapp для лучшего игрового опыта!
"""
    await message.answer(help_text, parse_mode="HTML")
