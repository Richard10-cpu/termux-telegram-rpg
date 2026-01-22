"""Модели данных игрока."""
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.story import StoryProgress


@dataclass
class BattleState:
    """Состояние активного боя."""
    monster_key: str
    monster_name: str
    monster_hp: int
    monster_max_hp: int
    monster_power: int
    monster_exp: int
    monster_gold_min: int
    monster_gold_max: int
    is_boss: bool = False
    is_elite: bool = False
    defending: bool = False  # Игрок защищается в этом ходу
    turn: int = 1

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'BattleState':
        """Создать из словаря."""
        return cls(
            monster_key=data['monster_key'],
            monster_name=data['monster_name'],
            monster_hp=data['monster_hp'],
            monster_max_hp=data['monster_max_hp'],
            monster_power=data['monster_power'],
            monster_exp=data['monster_exp'],
            monster_gold_min=data['monster_gold_min'],
            monster_gold_max=data['monster_gold_max'],
            is_boss=data.get('is_boss', False),
            is_elite=data.get('is_elite', False),
            defending=data.get('defending', False),
            turn=data.get('turn', 1)
        )


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
    mana: int = 50
    max_mana: int = 50
    level: int = 1
    exp: int = 0
    gold: int = 20
    power: int = 10
    inventory: List[str] = field(default_factory=lambda: ["Деревянная палка"])
    spells: List[str] = field(default_factory=list)  # Изученные заклинания
    location: str = "village"
    equipment: Equipment = field(default_factory=Equipment)
    quests: Dict[str, DailyQuest] = field(default_factory=lambda: {"daily": DailyQuest()})
    achievements: List[str] = field(default_factory=list)
    total_kills: int = 0
    story_progress: Optional['StoryProgress'] = None
    potions: Dict[str, int] = field(default_factory=lambda: {"health": 0, "mana": 0, "power": 0})
    battle_state: Optional[BattleState] = None

    def to_dict(self) -> dict:
        """Преобразовать в словарь для сохранения в JSON."""
        return {
            'user_id': self.user_id,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'level': self.level,
            'exp': self.exp,
            'gold': self.gold,
            'power': self.power,
            'inventory': self.inventory,
            'spells': self.spells,
            'location': self.location,
            'equipment': self.equipment.to_dict(),
            'quests': {k: v.to_dict() for k, v in self.quests.items()},
            'achievements': self.achievements,
            'total_kills': self.total_kills,
            'story_progress': self.story_progress.to_dict() if self.story_progress else None,
            'potions': self.potions,
            'battle_state': self.battle_state.to_dict() if self.battle_state else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Player':
        """Создать из словаря."""
        from models.story import StoryProgress

        equipment = Equipment.from_dict(data.get('equipment', {}))

        quests_data = data.get('quests', {})
        quests = {
            k: DailyQuest.from_dict(v) if isinstance(v, dict) else v
            for k, v in quests_data.items()
        }
        if 'daily' not in quests:
            quests['daily'] = DailyQuest()

        story_progress_data = data.get('story_progress')
        story_progress = StoryProgress.from_dict(story_progress_data) if story_progress_data else None

        battle_state_data = data.get('battle_state')
        battle_state = BattleState.from_dict(battle_state_data) if battle_state_data else None

        return cls(
            user_id=data['user_id'],
            hp=data.get('hp', 100),
            max_hp=data.get('max_hp', 100),
            mana=data.get('mana', 50),
            max_mana=data.get('max_mana', 50),
            level=data.get('level', 1),
            exp=data.get('exp', 0),
            gold=data.get('gold', 20),
            power=data.get('power', 10),
            inventory=data.get('inventory', ["Деревянная палка"]),
            spells=data.get('spells', []),
            location=data.get('location', 'village'),
            equipment=equipment,
            quests=quests,
            achievements=data.get('achievements', []),
            total_kills=data.get('total_kills', 0),
            story_progress=story_progress,
            potions=data.get('potions', {"health": 0, "mana": 0, "power": 0}),
            battle_state=battle_state
        )
