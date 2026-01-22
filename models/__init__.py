"""Модели данных RPG игры."""
from .player import Player, Equipment, DailyQuest, BattleState
from .monster import Monster, MonsterTemplate
from .location import Location
from .item import Item, ItemType, ShopItem
from .story import StoryChapter, StoryProgress

__all__ = [
    'Player',
    'Equipment',
    'DailyQuest',
    'BattleState',
    'Monster',
    'MonsterTemplate',
    'Location',
    'Item',
    'ItemType',
    'ShopItem',
    'StoryChapter',
    'StoryProgress',
]
