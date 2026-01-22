"""Логика опыта и уровней."""
from models import Player


class ExperienceConstants:
    """Константы системы опыта."""
    LEVEL_EXP_BASE = 60  # опыта для уровня 1 -> 2
    LEVEL_EXP_MULTIPLIER = 1  # множитель (linear: level * 60)
    HP_PER_LEVEL = 25
    POWER_PER_LEVEL = 5


def exp_for_level(level: int) -> int:
    """Получить необходимое количество опыта для уровня."""
    return level * ExperienceConstants.LEVEL_EXP_BASE


def check_level_up(player: Player) -> tuple[bool, str | None]:
    """Проверить повышение уровня.

    Returns:
        (level_up: bool, message: str | None)
    """
    required_exp = exp_for_level(player.level)

    if player.exp >= required_exp:
        # Повышаем уровень
        player.level += 1
        player.max_hp += ExperienceConstants.HP_PER_LEVEL
        player.hp = player.max_hp  # Полное лечение при повышении уровня
        player.power += ExperienceConstants.POWER_PER_LEVEL

        msg = (
            f"🆙 УРОВЕНЬ ПОВЫШЕН! "
            f"Теперь вы {player.level} уровня! "
            f"Сила и HP выросли."
        )
        return True, msg

    return False, None


def add_experience(player: Player, amount: int) -> tuple[bool, str | None]:
    """Добавить опыт и проверить повышение уровня.

    Returns:
        (level_up: bool, message: str | None)
    """
    player.exp += amount
    return check_level_up(player)
