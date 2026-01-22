"""Обработчики боев."""
from aiogram import Router, F, types
from aiogram.types import FSInputFile
from services import get_player_service
from game_logic import (
    select_monster_for_location,
    simulate_battle,
    apply_battle_result,
    add_experience,
    increment_kills,
    check_and_award
)
from game_logic.battle import create_boss_monster
from game_logic.story import get_story_progress, get_current_chapter, complete_chapter
from utils import format_battle_result
from data import LOCATIONS

router = Router()

player_service = get_player_service()


@router.message(F.text == "⚔️ В бой!")
async def start_battle(message: types.Message) -> None:
    """Начать бой."""
    if not message.from_user:
        return
    player = player_service.get_or_create(message.from_user.id)

    # Проверка здоровья
    if player.hp <= 15:
        await message.answer("⚠️ Вы слишком слабы для боя! Отдохните.")
        return

    # Проверяем, есть ли активная сюжетная битва с боссом
    progress = get_story_progress(player)
    current_chapter = get_current_chapter(player)
    is_boss_fight = False
    monster = None

    if current_chapter and current_chapter.boss_name:
        if not progress.is_boss_defeated(current_chapter.boss_name):
            # Создаём босса для битвы
            monster = create_boss_monster(current_chapter.boss_name)
            if monster:
                is_boss_fight = True

    # Если не сюжетная битва, выбираем обычного монстра
    if not is_boss_fight:
        location = player.location
        monster = select_monster_for_location(location, player.level)
        if monster is None:
            loc_data = LOCATIONS.get(location)
            if loc_data and loc_data.is_peaceful:
                await message.answer(f"🏘️ В {loc_data.name} нет врагов! Отправляйтесь в приключение.")
            else:
                await message.answer("⚠️ В этой локации нет подходящих монстров для вашего уровня. Попробуйте другое место!")
            return

    # Симуляция боя
    result = simulate_battle(player, monster)

    # Применение результата
    apply_battle_result(player, result)

    # Пост-обработка победы
    msg = format_battle_result(result, player)

    if result.victory:
        # Если это была битва с боссом - завершаем главу
        if is_boss_fight and current_chapter:
            success, chapter_msg = complete_chapter(player, current_chapter.chapter_id)
            if success:
                msg += f"\n\n{chapter_msg}"

        # Обновление дневного квеста
        completed, quest_msg = increment_kills(player)
        if completed and quest_msg:
            msg += quest_msg

        # Проверка уровня
        leveled, level_msg = add_experience(player, 0)  # Опыт уже добавлен в apply_battle_result
        if leveled and level_msg:
            msg += f"\n\n{level_msg}"

        # Проверка достижений
        msg, _ = check_and_award(player, msg)

    # Сохранение
    player_service.save_player(player)

    if monster.image_path:
        photo = FSInputFile(monster.image_path)
        await message.answer_photo(photo, caption=msg)
    else:
        await message.answer(msg)
