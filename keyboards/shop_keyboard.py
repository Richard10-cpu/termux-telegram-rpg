"""Клавиатура магазина."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import Player, ItemType
from data import SHOP_ITEMS


def get_shop_main_keyboard() -> InlineKeyboardMarkup:
    """Главное меню магазина."""
    keyboard = [
        [InlineKeyboardButton(text="⚔️ Оружие и Броня", callback_data="shop_equipment")],
        [InlineKeyboardButton(text="📚 Заклинания", callback_data="shop_spells")],
        [InlineKeyboardButton(text="🧪 Зелья", callback_data="shop_potions")],
        [InlineKeyboardButton(text="🔙 Закрыть", callback_data="shop_close")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_equipment_keyboard(player: Player) -> InlineKeyboardMarkup:
    """Клавиатура оружия и брони."""
    keyboard = []

    for key, shop_item in SHOP_ITEMS.items():
        item = shop_item.item
        if item.item_type in (ItemType.WEAPON, ItemType.ARMOR):
            # Проверяем, куплен ли предмет
            owned = item.name in player.inventory
            status = "✅" if owned else ""

            button_text = f"{status} {item.name} - {item.cost}💰"
            keyboard.append([InlineKeyboardButton(
                text=button_text,
                callback_data=f"buy_{key}" if not owned else "shop_equipment"
            )])

    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="shop_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_spells_keyboard(player: Player) -> InlineKeyboardMarkup:
    """Клавиатура заклинаний."""
    keyboard = []

    for key, shop_item in SHOP_ITEMS.items():
        item = shop_item.item
        if item.is_spell:
            # Проверяем, изучено ли заклинание
            learned = item.name in player.spells
            can_learn = player.level >= item.required_level

            if learned:
                status = "✅"
            elif not can_learn:
                status = f"🔒{item.required_level}ур."
            else:
                status = ""

            button_text = f"{status} {item.name} - {item.cost}💰"

            callback = f"buy_{key}" if (not learned and can_learn) else "shop_spells"
            keyboard.append([InlineKeyboardButton(text=button_text, callback_data=callback)])

    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="shop_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_potions_keyboard(player: Player) -> InlineKeyboardMarkup:
    """Клавиатура зелий."""
    keyboard = []

    for key, shop_item in SHOP_ITEMS.items():
        item = shop_item.item
        if item.item_type == ItemType.CONSUMABLE:
            # Показываем количество зелий у игрока
            owned_count = player.potions.get(key, 0)
            count_text = f" (x{owned_count})" if owned_count > 0 else ""

            button_text = f"{item.name} - {item.cost}💰{count_text}"
            keyboard.append([InlineKeyboardButton(
                text=button_text,
                callback_data=f"buy_{key}"
            )])

    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="shop_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Для совместимости со старым кодом
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

shop_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)
