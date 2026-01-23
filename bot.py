# pyright: reportUnknownMemberType=false
"""Termux RPG Bot - Модульная версия.

Главный точка входа бота.
"""
import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from handlers import (
    commands_router,
    profile_router,
    battle_router,
    shop_router,
    map_router,
    quest_router,
    rest_router,
    story_router
)

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

# Инициализация бота и диспетчера
bot: Bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp: Dispatcher = Dispatcher()

# Регистрация роутеров
dp.include_router(commands_router)
dp.include_router(profile_router)
dp.include_router(battle_router)
dp.include_router(shop_router)
dp.include_router(map_router)
dp.include_router(quest_router)
dp.include_router(rest_router)
dp.include_router(story_router)


async def main() -> None:
    """Главная функция запуска бота."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logging.getLogger("aiogram").setLevel(logging.DEBUG)
    print("🤖 Termux RPG Bot запускается...")
    print("📡 Начинаем polling...")

    try:
        await dp.start_polling(bot)  # type: ignore[reportUnknownMemberType]
    except Exception as e:
        print(f"❌ Ошибка polling: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
