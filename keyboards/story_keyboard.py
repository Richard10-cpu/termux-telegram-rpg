"""Клавиатуры для системы сюжета."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import Player
from models.story import StoryProgress
from data.story_chapters import get_all_chapters


def story_main_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура сюжета."""
    keyboard = [
        [InlineKeyboardButton(text="📖 Текущая глава", callback_data="story_current")],
        [InlineKeyboardButton(text="📚 Все главы", callback_data="story_chapters")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="story_overview")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_chapters_keyboard(player: Player) -> InlineKeyboardMarkup:
    """Клавиатура со списком глав."""
    from game_logic.story import get_story_progress

    progress = get_story_progress(player)
    all_chapters = get_all_chapters()

    keyboard = []

    for chapter in all_chapters:
        # Определяем статус
        if progress.is_chapter_completed(chapter.chapter_id):
            status = "✅"
        elif progress.current_chapter == chapter.chapter_id:
            status = "▶️"
        elif chapter.is_unlocked(player.level):
            status = "🔓"
        else:
            status = "🔒"

        button_text = f"{status} Глава {chapter.chapter_id}: {chapter.title[:20]}..."
        callback_data = f"chapter_{chapter.chapter_id}"

        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])

    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="story_overview")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_chapter_detail_keyboard(chapter_id: int, player: Player) -> InlineKeyboardMarkup:
    """Клавиатура деталей главы."""
    from game_logic.story import get_story_progress, check_chapter_requirements
    from data.story_chapters import get_chapter

    progress = get_story_progress(player)
    chapter = get_chapter(chapter_id)

    keyboard = []

    # Кнопка начала битвы с боссом (если глава активна и не завершена)
    if chapter and not progress.is_chapter_completed(chapter_id):
        if progress.current_chapter == chapter_id:
            can_start, _ = check_chapter_requirements(player, chapter)
            if can_start and chapter.boss_name and not progress.is_boss_defeated(chapter.boss_name):
                keyboard.append([
                    InlineKeyboardButton(
                        text=f"⚔️ Сразиться с {chapter.boss_name}",
                        callback_data=f"start_boss_{chapter_id}"
                    )
                ])

    keyboard.append([InlineKeyboardButton(text="🔙 К главам", callback_data="story_chapters")])
    keyboard.append([InlineKeyboardButton(text="🏠 К обзору", callback_data="story_overview")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Экспортируем главную клавиатуру как константу
story_main_keyboard = story_main_keyboard()
