"""Клавиатура магазина."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


shop_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗡️ Купить Меч (50💰)"),
            KeyboardButton(text="🛡️ Купить Броню (80💰)")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True
)
