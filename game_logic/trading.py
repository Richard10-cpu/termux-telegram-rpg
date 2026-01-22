"""Логика торговли и экипирования."""
from models import Player, Item, ItemType
from data import SHOP_ITEMS, ITEM_KEYWORDS


def get_item_type(item_name: str) -> ItemType | None:
    """Определить тип предмета по названию."""
    for item_type, keywords in ITEM_KEYWORDS.items():
        if any(keyword in item_name for keyword in keywords):
            return item_type
    return None


def can_purchase_item(player: Player, item_key: str) -> tuple[bool, str]:
    """Проверить можно ли купить предмет.

    Returns:
        (can_purchase: bool, message: str)
    """
    shop_item = SHOP_ITEMS.get(item_key)
    if not shop_item:
        return False, "❌ Предмет не найден в магазине!"

    if player.gold < shop_item.item.cost:
        return False, "❌ Недостаточно золота!"

    if not shop_item.can_purchase(player.inventory):
        return False, f"❌ У вас уже есть {shop_item.item.name}!"

    return True, ""


def purchase_item(player: Player, item_key: str) -> tuple[bool, str]:
    """Купить предмет.

    Returns:
        (success: bool, message: str)
    """
    can_buy, error_msg = can_purchase_item(player, item_key)
    if not can_buy:
        return False, error_msg

    shop_item = SHOP_ITEMS[item_key]
    item = shop_item.item

    # Списываем золото
    player.gold -= item.cost

    # Применяем бонусы
    player.power += item.power_bonus
    player.max_hp += item.max_hp_bonus

    # Добавляем в инвентарь
    player.inventory.append(item.name)

    # Формируем сообщение
    if item.item_type == ItemType.WEAPON:
        msg = f"🗡️ Вы купили {item.name}! Сила значительно выросла."
    elif item.item_type == ItemType.ARMOR:
        msg = f"🛡️ Вы купили {item.name}! Максимальный HP +{item.max_hp_bonus}."
    else:
        msg = f"🎒 Вы купили {item.name}!"

    return True, msg


def equip_item(player: Player, item_name: str) -> tuple[bool, str]:
    """Экипировать предмет.

    Returns:
        (success: bool, message: str)
    """
    # Проверяем наличие предмета
    if item_name not in player.inventory:
        return False, "❌ У вас нет этого предмета!"

    # Определяем тип предмета
    item_type = get_item_type(item_name)
    if item_type is None:
        return False, "❌ Этот предмет нельзя экипировать!"

    equipment = player.equipment

    if item_type == ItemType.WEAPON:
        # Снимаем текущее оружие
        if equipment.weapon and equipment.weapon != item_name:
            player.inventory.append(equipment.weapon)
        equipment.weapon = item_name
        player.inventory.remove(item_name)
        return True, f"🗡️ Вы экипировали {item_name}!"

    elif item_type == ItemType.ARMOR:
        # Снимаем текущую броню
        if equipment.armor and equipment.armor != item_name:
            player.inventory.append(equipment.armor)
        equipment.armor = item_name
        player.inventory.remove(item_name)
        return True, f"🛡️ Вы экипировали {item_name}!"

    return False, "❌ Этот предмет нельзя экипировать!"


def get_item_by_name(item_name: str) -> Item | None:
    """Найти предмет по названию."""
    for shop_item in SHOP_ITEMS.values():
        if shop_item.item.name == item_name:
            return shop_item.item
    return None
