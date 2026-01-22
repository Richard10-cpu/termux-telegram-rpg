"""Обработчики боев."""
from aiogram import Router, F, types
from services import get_player_service
from game_logic import (
    select_monster_for_location,
    simulate_battle,
    apply_battle_result,
    add_experience,
    increment_kills,
    check_and_award
)
from utils import format_battle_result
from data import LOCATIONS

router = Router()

player_service = get_player_service()


@router.message(F.text == "⚔️ В бой!")
async def start_battle(message: types.Message) -> None:
    """Начать бой."""
    player = player_service.get_or_create(message.from_user.id)

    # Проверка здоровья
    if player.hp <= 15:
        await message.answer("⚠️ Вы слишком слабы для боя! Отдохните.")
        return

    # Проверка локации
    location = player.location

    # Выбор монстра
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
        # Обновление дневного квеста
        completed, quest_msg = increment_kills(player)
        if completed:
            msg += quest_msg

        # Проверка уровня
        leveled, level_msg = add_experience(player, 0)  # Опыт уже добавлен в apply_battle_result
        if leveled and level_msg:
            msg += f"\n\n{level_msg}"

        # Проверка достижений
        msg, _ = check_and_award(player, msg)

    # Сохранение
    player_service.save_player(player)

    await message.answer(msg)
