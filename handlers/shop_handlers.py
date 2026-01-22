"""Обработчики магазина."""
from aiogram import Router, F, types
from services import get_player_service
from keyboards import shop_keyboard, main_keyboard
from game_logic import purchase_item

router = Router()

player_service = get_player_service()


@router.message(F.text == "🛒 Магазин")
async def open_shop(message: types.Message) -> None:
    """Открыть магазин."""
    await message.answer("Добро пожаловать в лавку торговца! Что купишь?", reply_markup=shop_keyboard)


@router.message(F.text == "🗡️ Купить Меч (50💰)")
async def buy_sword(message: types.Message) -> None:
    """Купить меч."""
    if not message.from_user:
        return
    player = player_service.get_or_create(message.from_user.id)
    success, msg = purchase_item(player, "steel_sword")
    if success:
        player_service.save_player(player)
    await message.answer(msg)


@router.message(F.text == "🛡️ Купить Броню (80💰)")
async def buy_armor(message: types.Message) -> None:
    """Купить броню."""
    if not message.from_user:
        return
    player = player_service.get_or_create(message.from_user.id)
    success, msg = purchase_item(player, "leather_armor")
    if success:
        player_service.save_player(player)
    await message.answer(msg)


@router.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message) -> None:
    """Вернуться в главное меню."""
    await message.answer("Вы вернулись на главную.", reply_markup=main_keyboard)
