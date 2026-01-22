"""Обработчики боев с пошаговой системой."""
import random
from aiogram import Router, F, types
from aiogram.types import FSInputFile, CallbackQuery
from services import get_player_service
from game_logic import (
    select_monster_for_location,
    create_battle_state,
    player_attack,
    monster_attack,
    flee_battle,
    add_experience,
    increment_kills,
    check_and_award,
    cast_spell,
    use_potion
)
from game_logic.battle import create_boss_monster
from game_logic.story import get_story_progress, get_current_chapter, complete_chapter
from data import LOCATIONS
from keyboards.battle_keyboard import get_battle_keyboard, get_spells_battle_keyboard, get_potions_battle_keyboard

router = Router()

player_service = get_player_service()


def format_battle_status(player, state) -> str:
    """Форматировать текущее состояние боя."""
    monster_hp_bar = "█" * max(1, int(state.monster_hp / state.monster_max_hp * 10))
    monster_hp_percent = int(state.monster_hp / state.monster_max_hp * 100)

    player_hp_bar = "█" * max(1, int(player.hp / player.max_hp * 10))
    player_hp_percent = int(player.hp / player.max_hp * 100)

    boss_icon = "👑 " if state.is_boss else ""
    elite_icon = "⭐ " if state.is_elite else ""

    text = f"⚔️ БОЙ - Ход {state.turn}\n\n"
    text += f"{boss_icon}{elite_icon}{state.monster_name}\n"
    text += f"💚 HP: {state.monster_hp}/{state.monster_max_hp} ({monster_hp_percent}%)\n"
    text += f"{monster_hp_bar}\n\n"
    text += f"👤 Вы\n"
    text += f"❤️ HP: {player.hp}/{player.max_hp} ({player_hp_percent}%)\n"
    text += f"{player_hp_bar}\n"
    text += f"💙 Мана: {player.mana}/{player.max_mana}\n\n"
    text += "Выберите действие:"

    return text


@router.message(F.text == "⚔️ В бой!")
async def start_battle(message: types.Message) -> None:
    """Начать пошаговый бой."""
    if not message.from_user:
        return
    player = player_service.get_or_create(message.from_user.id)

    # Проверка здоровья
    if player.hp <= 15:
        await message.answer("⚠️ Вы слишком слабы для боя! Отдохните.")
        return

    # Проверка, нет ли уже активного боя
    if player.battle_state:
        await message.answer("⚠️ У вас уже есть активный бой! Завершите его сначала.")
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

    # Создаём состояние боя
    player.battle_state = create_battle_state(monster, is_boss=is_boss_fight)
    player_service.save_player(player)

    # Проверяем наличие зелий
    has_potions = any(count > 0 for count in player.potions.values())

    # Показываем статус боя
    text = format_battle_status(player, player.battle_state)

    if monster.image_path:
        photo = FSInputFile(monster.image_path)
        await message.answer_photo(
            photo,
            caption=text,
            reply_markup=get_battle_keyboard(player, has_potions)
        )
    else:
        await message.answer(
            text,
            reply_markup=get_battle_keyboard(player, has_potions)
        )


@router.callback_query(F.data == "battle_attack")
async def callback_battle_attack(callback: CallbackQuery) -> None:
    """Атака игрока."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)

    if not player.battle_state:
        await callback.answer("❌ У вас нет активного боя!")
        return

    state = player.battle_state

    # Атака игрока
    damage, is_crit = player_attack(player, state)
    state.monster_hp -= damage

    log = f"⚔️ Вы атакуете! "
    if is_crit:
        log += f"💥 КРИТИЧЕСКИЙ УДАР! {damage} урона!\n"
    else:
        log += f"{damage} урона.\n"

    # Проверяем, жив ли монстр
    if state.monster_hp <= 0:
        await handle_victory(callback, player, state, log)
        return

    # Ход монстра
    enemy_damage, is_dodge = monster_attack(player, state)
    player.hp -= enemy_damage

    if is_dodge:
        log += f"💨 Вы уклонились от атаки {state.monster_name}!"
    elif state.defending:
        log += f"🛡️ {state.monster_name} атакует! Благодаря защите урон снижен до {enemy_damage}."
    else:
        log += f"🗡️ {state.monster_name} атакует! {enemy_damage} урона."

    # Сбрасываем защиту
    state.defending = False
    state.turn += 1

    # Проверяем, жив ли игрок
    if player.hp <= 0:
        await handle_defeat(callback, player, state, log)
        return

    player_service.save_player(player)

    # Обновляем статус боя
    text = log + "\n\n" + format_battle_status(player, state)
    has_potions = any(count > 0 for count in player.potions.values())

    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_battle_keyboard(player, has_potions)
    )
    await callback.answer()


@router.callback_query(F.data == "battle_defend")
async def callback_battle_defend(callback: CallbackQuery) -> None:
    """Защита игрока."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)

    if not player.battle_state:
        await callback.answer("❌ У вас нет активного боя!")
        return

    state = player.battle_state

    # Игрок защищается
    state.defending = True
    log = "🛡️ Вы приняли защитную стойку!\n"

    # Ход монстра
    enemy_damage, is_dodge = monster_attack(player, state)
    player.hp -= enemy_damage

    if is_dodge:
        log += f"💨 Вы уклонились от атаки {state.monster_name}!"
    else:
        log += f"🗡️ {state.monster_name} атакует! Урон снижен до {enemy_damage}."

    state.defending = False
    state.turn += 1

    # Проверяем, жив ли игрок
    if player.hp <= 0:
        await handle_defeat(callback, player, state, log)
        return

    player_service.save_player(player)

    # Обновляем статус боя
    text = log + "\n\n" + format_battle_status(player, state)
    has_potions = any(count > 0 for count in player.potions.values())

    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_battle_keyboard(player, has_potions)
    )
    await callback.answer()


