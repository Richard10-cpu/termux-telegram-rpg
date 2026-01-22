"""Обработчики отдыха и рейтинга."""
from aiogram import Router, F, types
from services import get_player_service
from utils import format_top_players

router = Router()

player_service = get_player_service()


@router.message(F.text == "☕ Отдых (15💰)")
async def rest_and_heal(message: types.Message) -> None:
    """Отдохнуть и восстановить здоровье и ману."""
    if not message.from_user:
        return
    player = player_service.get_or_create(message.from_user.id)
    if player.gold >= 15:
        player.gold -= 15
        player.hp = player.max_hp
        player.mana = player.max_mana
        player_service.save_player(player)
        await message.answer("☕ Вы отлично отдохнули! Здоровье и мана полностью восстановлены!")
    else:
        await message.answer("❌ Не хватает золота!")


@router.message(F.text == "🏆 Рейтинг")
async def show_rating_inline(message: types.Message) -> None:
    """Показать рейтинг (из главного меню)."""
    top_players = player_service.get_top_players(10)
    if not top_players:
        await message.answer("📊 Пока нет игроков в рейтинге.")
        return
    text = format_top_players(top_players)
    await message.answer(text)
