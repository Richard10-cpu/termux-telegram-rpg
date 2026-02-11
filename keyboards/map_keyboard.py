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
        [
            KeyboardButton(text="🌊 Морская бездна"),
            KeyboardButton(text="🏛️ Руины империи")
        ],
        [
            KeyboardButton(text="🔥 Преисподняя"),
            KeyboardButton(text="⚡ Пустота")
        ],
    ],
    resize_keyboard=True
)
