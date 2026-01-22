"""Модели данных игрока."""
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List


@dataclass
class Equipment:
    """Экипировка игрока."""
    weapon: Optional[str] = None
    armor: Optional[str] = None

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Equipment':
        """Создать из словаря."""
        return cls(
            weapon=data.get('weapon'),
            armor=data.get('armor')
        )


@dataclass
class DailyQuest:
    """Ежедневный квест."""
    date: Optional[str] = None  # YYYY-MM-DD
    kills: int = 0
    target: int = 5
    reward_claimed: bool = False

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'DailyQuest':
        """Создать из словаря."""
        return cls(
            date=data.get('date'),
            kills=data.get('kills', 0),
            target=data.get('target', 5),
            reward_claimed=data.get('reward_claimed', False)
        )


@dataclass
class Player:
    """Игрок."""
    user_id: int
    hp: int = 100
    max_hp: int = 100
    level: int = 1
    exp: int = 0
    gold: int = 20
    power: int = 10
    inventory: List[str] = field(default_factory=lambda: ["Деревянная палка"])
    location: str = "village"
    equipment: Equipment = field(default_factory=Equipment)
    quests: Dict[str, DailyQuest] = field(default_factory=lambda: {"daily": DailyQuest()})
    achievements: List[str] = field(default_factory=list)
    total_kills: int = 0

    def to_dict(self) -> dict:
        """Преобразовать в словарь для сохранения в JSON."""
        return {
            'user_id': self.user_id,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'level': self.level,
            'exp': self.exp,
            'gold': self.gold,
            'power': self.power,
            'inventory': self.inventory,
            'location': self.location,
            'equipment': self.equipment.to_dict(),
            'quests': {k: v.to_dict() for k, v in self.quests.items()},
            'achievements': self.achievements,
            'total_kills': self.total_kills
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Player':
        """Создать из словаря."""
        equipment = Equipment.from_dict(data.get('equipment', {}))

        quests_data = data.get('quests', {})
        quests = {
            k: DailyQuest.from_dict(v) if isinstance(v, dict) else v
            for k, v in quests_data.items()
        }
        if 'daily' not in quests:
            quests['daily'] = DailyQuest()

        return cls(
            user_id=data['user_id'],
            hp=data.get('hp', 100),
            max_hp=data.get('max_hp', 100),
            level=data.get('level', 1),
            exp=data.get('exp', 0),
            gold=data.get('gold', 20),
            power=data.get('power', 10),
            inventory=data.get('inventory', ["Деревянная палка"]),
            location=data.get('location', 'village'),
            equipment=equipment,
            quests=quests,
            achievements=data.get('achievements', []),
            total_kills=data.get('total_kills', 0)
        )
