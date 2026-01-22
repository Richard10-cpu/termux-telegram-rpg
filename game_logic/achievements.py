"""Система достижений."""
from enum import Enum
from typing import Callable
from models import Player


class Achievement(Enum):
    """Перечисление достижений."""
    FIRST_BLOOD = "first_blood"
    MONSTER_HUNTER = "monster_hunter"
    RICH = "rich"
    EXPLORER = "explorer"


class AchievementInfo:
    """Информация о достижении."""

    def __init__(self, key: Achievement, name: str, emoji: str, check_fn: Callable[[Player], bool]):
        self.key = key
        self.name = name
        self.emoji = emoji
        self.check_fn = check_fn


# Правила получения достижений
ACHIEVEMENTS = {
    Achievement.FIRST_BLOOD: AchievementInfo(
        Achievement.FIRST_BLOOD,
        "Первая кровь",
        "🩸",
        lambda p: p.total_kills >= 1
    ),
    Achievement.MONSTER_HUNTER: AchievementInfo(
        Achievement.MONSTER_HUNTER,
        "Охотник на монстров",
        "🎯",
        lambda p: p.total_kills >= 10
    ),
    Achievement.RICH: AchievementInfo(
        Achievement.RICH,
        "Богач",
        "💰",
        lambda p: p.gold >= 100
    ),
    Achievement.EXPLORER: AchievementInfo(
        Achievement.EXPLORER,
        "Исследователь",
        "🗺️",
        lambda p: p.level >= 5
    ),
}


def check_and_award(player: Player, message: str) -> tuple[str, list[str]]:
    """Проверить и выдать достижения.

    Args:
        player: Игрок
        message: Текущее сообщение

    Returns:
        (updated_message, new_achievements)
    """
    new_achievements: list[str] = []

    for achievement, info in ACHIEVEMENTS.items():
        achievement_key = achievement.value

        # Пропускаем если уже есть
        if achievement_key in player.achievements:
            continue

        # Проверяем условие
        if info.check_fn(player):
            player.achievements.append(achievement_key)
            new_achievements.append(f"{info.emoji} {info.name}")
            message += f"\n\n🏆 Достижение: {info.name}!"

    return message, new_achievements


def get_achievement_name(key: str) -> str:
    """Получить название достижения по ключу."""
    try:
        achievement = Achievement(key)
        info = ACHIEVEMENTS.get(achievement)
        return info.name if info else key
    except ValueError:
        return key


def format_achievements(achievements: list[str]) -> str:
    """Отформатировать список достижений."""
    if not achievements:
        return ""

    names = [get_achievement_name(a) for a in achievements]
    return "\n🏆 Достижения: " + ", ".join(names)
