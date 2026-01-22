"""Конфигурация бота."""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Data file
DATA_FILE = 'players_rpg.json'

# Game constants
HEAL_COST = 10
MIN_HP_FOR_BATTLE = 15
