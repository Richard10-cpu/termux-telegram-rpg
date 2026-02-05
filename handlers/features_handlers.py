"""Обработчики для новых фич: достижения, питомцы, мини-игры, крафт."""
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services import get_player_service
from data.achievements import get_player_achievements_summary, unlock_achievement, ACHIEVEMENTS
from data.pets import PETS, get_pet_description
from data.minigames import (
    play_slots, play_dice, play_roulette, play_coinflip,
    go_fishing, get_available_arena_opponents, FISH_TYPES
)
from data.crafting import get_recipes_by_type, can_craft, craft_item, CRAFTING_RECIPES
from data.random_events import get_random_event, apply_event_choice
import random

router = Router()
player_service = get_player_service()


# ============= ДОСТИЖЕНИЯ =============

@router.message(Command("achievements"))
async def cmd_achievements(message: types.Message) -> None:
    """Показать достижения игрока."""
    if not message.from_user:
        return

    player = player_service.get_or_create(message.from_user.id)
    summary = get_player_achievements_summary(player)

    await message.answer(summary)


# ============= ПИТОМЦЫ =============

@router.message(Command("pets"))
async def cmd_pets(message: types.Message) -> None:
    """Показать доступных питомцев."""
    if not message.from_user:
        return

    player = player_service.get_or_create(message.from_user.id)

    if not hasattr(player, 'pets'):
        player.pets = []

    text = "🐾 ПИТОМЦЫ\n\n"

    for pet_id, pet in PETS.items():
        owned = pet_id in player.pets
        text += get_pet_description(pet, owned) + "\n\n"

    if player.pets:
        text += f"\n✅ У вас {len(player.pets)} питомцев!"
    else:
        text += "\n🔍 Найдите питомцев в своих приключениях!"

    await message.answer(text)


# ============= КАЗИНО =============

class CasinoStates(StatesGroup):
    """Состояния для казино."""
    waiting_for_bet = State()
    waiting_for_choice = State()


@router.message(Command("casino"))
async def cmd_casino(message: types.Message) -> None:
    """Главное меню казино."""
    text = (
        "🎰 ДОБРО ПОЖАЛОВАТЬ В КАЗИНО! 🎰\n\n"
        "Выберите игру:\n\n"
        "🎰 /slots <ставка> - Игровые автоматы\n"
        "🎲 /dice <ставка> <число> - Кости (1-6)\n"
        "🪙 /coinflip <ставка> <heads/tails> - Монетка\n"
        "🎣 /fishing - Рыбалка (100 золота)\n\n"
        "💰 Удачи!"
    )
    await message.answer(text)


@router.message(Command("slots"))
async def cmd_slots(message: types.Message) -> None:
    """Игровые автоматы."""
    if not message.from_user or not message.text:
        return

    player = player_service.get_or_create(message.from_user.id)

    args = message.text.split()
    if len(args) < 2:
        await message.answer("❌ Укажите ставку!\nПример: /slots 100")
        return

    try:
        bet = int(args[1])
    except ValueError:
        await message.answer("❌ Ставка должна быть числом!")
        return

    if bet < 10:
        await message.answer("❌ Минимальная ставка: 10 золота")
        return

    if player.gold < bet:
        await message.answer(f"❌ Недостаточно золота! У вас: {player.gold}💰")
        return

    result_msg, winnings = play_slots(bet)
    player.gold += winnings
    player_service.save(player)

    result_msg += f"\n\n💰 Баланс: {player.gold} золота"
    await message.answer(result_msg)


@router.message(Command("dice"))
async def cmd_dice(message: types.Message) -> None:
    """Игра в кости."""
    if not message.from_user or not message.text:
        return

    player = player_service.get_or_create(message.from_user.id)

    args = message.text.split()
    if len(args) < 3:
        await message.answer("❌ Укажите ставку и число (1-6)!\nПример: /dice 100 3")
        return

    try:
        bet = int(args[1])
        guess = int(args[2])
    except ValueError:
        await message.answer("❌ Неверный формат!")
        return

    if player.gold < bet:
        await message.answer(f"❌ Недостаточно золота! У вас: {player.gold}💰")
        return

    result_msg, winnings = play_dice(bet, guess)
    player.gold += winnings
    player_service.save(player)

    result_msg += f"\n\n💰 Баланс: {player.gold} золота"
    await message.answer(result_msg)


@router.message(Command("coinflip"))
async def cmd_coinflip(message: types.Message) -> None:
    """Подбрасывание монеты."""
    if not message.from_user or not message.text:
        return

    player = player_service.get_or_create(message.from_user.id)

    args = message.text.split()
    if len(args) < 3:
        await message.answer("❌ Укажите ставку и выбор!\nПример: /coinflip 100 heads")
        return

    try:
        bet = int(args[1])
        choice = args[2].lower()
    except (ValueError, IndexError):
        await message.answer("❌ Неверный формат!")
        return

    if choice not in ['heads', 'tails']:
        await message.answer("❌ Выберите heads или tails!")
        return

    if player.gold < bet:
        await message.answer(f"❌ Недостаточно золота! У вас: {player.gold}💰")
        return

    result_msg, winnings = play_coinflip(bet, choice)
    player.gold += winnings
    player_service.save(player)

    result_msg += f"\n\n💰 Баланс: {player.gold} золота"
    await message.answer(result_msg)


