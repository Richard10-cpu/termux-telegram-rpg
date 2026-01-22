"""Клавиатуры для боевой системы."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import Player
from game_logic import get_spell_by_name


def get_battle_keyboard(player: Player, has_potions: bool = False) -> InlineKeyboardMarkup:
    """Кнопки действий в бою."""
    buttons = [
        [InlineKeyboardButton(text="⚔️ Атака", callback_data="battle_attack")],
    ]

    # Показываем кнопку заклинаний только если они есть
    if player.spells:
        buttons.append([InlineKeyboardButton(text="🔮 Заклинания", callback_data="battle_spells")])

    # Показываем кнопку зелий только если они есть
    if has_potions:
        buttons.append([InlineKeyboardButton(text="🧪 Зелья", callback_data="battle_potions")])

    buttons.append([InlineKeyboardButton(text="🛡️ Защита", callback_data="battle_defend")])
    buttons.append([InlineKeyboardButton(text="🏃 Бежать", callback_data="battle_flee")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_spells_battle_keyboard(player: Player) -> InlineKeyboardMarkup:
    """Выбор заклинания в бою."""
    buttons = []

    for spell_name in player.spells:
        spell = get_spell_by_name(spell_name)
        if spell:
            # Проверяем, хватает ли маны
            can_cast = player.mana >= spell.mana_cost
            mana_text = f"({spell.mana_cost} маны)"

            if spell.spell_damage > 0:
                effect_text = f"⚡{spell.spell_damage} урона"
            elif spell.spell_heal > 0:
                effect_text = f"💚{spell.spell_heal} HP"
            else:
                effect_text = ""

            button_text = f"{spell.name} {mana_text} {effect_text}"
            if not can_cast:
                button_text = f"❌ {button_text}"

            buttons.append([InlineKeyboardButton(
                text=button_text,
                callback_data=f"cast_{spell.key}" if can_cast else "battle_spells"
            )])

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="battle_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_potions_battle_keyboard(player: Player) -> InlineKeyboardMarkup:
    """Выбор зелья в бою."""
    buttons = []

    # Зелье здоровья
    if player.potions.get("health_potion", 0) > 0:
        count = player.potions["health_potion"]
        buttons.append([InlineKeyboardButton(
            text=f"❤️ Зелье здоровья (x{count})",
            callback_data="use_health_potion"
        )])

    # Зелье маны
    if player.potions.get("mana_potion", 0) > 0:
        count = player.potions["mana_potion"]
        buttons.append([InlineKeyboardButton(
            text=f"💙 Зелье маны (x{count})",
            callback_data="use_mana_potion"
        )])

    # Зелье силы
    if player.potions.get("power_potion", 0) > 0:
        count = player.potions["power_potion"]
        buttons.append([InlineKeyboardButton(
            text=f"💪 Зелье силы (x{count})",
            callback_data="use_power_potion"
        )])

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="battle_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
