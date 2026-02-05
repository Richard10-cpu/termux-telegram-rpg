"""Система достижений."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Achievement:
    """Достижение."""
    achievement_id: str
    title: str
    description: str
    icon: str
    reward_gold: int = 0
    reward_exp: int = 0
    reward_item: Optional[str] = None
    hidden: bool = False  # Скрытое достижение
    rarity: str = "common"  # common, rare, epic, legendary


# ============= ДОСТИЖЕНИЯ =============

ACHIEVEMENTS = {
    # === Боевые достижения ===
    "first_blood": Achievement(
        achievement_id="first_blood",
        title="⚔️ Первая кровь",
        description="Победите своего первого врага",
        icon="⚔️",
        reward_gold=50,
        reward_exp=25,
        rarity="common"
    ),

    "slayer_100": Achievement(
        achievement_id="slayer_100",
        title="💀 Истребитель",
        description="Уби��те 100 врагов",
        icon="💀",
        reward_gold=500,
        reward_exp=250,
        rarity="rare"
    ),

    "slayer_1000": Achievement(
        achievement_id="slayer_1000",
        title="☠️ Легенда войны",
        description="Убейте 1000 врагов",
        icon="☠️",
        reward_gold=5000,
        reward_exp=2500,
        reward_item="Кольцо берсерка",
        rarity="epic"
    ),

    "boss_slayer": Achievement(
        achievement_id="boss_slayer",
        title="👑 Убийца боссов",
        description="Победите всех 8 сюжетных боссов",
        icon="👑",
        reward_gold=10000,
        reward_exp=5000,
        reward_item="Корона победителя",
        rarity="legendary"
    ),

    "no_damage_boss": Achievement(
        achievement_id="no_damage_boss",
        title="🛡️ Непобедимый",
        description="Победите босса не получив урона",
        icon="🛡️",
        reward_gold=1000,
        reward_exp=500,
        rarity="epic"
    ),

    # === Прогрессия ===
    "level_10": Achievement(
        achievement_id="level_10",
        title="⭐ Новичок",
        description="Достигните 10 уровня",
        icon="⭐",
        reward_gold=100,
        reward_exp=50,
        rarity="common"
    ),

    "level_25": Achievement(
        achievement_id="level_25",
        title="🌟 Опытный",
        description="Достигните 25 уровня",
        icon="🌟",
        reward_gold=500,
        reward_exp=250,
        rarity="rare"
    ),

    "level_40": Achievement(
        achievement_id="level_40",
        title="✨ Мастер",
        description="Достигните 40 уровня",
        icon="✨",
        reward_gold=2000,
        reward_exp=1000,
        rarity="epic"
    ),

    "max_level": Achievement(
        achievement_id="max_level",
        title="💫 Легенда",
        description="Достигните максимального уровня (50+)",
        icon="💫",
        reward_gold=10000,
        reward_exp=5000,
        reward_item="Аура легенды",
        rarity="legendary"
    ),

    # === Богатство ===
    "rich_1000": Achievement(
        achievement_id="rich_1000",
        title="💰 Зажиточный",
        description="Накопите 1000 золота",
        icon="💰",
        reward_exp=100,
        rarity="common"
    ),

    "rich_10000": Achievement(
        achievement_id="rich_10000",
        title="💎 Богач",
        description="Накопите 10000 золота",
        icon="💎",
        reward_exp=500,
        rarity="rare"
    ),

    "millionaire": Achievement(
        achievement_id="millionaire",
        title="👑 Миллионер",
        description="Накопите 100000 золота",
        icon="👑",
        reward_item="Золотая корона",
        rarity="legendary"
    ),

    # === Исследование ===
    "explorer": Achievement(
        achievement_id="explorer",
        title="🗺️ Исследователь",
        description="Посетите все локации",
        icon="🗺️",
        reward_gold=500,
        reward_exp=250,
        rarity="rare"
    ),

    "quest_master": Achievement(
        achievement_id="quest_master",
        title="📜 Мастер квестов",
        description="Выполните все побочные квесты",
        icon="📜",
        reward_gold=2000,
        reward_exp=1000,
        reward_item="Книга знаний",
        rarity="epic"
    ),

    # === Социальные ===
    "friendly": Achievement(
        achievement_id="friendly",
        title="🤝 Дружелюбный",
        description="Достигните репутации +50 с любым NPC",
        icon="🤝",
        reward_gold=300,
        reward_exp=150,
        rarity="rare"
    ),

    "loved_by_all": Achievement(
        achievement_id="loved_by_all",
        title="💝 Любимец всех",
        description="Достигните репутации +80 со всеми NPC",
        icon="💝",
        reward_gold=2000,
        reward_exp=1000,
        reward_item="Амулет обаяния",
        rarity="epic"
    ),

    # === Сюжет ===
    "story_complete": Achievement(
        achievement_id="story_complete",
        title="📖 Спаситель мира",
        description="Пройдите основной сюжет (все 8 глав)",
        icon="📖",
        reward_gold=15000,
        reward_exp=7500,
        reward_item="Титул Героя",
        rarity="legendary"
    ),

    "true_ending": Achievement(
        achievement_id="true_ending",
        title="🌟 Истинный финал",
        description="Получите секретную концовку",
        icon="🌟",
        reward_gold=20000,
        reward_exp=10000,
        reward_item="Корона творца",
        rarity="legendary",
        hidden=True
    ),

    # === Пасхалки и секреты ===
    "cake_is_a_lie": Achievement(
        achievement_id="cake_is_a_lie",
        title="🎂 Торт - это ложь",
        description="Найдите отсылку к Portal",
        icon="🎂",
        reward_gold=300,
        reward_exp=100,
        rarity="rare",
        hidden=True
    ),

    "arrow_to_the_knee": Achievement(
        achievement_id="arrow_to_the_knee",
        title="🏹 Стрела в колено",
        description="Встретьте легендарного стражника",
        icon="🏹",
        reward_gold=200,
        reward_exp=100,
        rarity="common",
        hidden=True
    ),

    "matrix_awakened": Achievement(
        achievement_id="matrix_awakened",
        title="💊 Пробуждённый",
        description="Выберите красную таблетку",
        icon="💊",
        reward_gold=500,
        reward_exp=250,
        rarity="rare",
        hidden=True
    ),

    "lucky_lottery": Achievement(
        achievement_id="lucky_lottery",
        title="🎰 Невероятная удача",
        description="Выиграйте в лотерею (шанс 0.1%)",
        icon="🎰",
        reward_item="Талисман удачи",
        rarity="legendary",
        hidden=True
    ),

    "dragon_master": Achievement(
        achievement_id="dragon_master",
        title="🐉 Повелитель драконов",
        description="Найдите и вырастите драконьего питомца",
        icon="🐉",
        reward_gold=5000,
        reward_exp=2500,
        rarity="legendary",
        hidden=True
    ),

    # === Челленджи ===
    "speedrunner": Achievement(
        achievement_id="speedrunner",
        title="⚡ Спидраннер",
        description="Пройдите игру за 24 часа игрового времени",
        icon="⚡",
        reward_gold=10000,
        reward_exp=5000,
        reward_item="Сапоги скорости",
        rarity="legendary",
        hidden=True
    ),

    "pacifist": Achievement(
        achievement_id="pacifist",
        title="☮️ Пацифист",
        description="Пройдите главу убив менее 5 врагов",
        icon="☮️",
        reward_gold=1000,
        reward_exp=500,
        rarity="epic",
        hidden=True
    ),

    "hoarder": Achievement(
        achievement_id="hoarder",
        title="📦 Коллекционер",
        description="Соберите 50+ предметов в инвентарь",
        icon="📦",
        reward_gold=1000,
        reward_exp=500,
        rarity="rare"
    ),

    "magic_master": Achievement(
        achievement_id="magic_master",
        title="🧙 Архимаг",
        description="Изучите все заклинания",
        icon="🧙",
        reward_gold=2000,
        reward_exp=1000,
        reward_item="Посох архимага",
        rarity="epic"
    ),

    # === Смерть и неудачи ===
    "first_death": Achievement(
        achievement_id="first_death",
        title="💀 Первая смерть",
        description="Проиграйте битву в первый раз",
        icon="💀",
        reward_exp=50,
        rarity="common"
    ),

    "immortal": Achievement(
        achievement_id="immortal",
        title="👼 Бессмертный",
        description="Пройдите игру ни разу не умерев",
        icon="👼",
        reward_gold=20000,
        reward_exp=10000,
        reward_item="Аура бессмертия",
        rarity="legendary",
        hidden=True
    ),

    # === Особые ===
    "time_traveler": Achievement(
        achievement_id="time_traveler",
        title="⏰ Путешественник во времени",
        description="Встретьте себя из будущего",
        icon="⏰",
        reward_gold=1000,
        reward_exp=500,
        rarity="epic",
        hidden=True
    ),

    "merchant_best_friend": Achievement(
        achievement_id="merchant_best_friend",
        title="🛒 Лучший клиент",
        description="Потратьте 10000 золота в магазине",
        icon="🛒",
        reward_gold=1000,
        reward_item="Карта лояльности",
        rarity="rare"
    ),

    "code_breaker": Achievement(
        achievement_id="code_breaker",
        title="🔓 Взломщик кода",
        description="Найдите секретный код в игре",
        icon="🔓",
        reward_gold=5000,
        reward_exp=2500,
        rarity="legendary",
        hidden=True
    )
}


def get_achievement(achievement_id: str) -> Optional[Achievement]:
    """Получить достижение по ID."""
    return ACHIEVEMENTS.get(achievement_id)


def check_achievement_unlock(player, achievement_id: str) -> bool:
    """Проверить, разблокировано ли достижение."""
    if not hasattr(player, 'achievements'):
        player.achievements = []
    return achievement_id in player.achievements


def unlock_achievement(player, achievement_id: str) -> tuple[bool, str]:
    """Разблокировать достижение."""
    if not hasattr(player, 'achievements'):
        player.achievements = []

    if achievement_id in player.achievements:
        return False, ""

    achievement = get_achievement(achievement_id)
    if not achievement:
        return False, ""

    player.achievements.append(achievement_id)

    # Выдать награды
    rewards = []
    if achievement.reward_gold > 0:
        player.gold += achievement.reward_gold
        rewards.append(f"{achievement.reward_gold}💰")

    if achievement.reward_exp > 0:
        player.exp += achievement.reward_exp
        rewards.append(f"{achievement.reward_exp}📊")

    if achievement.reward_item:
        player.inventory.append(achievement.reward_item)
        rewards.append(f"'{achievement.reward_item}'")

    reward_text = ", ".join(rewards) if rewards else "Только слава!"

    rarity_emoji = {
        "common": "⚪",
        "rare": "🔵",
        "epic": "🟣",
        "legendary": "🟡"
    }

    msg = (
        f"🎉 ДОСТИЖЕНИЕ РАЗБЛОКИРОВАНО! {rarity_emoji.get(achievement.rarity, '')}\n\n"
        f"{achievement.icon} {achievement.title}\n"
        f"📝 {achievement.description}\n\n"
        f"🎁 Награда: {reward_text}"
    )

    return True, msg


def get_player_achievements_summary(player) -> str:
    """Получить сводку достижений игрока."""
    if not hasattr(player, 'achievements'):
        player.achievements = []

    total = len(ACHIEVEMENTS)
    unlocked = len(player.achievements)
    percentage = (unlocked / total * 100) if total > 0 else 0

    visible_achievements = {k: v for k, v in ACHIEVEMENTS.items() if not v.hidden or k in player.achievements}

    text = f"🏆 ДОСТИЖЕНИЯ ({unlocked}/{total})\n"
    text += f"📊 Прогресс: {percentage:.1f}%\n\n"

    by_rarity = {"legendary": [], "epic": [], "rare": [], "common": []}

    for ach_id, ach in visible_achievements.items():
        status = "✅" if ach_id in player.achievements else "🔒"
        by_rarity[ach.rarity].append(f"{status} {ach.icon} {ach.title}")

    for rarity in ["legendary", "epic", "rare", "common"]:
        if by_rarity[rarity]:
            rarity_names = {"legendary": "🟡 Легендарные", "epic": "🟣 Эпические", "rare": "🔵 Редкие", "common": "⚪ Обычные"}
            text += f"\n{rarity_names[rarity]}:\n"
            text += "\n".join(by_rarity[rarity]) + "\n"

    return text
