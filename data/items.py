"""Статические данные предметов."""
from models import Item, ItemType, ShopItem

SHOP_ITEMS: dict[str, ShopItem] = {
    "steel_sword": ShopItem(
        item=Item(
            key="steel_sword",
            name="Стальной меч",
            item_type=ItemType.WEAPON,
            cost=50,
            power_bonus=15
        ),
        unique=True
    ),
    "leather_armor": ShopItem(
        item=Item(
            key="leather_armor",
            name="Кожаная броня",
            item_type=ItemType.ARMOR,
            cost=80,
            max_hp_bonus=30
        ),
        unique=True
    )
}

# Карта названий предметов для команд экипирования
ITEM_KEYWORDS = {
    ItemType.WEAPON: ["Меч", "меч", "Палка", "Топор", "sword", "axe"],
    ItemType.ARMOR: ["Броня", "броня", "armor"]
}
