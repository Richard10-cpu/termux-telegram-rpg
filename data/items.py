"""Статические данные предметов."""
from models import Item, ItemType, ShopItem

SHOP_ITEMS: dict[str, ShopItem] = {
    "steel_sword": ShopItem(
        item=Item(
            key="steel_sword",
            name="Стальной меч",
            item_type=ItemType.WEAPON,
            cost=50,
            power_bonus=15,
            image_path="assets/images/items/steel_sword.png"
        ),
        unique=True
    ),
    "leather_armor": ShopItem(
        item=Item(
            key="leather_armor",
            name="Кожаная броня",
            item_type=ItemType.ARMOR,
            cost=80,
            max_hp_bonus=30,
            image_path="assets/images/items/leather_armor.png"
        ),
        unique=True
    ),
    "wooden_stick": ShopItem(
        item=Item(
            key="wooden_stick",
            name="Деревянная палка",
            item_type=ItemType.WEAPON,
            cost=10,
            power_bonus=3,
            image_path="assets/images/items/wooden_stick.png"
        ),
        unique=False
    ),
    "steel_axe": ShopItem(
        item=Item(
            key="steel_axe",
            name="Стальной топор",
            item_type=ItemType.WEAPON,
            cost=120,
            power_bonus=35,
            image_path="assets/images/items/steel_axe.png"
        ),
        unique=True
    )
}

# Карта названий предметов для команд экипирования
ITEM_KEYWORDS = {
    ItemType.WEAPON: ["Меч", "меч", "Палка", "Топор", "sword", "axe"],
    ItemType.ARMOR: ["Броня", "броня", "armor"]
}
