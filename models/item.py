"""Модели данных предметов."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ItemType(Enum):
    """Тип предмета."""
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
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

    @property
    def is_equipable(self) -> bool:
        """Можно ли экипировать предмет."""
        return self.item_type in (ItemType.WEAPON, ItemType.ARMOR)


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
