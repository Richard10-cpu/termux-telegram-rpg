"""Обработчики магазина."""
from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from services import get_player_service
from keyboards.shop_keyboard import get_shop_main_keyboard, get_equipment_keyboard, get_spells_keyboard, get_potions_keyboard
from keyboards import main_keyboard
from game_logic import purchase_item
from data import SHOP_ITEMS

router = Router()

player_service = get_player_service()


@router.message(F.text == "🛒 Магазин")
async def open_shop(message: types.Message) -> None:
    """Открыть магазин."""
    if not message.from_user:
        return

    player = player_service.get_or_create(message.from_user.id)

    text = (
        "🏪 Добро пожаловать в магазин!\n\n"
        f"💰 Ваше золото: {player.gold}\n"
        f"⚡ Мана: {player.mana}/{player.max_mana}\n\n"
        "Выберите категорию:"
    )

    await message.answer(text, reply_markup=get_shop_main_keyboard())


@router.callback_query(F.data == "shop_main")
async def callback_shop_main(callback: CallbackQuery) -> None:
    """Главное меню магазина."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)

    text = (
        "🏪 Добро пожаловать в магазин!\n\n"
        f"💰 Ваше золото: {player.gold}\n"
        f"⚡ Мана: {player.mana}/{player.max_mana}\n\n"
        "Выберите категорию:"
    )

    await callback.message.edit_text(text, reply_markup=get_shop_main_keyboard())
    await callback.answer()


@router.callback_query(F.data == "shop_equipment")
async def callback_shop_equipment(callback: CallbackQuery) -> None:
    """Показать оружие и броню."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)

    text = (
        "⚔️ ОРУЖИЕ И БРОНЯ\n\n"
        f"💰 Ваше золото: {player.gold}\n\n"
        "Выберите товар:"
    )

    await callback.message.edit_text(text, reply_markup=get_equipment_keyboard(player))
    await callback.answer()


@router.callback_query(F.data == "shop_spells")
async def callback_shop_spells(callback: CallbackQuery) -> None:
    """Показать заклинания."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)

    text = (
        "📚 ЗАКЛИНАНИЯ\n\n"
        f"💰 Ваше золото: {player.gold}\n"
        f"👤 Ваш уровень: {player.level}\n\n"
        "🔒 - требуется уровень\n"
        "✅ - уже изучено\n\n"
        "Выберите заклинание:"
    )

    await callback.message.edit_text(text, reply_markup=get_spells_keyboard(player))
    await callback.answer()


@router.callback_query(F.data == "shop_potions")
async def callback_shop_potions(callback: CallbackQuery) -> None:
    """Показать зелья."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)

    text = (
        "🧪 ЗЕЛЬЯ\n\n"
        f"💰 Ваше золото: {player.gold}\n\n"
        "❤️ Зелье здоровья - восстанавливает 50 HP\n"
        "💙 Зелье маны - восстанавливает 40 маны\n"
        "💪 Зелье силы - +50% урона на 3 хода\n\n"
        "Выберите зелье:"
    )

    await callback.message.edit_text(text, reply_markup=get_potions_keyboard(player))
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def callback_buy_item(callback: CallbackQuery) -> None:
    """Купить предмет."""
    if not callback.from_user or not callback.message or not callback.data:
        return

    player = player_service.get_or_create(callback.from_user.id)

    # Получаем ключ предмета
    item_key = callback.data.replace("buy_", "")
    shop_item = SHOP_ITEMS.get(item_key)

    if not shop_item:
        await callback.answer("❌ Предмет не найден!")
        return

    # Покупаем
    success, msg = purchase_item(player, item_key)

    if success:
        player_service.save_player(player)

        # Обновляем клавиатуру
        from models import ItemType
        if shop_item.item.is_spell:
            keyboard = get_spells_keyboard(player)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        elif shop_item.item.item_type == ItemType.CONSUMABLE:
            keyboard = get_potions_keyboard(player)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        else:
            keyboard = get_equipment_keyboard(player)
            await callback.message.edit_reply_markup(reply_markup=keyboard)

    await callback.answer(msg, show_alert=True)


@router.callback_query(F.data == "shop_close")
async def callback_shop_close(callback: CallbackQuery) -> None:
    """Закрыть магазин."""
    if not callback.message:
        return

    await callback.message.delete()
    await callback.answer("Магазин закрыт")


# Обработчик для старой кнопки "Назад"
@router.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message) -> None:
    """Вернуться в главное меню."""
    await message.answer("Вы вернулись на главную.", reply_markup=main_keyboard)
