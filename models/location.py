"""Модели данных локаций."""
from dataclasses import dataclass
from typing import List


@dataclass
class Location:
    """Локация в игровом мире."""
    key: str
    name: str
    emoji: str
    enemies: List[str]  # Список ключей монстров
    description: str

    @property
    def has_enemies(self) -> bool:
        """Есть ли враги в локации."""
        return bool(self.enemies)

    @property
    def is_peaceful(self) -> bool:
        """Мирная ли локация."""
        return not self.has_enemies
