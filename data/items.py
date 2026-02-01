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
    ),
    # Заклинания
    "fireball": ShopItem(
        item=Item(
            key="fireball",
            name="⚡ Огненный шар",
            item_type=ItemType.SPELL,
            cost=100,
            mana_cost=15,
            spell_damage=40,
            required_level=3,
            image_path="assets/images/spells/fireball.png"
        ),
        unique=True
    ),
    "heal": ShopItem(
        item=Item(
            key="heal",
            name="✨ Исцеление",
            item_type=ItemType.SPELL,
            cost=80,
            mana_cost=20,
            spell_heal=50,
            required_level=2,
            image_path="assets/images/spells/heal.png"
        ),
        unique=True
    ),
    "lightning": ShopItem(
        item=Item(
            key="lightning",
            name="⚡ Молния",
            item_type=ItemType.SPELL,
            cost=200,
            mana_cost=25,
            spell_damage=70,
            required_level=7,
            image_path="assets/images/spells/lightning.png"
        ),
        unique=True
    ),
    "ice_blast": ShopItem(
        item=Item(
            key="ice_blast",
            name="❄️ Ледяной взрыв",
            item_type=ItemType.SPELL,
            cost=300,
            mana_cost=30,
            spell_damage=90,
            required_level=12,
            image_path="assets/images/spells/ice_blast.png"
        ),
        unique=True
    ),
    "regeneration": ShopItem(
        item=Item(
            key="regeneration",
            name="💚 Регенерация",
            item_type=ItemType.SPELL,
            cost=150,
            mana_cost=25,
            spell_heal=80,
            required_level=8,
            image_path="assets/images/spells/regeneration.png"
        ),
        unique=True
    ),
    # Зелья
    "health_potion": ShopItem(
        item=Item(
            key="health_potion",
            name="❤️ Зелье здоровья",
            item_type=ItemType.CONSUMABLE,
            cost=25,
            description="Восстанавливает 50 HP",
            image_path="assets/images/potions/health.png"
        ),
        unique=False
    ),
    "mana_potion": ShopItem(
        item=Item(
            key="mana_potion",
            name="💙 Зелье маны",
            item_type=ItemType.CONSUMABLE,
            cost=30,
            description="Восстанавливает 40 маны",
            image_path="assets/images/potions/mana.png"
        ),
        unique=False
    ),
    "power_potion": ShopItem(
        item=Item(
            key="power_potion",
            name="💪 Зелье силы",
            item_type=ItemType.CONSUMABLE,
            cost=50,
            description="Увеличивает урон на 50% на 3 хода",
            image_path="assets/images/potions/power.png"
        ),
        unique=False
    ),
    # Легендарные награды за сюжетные главы
    "trident_of_depths": ShopItem(
        item=Item(
            key="trident_of_depths",
            name="🔱 Трезубец морского владыки",
            item_type=ItemType.WEAPON,
            cost=0,  # Нельзя купить, только получить за квест
            power_bonus=60,
            max_hp_bonus=50,
            description="Легендарное оружие Левиафана. +60 силы, +50 HP",
            image_path="assets/images/items/trident.png"
        ),
        unique=True
    ),
    "staff_of_eternity": ShopItem(
        item=Item(
            key="staff_of_eternity",
            name="📜 Посох вечной магии",
            item_type=ItemType.WEAPON,
            cost=0,
            power_bonus=75,
            max_mana_bonus=100,
            mana_regen_bonus=5,
            description="Посох Архимага. +75 силы, +100 маны, +5 регена маны",
            image_path="assets/images/items/staff.png"
        ),
        unique=True
    ),
    "demon_crown": ShopItem(
        item=Item(
            key="demon_crown",
            name="👑 Корона покорителя демонов",
            item_type=ItemType.ARMOR,
            cost=0,
            max_hp_bonus=150,
            power_bonus=50,
            defense_bonus=40,
            description="Корона Абаддона. +150 HP, +50 силы, +40 защиты",
            image_path="assets/images/items/crown.png"
        ),
        unique=True
    ),
    "chaos_blade": ShopItem(
        item=Item(
            key="chaos_blade",
            name="⚔️ Клинок творения и разрушения",
            item_type=ItemType.WEAPON,
            cost=0,
            power_bonus=120,
            max_hp_bonus=100,
            max_mana_bonus=100,
            lifesteal=0.15,  # 15% вампиризма
            description="Величайшее оружие вселенной. +120 силы, +100 HP, +100 маны, 15% вампиризма",
            image_path="assets/images/items/chaos_blade.png"
        ),
        unique=True
    )
}

# Карта названий предметов для команд экипирования
ITEM_KEYWORDS = {
    ItemType.WEAPON: ["Меч", "меч", "Палка", "Топор", "sword", "axe"],
    ItemType.ARMOR: ["Броня", "броня", "armor"]
}
