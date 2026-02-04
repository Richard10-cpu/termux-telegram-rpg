"""Модели данных NPC и диалогов."""
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class NPCType(Enum):
    """Тип NPC."""
    QUEST_GIVER = "quest_giver"  # Даёт квесты
    MERCHANT = "merchant"  # Торговец
    STORY = "story"  # Сюжетный персонаж
    COMPANION = "companion"  # Союзник


class DialogueChoiceEffect(Enum):
    """Эффект выбора в диалоге."""
    NONE = "none"
    RECEIVE_QUEST = "receive_quest"
    COMPLETE_QUEST = "complete_quest"
    RECEIVE_ITEM = "receive_item"
    RECEIVE_GOLD = "receive_gold"
    UNLOCK_LOCATION = "unlock_location"
    CHANGE_REPUTATION = "change_reputation"


@dataclass
class DialogueChoice:
    """Выбор в диалоге."""
    text: str  # Текст выбора
    next_dialogue_id: Optional[str] = None  # ID следующего диалога
    effect: DialogueChoiceEffect = DialogueChoiceEffect.NONE
    effect_value: Optional[str] = None  # Значение эффекта (quest_id, item_key, etc.)
    effect_amount: int = 0  # Количество (золото, репутация)
    required_level: int = 1  # Требуемый уровень
    required_item: Optional[str] = None  # Требуемый предмет


@dataclass
class Dialogue:
    """Диалог с NPC."""
    dialogue_id: str
    npc_key: str
    text: str  # Текст диалога
    choices: list[DialogueChoice]
    is_first: bool = False  # Первый диалог при встрече
    required_chapter: int = 1  # Требуемая глава сюжета
    one_time: bool = False  # Показать только один раз


@dataclass
class NPC:
    """Персонаж (NPC)."""
    key: str
    name: str
    npc_type: NPCType
    location: str  # Локация где находится NPC
    description: str
    first_dialogue_id: str  # ID первого диалога
    emoji: str = "🧙"
    image_path: str = ""
    available_from_chapter: int = 1  # С какой главы доступен


@dataclass
class PlayerDialogueProgress:
    """Прогресс диалогов игрока."""
    viewed_dialogues: list[str] = None  # Просмотренные диалоги
    npc_relationships: dict[str, int] = None  # Отношения с NPC (-100 до 100)

    def __post_init__(self):
        """Инициализация."""
        if self.viewed_dialogues is None:
            self.viewed_dialogues = []
        if self.npc_relationships is None:
            self.npc_relationships = {}

    def mark_dialogue_viewed(self, dialogue_id: str) -> None:
        """Отметить диалог как просмотренный."""
        if dialogue_id not in self.viewed_dialogues:
            self.viewed_dialogues.append(dialogue_id)

    def has_viewed(self, dialogue_id: str) -> bool:
        """Проверить, был ли просмотрен диалог."""
        return dialogue_id in self.viewed_dialogues

    def change_relationship(self, npc_key: str, amount: int) -> None:
        """Изменить отношения с NPC."""
        current = self.npc_relationships.get(npc_key, 0)
        self.npc_relationships[npc_key] = max(-100, min(100, current + amount))

    def get_relationship(self, npc_key: str) -> int:
        """Получить уровень отношений с NPC."""
        return self.npc_relationships.get(npc_key, 0)

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return {
            'viewed_dialogues': self.viewed_dialogues,
            'npc_relationships': self.npc_relationships
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerDialogueProgress':
        """Создать из словаря."""
        return cls(
            viewed_dialogues=data.get('viewed_dialogues', []),
            npc_relationships=data.get('npc_relationships', {})
        )
