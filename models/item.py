"""Модели данных предметов."""
from dataclasses import dataclass
from enum import Enum



class ItemType(Enum):
    """Тип предмета."""
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    SPELL = "spell"
    MISC = "misc"


@dataclass
class Item:
    """Предмет."""
    key: str
    name: str
    item_type: ItemType
    cost: int
    power_bonus: int = 0
    hp_bonus: int = 0
    max_hp_bonus: int = 0
    mana_cost: int = 0  # Стоимость маны для заклинаний
    spell_damage: int = 0  # Урон заклинания
    spell_heal: int = 0  # Лечение заклинания
    required_level: int = 1  # Требуемый уровень
    image_path: str = ""

    @property
    def is_equipable(self) -> bool:
        """Можно ли экипировать предмет."""
        return self.item_type in (ItemType.WEAPON, ItemType.ARMOR)

    @property
    def is_spell(self) -> bool:
        """Является ли предмет заклинанием."""
        return self.item_type == ItemType.SPELL


@dataclass
class ShopItem:
    """Товар в магазине."""
    item: Item
    unique: bool = True  # True - можно купить только один раз

    def can_purchase(self, player_inventory: list) -> bool:
        """Можно ли купить товар."""
        if not self.unique:
            return True
        return self.item.name not in player_inventory
