"""Клавиатура карты."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


map_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏘️ Деревня"),
            KeyboardButton(text="🌲 Тёмный лес")
        ],
        [
            KeyboardButton(text="🕳️ Пещера"),
            KeyboardButton(text="⛰️ Гора")
        ],
    ],
    resize_keyboard=True
)