@router.callback_query(F.data == "battle_spells")
async def callback_battle_spells(callback: CallbackQuery) -> None:
    """Показать список заклинаний."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)

    if not player.battle_state:
        await callback.answer("❌ У вас нет активного боя!")
        return

    await callback.message.edit_reply_markup(reply_markup=get_spells_battle_keyboard(player))
    await callback.answer("Выберите заклинание:")


@router.callback_query(F.data.startswith("cast_"))
async def callback_cast_spell(callback: CallbackQuery) -> None:
    """Применить заклинание."""
    if not callback.from_user or not callback.message or not callback.data:
        return

    player = player_service.get_or_create(callback.from_user.id)

    if not player.battle_state:
        await callback.answer("❌ У вас нет активного боя!")
        return

    state = player.battle_state
    spell_key = callback.data.replace("cast_", "")

    # Применяем заклинание
    success, spell_msg, damage = cast_spell(player, spell_key, state)

    if not success:
        await callback.answer(spell_msg, show_alert=True)
        return

    log = spell_msg + "\n"

    # Проверяем, жив ли монстр после заклинания
    if state.monster_hp <= 0:
        await handle_victory(callback, player, state, log)
        return

    # Ход монстра
    enemy_damage, is_dodge = monster_attack(player, state)
    player.hp -= enemy_damage

    if is_dodge:
        log += f"💨 Вы уклонились от атаки {state.monster_name}!"
    else:
        log += f"🗡️ {state.monster_name} атакует! {enemy_damage} урона."

    state.turn += 1

    # Проверяем, жив ли игрок
    if player.hp <= 0:
        await handle_defeat(callback, player, state, log)
        return

    player_service.save_player(player)

    # Обновляем статус боя
    text = log + "\n\n" + format_battle_status(player, state)
    has_potions = any(count > 0 for count in player.potions.values())

    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_battle_keyboard(player, has_potions)
    )
    await callback.answer()


@router.callback_query(F.data == "battle_potions")
async def callback_battle_potions(callback: CallbackQuery) -> None:
    """Показать список зелий."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)

    if not player.battle_state:
        await callback.answer("❌ У вас нет активного боя!")
        return

    await callback.message.edit_reply_markup(reply_markup=get_potions_battle_keyboard(player))
    await callback.answer("Выберите зелье:")


@router.callback_query(F.data.startswith("use_"))
async def callback_use_potion(callback: CallbackQuery) -> None:
    """Использовать зелье."""
    if not callback.from_user or not callback.message or not callback.data:
        return

    player = player_service.get_or_create(callback.from_user.id)

    if not player.battle_state:
        await callback.answer("❌ У вас нет активного боя!")
        return

    state = player.battle_state
    potion_key = callback.data.replace("use_", "")

    # Используем зелье
    success, potion_msg = use_potion(player, potion_key, state)

    if not success:
        await callback.answer(potion_msg, show_alert=True)
        return

    log = potion_msg + "\n"

    # Ход монстра (использование зелья - это действие)
    enemy_damage, is_dodge = monster_attack(player, state)
    player.hp -= enemy_damage

    if is_dodge:
        log += f"💨 Вы уклонились от атаки {state.monster_name}!"
    else:
        log += f"🗡️ {state.monster_name} атакует! {enemy_damage} урона."

    state.turn += 1

    # Проверяем, жив ли игрок
    if player.hp <= 0:
        await handle_defeat(callback, player, state, log)
        return

    player_service.save_player(player)

    # Обновляем статус боя
    text = log + "\n\n" + format_battle_status(player, state)
    has_potions = any(count > 0 for count in player.potions.values())

    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_battle_keyboard(player, has_potions)
    )
    await callback.answer()


