"""Главная клавиатура бота."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⚔️ В бой!"),
            KeyboardButton(text="👤 Профиль")
        ],
        [
            KeyboardButton(text="🗺️ Карта"),
            KeyboardButton(text="📜 Квесты")
        ],
        [
            KeyboardButton(text="🛒 Магазин"),
            KeyboardButton(text="☕ Отдых (15💰)")
        ],
        [
            KeyboardButton(text="🏆 Рейтинг")
        ]
    ],
    resize_keyboard=True
)
