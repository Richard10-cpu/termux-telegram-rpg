"""Обработчики сюжета."""
from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from services import get_player_service
from game_logic.story import (
    format_story_overview,
    format_chapter_info,
    get_current_chapter,
    start_chapter_boss_fight,
    complete_chapter,
    check_chapter_requirements
)
from data.story_chapters import get_chapter, get_all_chapters
from keyboards.story_keyboard import story_main_keyboard, get_chapters_keyboard, get_chapter_detail_keyboard

router = Router()

player_service = get_player_service()


@router.message(F.text == "📖 Сюжет")
async def show_story(message: types.Message) -> None:
    """Показать обзор сюжета."""
    if not message.from_user:
        return
    player = player_service.get_or_create(message.from_user.id)

    text = format_story_overview(player)
    await message.answer(text, reply_markup=story_main_keyboard)


@router.callback_query(F.data == "story_overview")
async def callback_story_overview(callback: CallbackQuery) -> None:
    """Показать обзор сюжета (callback)."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)
    text = format_story_overview(player)

    await callback.message.edit_text(text, reply_markup=story_main_keyboard)
    await callback.answer()


@router.callback_query(F.data == "story_chapters")
async def callback_story_chapters(callback: CallbackQuery) -> None:
    """Показать список глав."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)
    keyboard = get_chapters_keyboard(player)

    text = "📚 Выберите главу для просмотра:"

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("chapter_"))
async def callback_chapter_detail(callback: CallbackQuery) -> None:
    """Показать детали главы."""
    if not callback.from_user or not callback.message or not callback.data:
        return

    player = player_service.get_or_create(callback.from_user.id)

    # Получаем ID главы из callback data
    chapter_id = int(callback.data.split("_")[1])
    chapter = get_chapter(chapter_id)

    if not chapter:
        await callback.answer("❌ Глава не найдена!")
        return

    text = format_chapter_info(chapter, player)
    keyboard = get_chapter_detail_keyboard(chapter_id, player)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("start_boss_"))
async def callback_start_boss(callback: CallbackQuery) -> None:
    """Начать битву с боссом главы."""
    if not callback.from_user or not callback.message or not callback.data:
        return

    player = player_service.get_or_create(callback.from_user.id)

    # Получаем ID главы
    chapter_id = int(callback.data.split("_")[2])
    chapter = get_chapter(chapter_id)

    if not chapter:
        await callback.answer("❌ Глава не найдена!")
        return

    # Проверка здоровья
    if player.hp <= 20:
        await callback.answer("⚠️ Вы слишком слабы для боя с боссом! Отдохните.", show_alert=True)
        return

    # Пытаемся начать битву
    success, msg = start_chapter_boss_fight(player, chapter_id)

    if not success:
        await callback.answer(msg, show_alert=True)
        return

    # Битва начинается - сохраняем информацию о том, что игрок в сюжетной битве
    player_service.save_player(player)

    # Информируем игрока
    await callback.message.answer(
        f"{msg}\n\n"
        f"⚠️ Это особая сюжетная битва!\n"
        f"Используйте команду '⚔️ В бой!' для сражения с {chapter.boss_name}."
    )
    await callback.answer()


@router.callback_query(F.data == "story_current")
async def callback_current_chapter(callback: CallbackQuery) -> None:
    """Показать текущую главу."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)
    chapter = get_current_chapter(player)

    if not chapter:
        await callback.answer("❌ Нет доступных глав!", show_alert=True)
        return

    text = format_chapter_info(chapter, player)
    keyboard = get_chapter_detail_keyboard(chapter.chapter_id, player)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