@router.callback_query(F.data == "battle_back")
async def callback_battle_back(callback: CallbackQuery) -> None:
    """Вернуться к действиям боя."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)

    if not player.battle_state:
        await callback.answer("❌ У вас нет активного боя!")
        return

    has_potions = any(count > 0 for count in player.potions.values())
    await callback.message.edit_reply_markup(reply_markup=get_battle_keyboard(player, has_potions))
    await callback.answer()


@router.callback_query(F.data == "battle_flee")
async def callback_battle_flee(callback: CallbackQuery) -> None:
    """Попытка сбежать."""
    if not callback.from_user or not callback.message:
        return

    player = player_service.get_or_create(callback.from_user.id)

    if not player.battle_state:
        await callback.answer("❌ У вас нет активного боя!")
        return

    state = player.battle_state

    # Нельзя сбежать от босса
    if state.is_boss:
        await callback.answer("❌ Вы не можете сбежать от босса!", show_alert=True)
        return

    # Попытка побега
    if flee_battle(player):
        player.battle_state = None
        player_service.save_player(player)

        await callback.message.edit_caption(
            caption=f"🏃 Вам удалось сбежать от {state.monster_name}!",
            reply_markup=None
        )
        await callback.answer()
    else:
        # Неудачная попытка - монстр атакует
        enemy_damage, is_dodge = monster_attack(player, state)
        player.hp -= enemy_damage

        log = "🏃 Попытка побега провалилась!\n"
        if is_dodge:
            log += f"💨 Но вы уклонились от атаки {state.monster_name}!"
        else:
            log += f"🗡️ {state.monster_name} атакует! {enemy_damage} урона."

        state.turn += 1

        # Проверяем, жив ли игрок
        if player.hp <= 0:
            await handle_defeat(callback, player, state, log)
            return

        player_service.save_player(player)

        text = log + "\n\n" + format_battle_status(player, state)
        has_potions = any(count > 0 for count in player.potions.values())

        await callback.message.edit_caption(
            caption=text,
            reply_markup=get_battle_keyboard(player, has_potions)
        )
        await callback.answer()


async def handle_victory(callback: CallbackQuery, player, state, log: str) -> None:
    """Обработка победы в бою."""
    # Награды
    gold_earned = random.randint(state.monster_gold_min, state.monster_gold_max)
    exp_earned = state.monster_exp

    # Бонус для элитных монстров
    if state.is_elite:
        gold_earned *= 2
        exp_earned *= 2

    player.gold += gold_earned
    player.exp += exp_earned
    player.total_kills += 1

    # Завершаем бой
    player.battle_state = None

    msg = log + f"\n🎉 Вы победили {state.monster_name}!\n"
    msg += f"💰 Найдено золота: {gold_earned}\n"
    msg += f"📊 Получено опыта: {exp_earned}\n"

    # Проверяем сюжетный босс
    if state.is_boss:
        progress = get_story_progress(player)
        current_chapter = get_current_chapter(player)
        if current_chapter:
            success, chapter_msg = complete_chapter(player, current_chapter.chapter_id)
            if success:
                msg += f"\n\n{chapter_msg}"

    # Обновление дневного квеста
    completed, quest_msg = increment_kills(player)
    if completed and quest_msg:
        msg += quest_msg

    # Проверка уровня
    leveled, level_msg = add_experience(player, 0)
    if leveled and level_msg:
        msg += f"\n\n{level_msg}"

    # Проверка достижений
    msg, _ = check_and_award(player, msg)

    player_service.save_player(player)

    await callback.message.edit_caption(caption=msg, reply_markup=None)
    await callback.answer("Победа!")


async def handle_defeat(callback: CallbackQuery, player, state, log: str) -> None:
    """Обработка поражения в бою."""
    gold_lost = min(player.gold // 2, 20)
    player.gold -= gold_lost
    player.hp = 1

    # Завершаем бой
    player.battle_state = None
    player_service.save_player(player)

    msg = log + f"\n💀 Вы проиграли...\n"
    msg += f"💸 Потеряно золота: {gold_lost}\n"
    msg += "💡 Отдохните и попробуйте снова!"

    await callback.message.edit_caption(caption=msg, reply_markup=None)
    await callback.answer("Поражение...")
