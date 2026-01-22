"""Модели данных сюжета."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class StoryChapter:
    """Глава сюжета."""
    chapter_id: int
    title: str
    description: str
    unlock_level: int
    location_requirement: Optional[str] = None
    boss_name: Optional[str] = None
    reward_gold: int = 0
    reward_exp: int = 0
    reward_item: Optional[str] = None

    def is_unlocked(self, player_level: int) -> bool:
        """Проверить, доступна ли глава."""
        return player_level >= self.unlock_level


@dataclass
class StoryProgress:
    """Прогресс игрока по сюжету."""
    current_chapter: int = 1
    completed_chapters: list[int] = None
    boss_defeated: dict[str, bool] = None

    def __post_init__(self):
        """Инициализация списков."""
        if self.completed_chapters is None:
            self.completed_chapters = []
        if self.boss_defeated is None:
            self.boss_defeated = {}

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return {
            'current_chapter': self.current_chapter,
            'completed_chapters': self.completed_chapters,
            'boss_defeated': self.boss_defeated
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'StoryProgress':
        """Создать из словаря."""
        return cls(
            current_chapter=data.get('current_chapter', 1),
            completed_chapters=data.get('completed_chapters', []),
            boss_defeated=data.get('boss_defeated', {})
        )

    def complete_chapter(self, chapter_id: int) -> None:
        """Отметить главу как завершённую."""
        if chapter_id not in self.completed_chapters:
            self.completed_chapters.append(chapter_id)
            self.current_chapter = chapter_id + 1

    def is_chapter_completed(self, chapter_id: int) -> bool:
        """Проверить, завершена ли глава."""
        return chapter_id in self.completed_chapters

    def defeat_boss(self, boss_name: str) -> None:
        """Отметить босса как побеждённого."""
        self.boss_defeated[boss_name] = True

    def is_boss_defeated(self, boss_name: str) -> bool:
        """Проверить, побеждён ли босс."""
        return self.boss_defeated.get(boss_name, False)
