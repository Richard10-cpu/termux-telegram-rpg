"""Логика сюжетной системы."""
from models import Player
from models.story import StoryProgress, StoryChapter
from data.story_chapters import get_chapter, get_all_chapters, get_available_chapters


def get_story_progress(player: Player) -> StoryProgress:
    """Получить прогресс сюжета игрока."""
    if not hasattr(player, 'story_progress') or player.story_progress is None:
        player.story_progress = StoryProgress()
    return player.story_progress


def get_current_chapter(player: Player) -> StoryChapter | None:
    """Получить текущую главу игрока."""
    progress = get_story_progress(player)
    return get_chapter(progress.current_chapter)


def check_chapter_requirements(player: Player, chapter: StoryChapter) -> tuple[bool, str]:
    """Проверить выполнение требований главы.

    Returns:
        (can_start: bool, message: str)
    """
    # Проверка уровня
    if not chapter.is_unlocked(player.level):
        return False, f"❌ Требуется {chapter.unlock_level} уровень! У вас {player.level}."

    # Проверка локации
    if chapter.location_requirement and player.location != chapter.location_requirement:
        location_names = {
            "village": "🏘️ Деревню",
            "forest": "🌲 Тёмный лес",
            "cave": "🕳️ Пещеру",
            "mountain": "⛰️ Гору",
            "abyss": "🌊 Морскую бездну",
            "ruins": "🏛️ Руины империи",
            "hell": "🔥 Преисподнюю",
            "void": "⚡ Пустоту"
        }
        required_location = location_names.get(chapter.location_requirement, chapter.location_requirement)
        return False, f"❌ Вы должны находиться в локации: {required_location}"

    return True, ""


def start_chapter_boss_fight(player: Player, chapter_id: int) -> tuple[bool, str]:
    """Начать битву с боссом главы.

    Returns:
        (success: bool, message: str)
    """
    progress = get_story_progress(player)
    chapter = get_chapter(chapter_id)

    if not chapter:
        return False, "❌ Глава не найдена!"

    # Проверка что это текущая глава
    if progress.current_chapter != chapter_id:
        return False, "❌ Эта глава недоступна!"

    # Проверка что глава не завершена
    if progress.is_chapter_completed(chapter_id):
        return False, "❌ Вы уже завершили эту главу!"

    # Проверка требований
    can_start, error_msg = check_chapter_requirements(player, chapter)
    if not can_start:
        return False, error_msg

    # Проверка что босс ещё не побеждён
    if chapter.boss_name and progress.is_boss_defeated(chapter.boss_name):
        return False, "❌ Вы уже победили этого босса!"

    return True, f"⚔️ Начинается битва с {chapter.boss_name}!"


def complete_chapter(player: Player, chapter_id: int) -> tuple[bool, str]:
    """Завершить главу и выдать награды.

    Returns:
        (success: bool, message: str)
    """
    progress = get_story_progress(player)
    chapter = get_chapter(chapter_id)

    if not chapter:
        return False, "❌ Глава не найдена!"

    # Проверка что глава не завершена
    if progress.is_chapter_completed(chapter_id):
        return False, "❌ Вы уже завершили эту главу!"

    # Отмечаем босса как побеждённого
    if chapter.boss_name:
        progress.defeat_boss(chapter.boss_name)

    # Завершаем главу
    progress.complete_chapter(chapter_id)

    # Выдаём награды
    rewards = []

    if chapter.reward_gold > 0:
        player.gold += chapter.reward_gold
        rewards.append(f"{chapter.reward_gold}💰")

    if chapter.reward_exp > 0:
        player.exp += chapter.reward_exp
        rewards.append(f"{chapter.reward_exp}📊 опыта")

    if chapter.reward_item:
        player.inventory.append(chapter.reward_item)
        rewards.append(f"'{chapter.reward_item}'")

    reward_text = ", ".join(rewards)

    # Проверка окончания игры
    if chapter_id == 8:
        msg = (
            f"🎉 ПОЗДРАВЛЯЕМ! Вы завершили главу '{chapter.title}'!\n\n"
            f"🏆 ВЫ ПРОШЛИ ВСЮ ИГРУ!\n"
            f"🎁 Награды: {reward_text}\n\n"
            f"✨ Вы стали легендой вселенной! Первозданный Хаос побеждён!\n"
            f"⚡ Реальность восстановлена, и ваше имя навечно вписано в историю!"
        )
    else:
        next_chapter = get_chapter(chapter_id + 1)
        next_info = ""
        if next_chapter:
            next_info = f"\n\n📖 Следующая глава: {next_chapter.title}\n🔓 Требуется уровень: {next_chapter.unlock_level}"

        msg = (
            f"🎉 Поздравляем! Вы завершили главу '{chapter.title}'!\n"
            f"🎁 Награды: {reward_text}"
            f"{next_info}"
        )

    return True, msg


def format_chapter_info(chapter: StoryChapter, player: Player) -> str:
    """Отформатировать информацию о главе."""
    progress = get_story_progress(player)

    # Статус главы
    if progress.is_chapter_completed(chapter.chapter_id):
        status = "✅ Завершена"
    elif progress.current_chapter == chapter.chapter_id:
        status = "🔄 Текущая"
    elif chapter.is_unlocked(player.level):
        status = "🔓 Доступна"
    else:
        status = f"🔒 Требуется {chapter.unlock_level} ур."

    text = f"📖 {chapter.title}\n"
    text += f"Статус: {status}\n"
    text += f"Уровень: {chapter.unlock_level}\n\n"
    text += f"{chapter.description}\n\n"

    if chapter.boss_name:
        boss_status = "✅ Побеждён" if progress.is_boss_defeated(chapter.boss_name) else "⚔️ Босс"
        text += f"{boss_status}: {chapter.boss_name}\n"

    text += f"💰 Награда: {chapter.reward_gold} золота\n"
    text += f"📊 Опыт: {chapter.reward_exp}\n"

    if chapter.reward_item:
        text += f"🎁 Предмет: {chapter.reward_item}\n"

    return text


def format_story_overview(player: Player) -> str:
    """Отформатировать обзор всего сюжета."""
    progress = get_story_progress(player)
    all_chapters = get_all_chapters()

    text = "📚 СЮЖЕТ ИГРЫ\n\n"

    completed = len(progress.completed_chapters)
    total = len(all_chapters)
    text += f"Прогресс: {completed}/{total} глав завершено\n\n"

    for chapter in all_chapters:
        if progress.is_chapter_completed(chapter.chapter_id):
            status = "✅"
        elif progress.current_chapter == chapter.chapter_id:
            status = "▶️"
        elif chapter.is_unlocked(player.level):
            status = "🔓"
        else:
            status = "🔒"

        text += f"{status} Глава {chapter.chapter_id}: {chapter.title}\n"

    text += f"\n💪 Ваш уровень: {player.level}"

    return text
