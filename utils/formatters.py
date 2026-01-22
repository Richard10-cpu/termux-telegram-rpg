"""Утилиты форматирования сообщений."""
from models import Player
from game_logic import format_achievements
from game_logic.story import get_story_progress, get_current_chapter


def format_profile(player: Player) -> str:
    """Отформатировать профиль игрока."""
    inv = ", ".join(player.inventory) if player.inventory else "Пусто"

    # Экипировка
    weapon = player.equipment.weapon or "Нет"
    armor = player.equipment.armor or "Нет"

    # Достижения
    achievements_text = format_achievements(player.achievements)

    # Сюжет
    progress = get_story_progress(player)
    current_chapter = get_current_chapter(player)
    story_text = ""

    if current_chapter:
        boss_status = ""
        if current_chapter.boss_name:
            if progress.is_boss_defeated(current_chapter.boss_name):
                boss_status = " ✅"
            else:
                boss_status = " ⚔️"

        story_text = f"\n\n📖 Сюжет: Глава {current_chapter.chapter_id}{boss_status}\n{current_chapter.title}"

    text = (
        f"👤 Уровень: {player.level}\n"
        f"❤️ HP: {player.hp}/{player.max_hp}\n"
        f"⚔️ Сила: {player.power}\n"
        f"💰 Золото: {player.gold}\n"
        f"🗡️ Оружие: {weapon}\n"
        f"🛡️ Броня: {armor}\n"
        f"🎒 Инвентарь: {inv}"
        f"{achievements_text}"
        f"{story_text}"
    )

    return text


def format_battle_result(result, player: Player) -> str:
    """Отформатировать результат боя."""
    msg = result.message
    msg += f"\n💔 Ваше HP: {player.hp}/{player.max_hp}"
    return msg


def format_top_players(players: list[tuple[str, Player]]) -> str:
    """Отформатировать топ игроков."""
    text = "🏆 ТОП-10 ИГРОКОВ 🏆\n\n"

    for i, (uid, p) in enumerate(players, 1):
        medal = ""
        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"

        text += f"{medal} #{i}. Уровень {p.level} | 💰 {p.gold}\n"

    return text


def format_location_info(location_key: str) -> str:
    """Отформатировать информацию о локации."""
    from data import LOCATIONS, MONSTER_TEMPLATES

    loc = LOCATIONS.get(location_key)
    if not loc:
        return "❌ Локация не найдена"

    enemies_text = ""
    if loc.has_enemies:
        enemies = ", ".join([MONSTER_TEMPLATES[e].name for e in loc.enemies if e in MONSTER_TEMPLATES])
        enemies_text = f"\n👹 Враги: {enemies}"
    else:
        enemies_text = "\n✨ Мирная зона"

    text = f"📍 Вы находитесь: {loc.name}\n"
    text += f"{loc.description}{enemies_text}"

    return text