# ============= РЫБАЛКА =============

@router.message(Command("fishing"))
async def cmd_fishing(message: types.Message) -> None:
    """Порыбачить."""
    if not message.from_user:
        return

    player = player_service.get_or_create(message.from_user.id)

    cost = 100
    if player.gold < cost:
        await message.answer(f"❌ Рыбалка стоит {cost}💰\nУ вас: {player.gold}💰")
        return

    player.gold -= cost

    result_msg, value, special_item = go_fishing()
    player.gold += value

    if special_item:
        player.inventory.append(special_item)

    player_service.save(player)

    result_msg += f"\n\n💰 Новый баланс: {player.gold} золота"
    await message.answer(result_msg)


# ============= АРЕНА =============

@router.message(Command("arena"))
async def cmd_arena(message: types.Message) -> None:
    """Показать доступных противников на арене."""
    if not message.from_user:
        return

    player = player_service.get_or_create(message.from_user.id)

    opponents = get_available_arena_opponents(player.level)

    text = "⚔️ АРЕНА ГЛАДИАТОРОВ ⚔️\n\n"
    text += "Сразитесь с могучими воинами!\n\n"

    for tier, opp in opponents:
        text += f"{opp.emoji} {opp.name}\n"
        text += f"   Уровень: {opp.level}\n"
        text += f"   HP: {opp.hp} | Сила: {opp.power}\n"
        text += f"   Награда: {opp.reward_gold}💰 + {opp.reward_exp}📊\n\n"

    text += "💡 Используйте /fight для битвы с монстром\n"
    text += "Арена скоро будет доступна!"

    await message.answer(text)


# ============= КРАФТ =============

@router.message(Command("craft"))
async def cmd_craft(message: types.Message) -> None:
    """Показать рецепты крафта."""
    if not message.from_user or not message.text:
        return

    player = player_service.get_or_create(message.from_user.id)

    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        text = (
            "🔨 КРАФТ И АЛХИМИЯ\n\n"
            "Доступные категории:\n\n"
            "🔨 /craft blacksmith - Кузнечное дело\n"
            "⚗️ /craft alchemy - Алхимия\n"
            "✨ /craft enchanting - Зачарование\n\n"
            f"📊 Ваш уровень: {player.level}"
        )
        await message.answer(text)
        return

    craft_type = args[1].lower()

    if craft_type not in ['blacksmith', 'alchemy', 'enchanting']:
        await message.answer("❌ Неверная категория! Выберите: blacksmith, alchemy, enchanting")
        return

    recipes = get_recipes_by_type(craft_type, player.level)

    type_names = {
        'blacksmith': '🔨 Кузнечное дело',
        'alchemy': '⚗️ Алхимия',
        'enchanting': '✨ Зачарование'
    }

    text = f"{type_names[craft_type]}\n\n"
    text += "Доступные рецепты:\n\n"

    for recipe in recipes:
        text += f"📜 {recipe.result_item} x{recipe.result_amount}\n"
        text += f"   {recipe.description}\n"
        text += f"   Ингредиенты:\n"
        for ing, amount in recipe.ingredients.items():
            text += f"      • {ing} x{amount}\n"
        text += f"   ID: {recipe.recipe_id}\n\n"

    text += "\n💡 Используйте /make <recipe_id> для крафта"

    await message.answer(text)


@router.message(Command("make"))
async def cmd_make(message: types.Message) -> None:
    """Скрафтить предмет."""
    if not message.from_user or not message.text:
        return

    player = player_service.get_or_create(message.from_user.id)

    args = message.text.split()
    if len(args) < 2:
        await message.answer("❌ Укажите ID рецепта!\nПример: /make iron_sword")
        return

    recipe_id = args[1]
    recipe = CRAFTING_RECIPES.get(recipe_id)

    if not recipe:
        await message.answer("❌ Рецепт не найден!")
        return

    if recipe.required_level > player.level:
        await message.answer(f"❌ Требуется {recipe.required_level} уровень!")
        return

    success, msg = craft_item(player.inventory, recipe)

    if success:
        player_service.save(player)

    await message.answer(msg)


# ============= СЛУЧАЙНЫЕ СОБЫТИЯ =============

async def trigger_random_event(player, message: types.Message) -> bool:
    """Триггерить случайное событие (вызывается после действий)."""
    event = get_random_event(player.level, player.location)

    if not event:
        return False

    # Проверка на уникальность
    if not hasattr(player, 'seen_events'):
        player.seen_events = []

    text = f"🌟 {event.title}\n\n{event.description}\n\n"

    if event.choices:
        text += "Выберите действие:\n"
        for i, (choice_text, effect) in enumerate(event.choices, 1):
            text += f"{i}. {choice_text}\n"
        text += "\n💡 Ответьте числом выбора"
        # TODO: Добавить FSM для обработки выбора
    else:
        # Применить автоматический эффект
        if event.choices:
            effect = event.choices[0][1]
            result = apply_event_choice(effect, player)
            text += "\n" + result
            player_service.save(player)

    await message.answer(text)
    return True


# Экспортируем функцию для использования в других handlers
__all__ = ['router', 'trigger_random_event']
