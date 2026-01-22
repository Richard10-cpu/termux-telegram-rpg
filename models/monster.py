"""Модели данных монстров."""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Monster:
    """Монстр в бою."""
    key: str
    name: str
    hp: int
    max_hp: int
    power: int
    exp: int
    gold_range: Tuple[int, int]
    image_path: str = ""

    @classmethod
    def from_template(cls, template: 'MonsterTemplate') -> 'Monster':
        """Создать монстра из шаблона."""
        return cls(
            key=template.key,
            name=template.name,
            hp=template.hp,
            max_hp=template.hp,
            power=template.power,
            exp=template.exp,
            gold_range=(template.gold_min, template.gold_max),
            image_path=template.image_path
        )


@dataclass
class MonsterTemplate:
    """Шаблон монстра (статические данные)."""
    key: str
    name: str
    hp: int
    power: int
    exp: int
    gold_min: int
    gold_max: int
    min_level: int = 1
    image_path: str = ""

    def is_available_for_level(self, player_level: int) -> bool:
        """Проверить доступность монстра для уровня игрока."""
        return player_level >= self.min_level
