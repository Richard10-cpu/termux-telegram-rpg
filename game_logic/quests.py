"""Система квестов - сюжетные и побочные."""
from datetime import datetime
from models import Player
from game_logic.story import get_story_progress, get_current_chapter
from data.story_chapters import get_chapter


class QuestConstants:
    """Константы системы квестов."""
    DAILY_TARGET = 5
    DAILY_REWARD_GOLD = 50
    DAILY_REWARD_EXP = 25


def get_today() -> str:
    """Получить сегодняшнюю дату в формате YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def update_daily_quest(player: Player) -> None:
    """Обновить дневной квест если сменился день."""
    today = get_today()

    if player.quests["daily"].date != today:
        player.quests["daily"] = player.quests["daily"]
        player.quests["daily"].date = today
        player.quests["daily"].kills = 0
        player.quests["daily"].reward_claimed = False


def increment_kills(player: Player, amount: int = 1) -> tuple[bool, str | None]:
    """Увеличить счётчик убийств для квеста.

    Returns:
        (completed: bool, message: str | None)
    """
    update_daily_quest(player)

    quest = player.quests["daily"]
    quest.kills += amount

    if quest.kills >= quest.target and not quest.reward_claimed:
        msg = f"\n\n📜 Ежедневный квест выполнен! ({quest.kills}/{quest.target})"
        return True, msg

    return False, None


def can_claim_reward(player: Player) -> tuple[bool, str]:
    """Проверить можно ли получить награду.

    Returns:
        (can_claim: bool, message: str)
    """
    quest = player.quests["daily"]

    if quest.reward_claimed:
        return False, "❌ Вы уже получили награду за сегодня!"

    if quest.kills < quest.target:
        return False, f"❌ Квест ещё не выполнен! Убито: {quest.kills}/{quest.target}"

    return True, ""


def claim_daily_reward(player: Player) -> tuple[bool, str]:
    """Получить награду за дневной квест.

    Returns:
        (success: bool, message: str)
    """
    can_claim, error_msg = can_claim_reward(player)
    if not can_claim:
        return False, error_msg

    player.gold += QuestConstants.DAILY_REWARD_GOLD
    player.exp += QuestConstants.DAILY_REWARD_EXP
    player.quests["daily"].reward_claimed = True

    msg = (
        f"🎁 Вы получили награду: "
        f"{QuestConstants.DAILY_REWARD_GOLD}💰 и "
        f"{QuestConstants.DAILY_REWARD_EXP}📊 опыта!"
    )
    return True, msg


def format_story_quest(player: Player) -> str:
    """Отформатировать сюжетный квест."""
    progress = get_story_progress(player)
    current_chapter = get_current_chapter(player)

    if not current_chapter:
        return "🏆 Все сюжетные главы пройдены!\n"

    text = f"📖 СЮЖЕТНЫЙ КВЕСТ\n"
    text += f"━━━━━━━━━━━━━━━━━━━━\n"
    text += f"{current_chapter.title}\n\n"

    # Проверяем требования
    requirements_met = True
    req_text = ""

    # Требование уровня
    if player.level < current_chapter.unlock_level:
        requirements_met = False
        req_text += f"❌ Уровень: {player.level}/{current_chapter.unlock_level}\n"
    else:
        req_text += f"✅ Уровень: {player.level}/{current_chapter.unlock_level}\n"

    # Требование локации
    if current_chapter.location_requirement:
        location_names = {
            "village": "Деревня",
            "forest": "Тёмный лес",
            "cave": "Пещера",
            "mountain": "Гора"
        }
        req_location = location_names.get(current_chapter.location_requirement, current_chapter.location_requirement)
        current_location = location_names.get(player.location, player.location)

        if player.location != current_chapter.location_requirement:
            requirements_met = False
            req_text += f"❌ Локация: {current_location} → {req_location}\n"
        else:
            req_text += f"✅ Локация: {req_location}\n"

    text += req_text

    # Статус босса
    if current_chapter.boss_name:
        if progress.is_boss_defeated(current_chapter.boss_name):
            text += f"\n✅ Босс побеждён: {current_chapter.boss_name}\n"
        else:
            text += f"\n⚔️ Цель: Победить {current_chapter.boss_name}\n"

            if requirements_met:
                text += "💡 Нажмите '⚔️ В бой!' для сражения с боссом!\n"

    # Награды
    text += f"\n🎁 Награда за главу:\n"
    text += f"   💰 {current_chapter.reward_gold} золота\n"
    text += f"   📊 {current_chapter.reward_exp} опыта\n"
    if current_chapter.reward_item:
        text += f"   🎁 {current_chapter.reward_item}\n"

    return text


def format_daily_quest(player: Player) -> str:
    """Отформатировать ежедневный квест."""
    update_daily_quest(player)

    quest = player.quests["daily"]
    target = quest.target
    kills = quest.kills
    claimed = quest.reward_claimed

    text = "📋 ЕЖЕДНЕВНЫЙ КВЕСТ\n"
    text += "━━━━━━━━━━━━━━━━━━━━\n"
    text += "Охота на монстров\n\n"

    # Прогресс-бар
    progress_pct = min(kills / target, 1.0)
    filled = int(progress_pct * 10)
    empty = 10 - filled
    progress_bar = "█" * filled + "░" * empty

    text += f"🎯 Прогресс: [{progress_bar}] {kills}/{target}\n"

    if claimed:
        text += "\n✅ Награда получена!\n"
    elif kills >= target:
        text += "\n🎁 Выполнено! Заберите награду.\n"
    else:
        text += f"\n💪 Осталось: {target - kills} монстров\n"

    text += f"\n💰 Награда: {QuestConstants.DAILY_REWARD_GOLD} золота, {QuestConstants.DAILY_REWARD_EXP} опыта\n"

    return text


def format_quest_status(player: Player) -> str:
    """Отформатировать полный статус квестов."""
    text = format_story_quest(player)
    text += "\n"
    text += format_daily_quest(player)

    return text
