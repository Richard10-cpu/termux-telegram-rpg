"""Клавиатура квестов."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


quest_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📦 Забрать награду"),
            KeyboardButton(text="🔄 Обновить")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True
)
