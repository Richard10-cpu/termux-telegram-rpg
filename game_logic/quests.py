"""Система квестов."""
from datetime import datetime
from models import Player


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


def format_quest_status(player: Player) -> str:
    """Отформатировать статус квеста."""
    update_daily_quest(player)

    quest = player.quests["daily"]
    target = quest.target
    kills = quest.kills
    claimed = quest.reward_claimed

    status = "✅ Выполнен" if kills >= target else f"🔄 В прогрессе: {kills}/{target}"

    text = "📜 Ежедневный квест\n"
    text += f"🎯 Убить монстров: {status}\n"
    text += f"💰 Награда: {QuestConstants.DAILY_REWARD_GOLD} золота\n\n"

    if claimed:
        text += "✅ Награда получена!"
    elif kills >= target:
        text += "🎁 Квест выполнен! Заберите награду."
    else:
        text += f"💪 Осталось убить: {target - kills}"

    return text
