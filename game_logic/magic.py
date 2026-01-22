"""Логика магии и заклинаний."""
from models import Player, BattleState
from data import SHOP_ITEMS


def get_spell_by_key(spell_key: str):
    """Получить заклинание по ключу."""
    shop_item = SHOP_ITEMS.get(spell_key)
    if shop_item and shop_item.item.is_spell:
        return shop_item.item
    return None


def get_spell_by_name(spell_name: str):
    """Получить заклинание по названию."""
    for shop_item in SHOP_ITEMS.values():
        if shop_item.item.is_spell and shop_item.item.name == spell_name:
            return shop_item.item
    return None


def cast_spell(player: Player, spell_key: str, state: BattleState) -> tuple[bool, str, int]:
    """Применить заклинание в бою.

    Returns:
        (success: bool, message: str, damage_to_monster: int)
    """
    spell = get_spell_by_key(spell_key)
    if not spell:
        return False, "❌ Заклинание не найдено!", 0

    # Проверяем, изучено ли заклинание
    if spell.name not in player.spells:
        return False, "❌ Вы не изучали это заклинание!", 0

    # Проверяем ману
    if player.mana < spell.mana_cost:
        return False, f"❌ Недостаточно маны! Требуется {spell.mana_cost}, у вас {player.mana}", 0

    # Списываем ману
    player.mana -= spell.mana_cost

    # Урон по монстру
    if spell.spell_damage > 0:
        damage = spell.spell_damage
        state.monster_hp -= damage
        return True, f"🔮 {spell.name} наносит {damage} урона врагу!", damage

    # Исцеление
    elif spell.spell_heal > 0:
        heal = min(spell.spell_heal, player.max_hp - player.hp)
        player.hp += heal
        return True, f"✨ {spell.name} восстанавливает {heal} HP!", 0

    return False, "❌ Неизвестный эффект заклинания!", 0


def use_potion(player: Player, potion_key: str, state: BattleState | None = None) -> tuple[bool, str]:
    """Использовать зелье.

    Returns:
        (success: bool, message: str)
    """
    # Проверяем наличие зелья
    if potion_key not in player.potions or player.potions[potion_key] <= 0:
        return False, "❌ У вас нет этого зелья!"

    potion = SHOP_ITEMS.get(potion_key)
    if not potion:
        return False, "❌ Зелье не найдено!"

    # Используем зелье
    player.potions[potion_key] -= 1

    if potion_key == "health_potion":
        heal = min(50, player.max_hp - player.hp)
        player.hp += heal
        return True, f"❤️ Зелье здоровья восстанавливает {heal} HP!"

    elif potion_key == "mana_potion":
        restore = min(40, player.max_mana - player.mana)
        player.mana += restore
        return True, f"💙 Зелье маны восстанавливает {restore} маны!"

    elif potion_key == "power_potion":
        # Зелье силы - пока просто сообщение, баффы добавим позже
        return True, "💪 Зелье силы! Ваш урон увеличен на 50% на 3 хода!"

    return False, "❌ Неизвестное зелье!"
