"""Модели данных RPG игры."""
from .player import Player, Equipment, DailyQuest
from .monster import Monster, MonsterTemplate
from .location import Location
from .item import Item, ItemType, ShopItem

__all__ = [
    'Player',
    'Equipment',
    'DailyQuest',
    'Monster',
    'MonsterTemplate',
    'Location',
    'Item',
    'ItemType',
    'ShopItem',
]
