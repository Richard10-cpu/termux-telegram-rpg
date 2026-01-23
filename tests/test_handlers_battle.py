"""Тесты обработчиков боевой системы."""
import pytest
from unittest.mock import patch, AsyncMock, Mock
from handlers.battle_handlers import (
    start_battle,
    callback_battle_attack,
    callback_battle_defend,
    callback_battle_spells,
    callback_cast_spell,
    callback_battle_potions,
    callback_use_potion,
    callback_battle_flee,
    callback_battle_back,
    format_battle_status
)
from models import Monster, MonsterTemplate, BattleState


@pytest.mark.asyncio
async def test_start_battle_success(mock_message, test_player, test_monster):
    """Тест успешного начала боя."""
    test_player.location = "forest"
    test_player.hp = 100

    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.select_monster_for_location', return_value=test_monster), \
         patch('handlers.battle_handlers.get_story_progress'), \
         patch('handlers.battle_handlers.get_current_chapter', return_value=None):

        mock_service.get_or_create.return_value = test_player

        await start_battle(mock_message)

        # Проверяем, что бой создан
        assert test_player.battle_state is not None
        assert test_player.battle_state.monster_name == test_monster.name

        # Проверяем, что вызван answer_photo или answer
        assert mock_message.answer_photo.called or mock_message.answer.called
        mock_service.save_player.assert_called_once_with(test_player)


@pytest.mark.asyncio
async def test_start_battle_low_hp(mock_message, test_player):
    """Тест начала боя с низким HP."""
    test_player.hp = 10  # Меньше 15

    with patch('handlers.battle_handlers.player_service') as mock_service:
        mock_service.get_or_create.return_value = test_player

        await start_battle(mock_message)

        # Проверяем, что бой не начался
        assert test_player.battle_state is None

        # Проверяем сообщение об ошибке
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "слишком слабы" in call_args


@pytest.mark.asyncio
async def test_start_battle_already_active(mock_message, player_in_battle):
    """Тест начала боя при уже активном бое."""
    with patch('handlers.battle_handlers.player_service') as mock_service:
        mock_service.get_or_create.return_value = player_in_battle

        await start_battle(mock_message)

        # Проверяем сообщение об ошибке
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "активный бой" in call_args


@pytest.mark.asyncio
async def test_start_battle_peaceful_location(mock_message, test_player):
    """Тест начала боя в мирной локации."""
    test_player.location = "village"
    test_player.hp = 100

    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.select_monster_for_location', return_value=None), \
         patch('handlers.battle_handlers.get_story_progress'), \
         patch('handlers.battle_handlers.get_current_chapter', return_value=None), \
         patch('handlers.battle_handlers.LOCATIONS', {"village": Mock(name="Деревня", is_peaceful=True)}):

        mock_service.get_or_create.return_value = test_player

        await start_battle(mock_message)

        # Проверяем, что бой не начался
        assert test_player.battle_state is None
        mock_message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_callback_battle_attack_victory(mock_callback, player_in_battle):
    """Тест атаки с победой."""
    # Устанавливаем HP монстра на минимум
    player_in_battle.battle_state.monster_hp = 1

    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.player_attack', return_value=(10, False)), \
         patch('handlers.battle_handlers.handle_victory') as mock_victory:

        mock_service.get_or_create.return_value = player_in_battle

        await callback_battle_attack(mock_callback)

        # Проверяем, что вызвана обработка победы
        mock_victory.assert_called_once()


@pytest.mark.asyncio
async def test_callback_battle_attack_continue(mock_callback, player_in_battle):
    """Тест атаки с продолжением боя."""
    player_in_battle.battle_state.monster_hp = 50

    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.player_attack', return_value=(10, False)), \
         patch('handlers.battle_handlers.monster_attack', return_value=(5, False)):

        mock_service.get_or_create.return_value = player_in_battle

        await callback_battle_attack(mock_callback)

        # Проверяем, что бой продолжается
        assert player_in_battle.battle_state is not None
        mock_callback.message.edit_caption.assert_called_once()
        mock_callback.answer.assert_called_once()


@pytest.mark.asyncio
async def test_callback_battle_attack_defeat(mock_callback, player_in_battle):
    """Тест атаки с поражением игрока."""
    player_in_battle.hp = 5
    player_in_battle.battle_state.monster_hp = 50

    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.player_attack', return_value=(10, False)), \
         patch('handlers.battle_handlers.monster_attack', return_value=(10, False)), \
         patch('handlers.battle_handlers.handle_defeat') as mock_defeat:

        mock_service.get_or_create.return_value = player_in_battle

        await callback_battle_attack(mock_callback)

        # Проверяем, что вызвана обработка поражения
        mock_defeat.assert_called_once()


@pytest.mark.asyncio
async def test_callback_battle_attack_no_battle(mock_callback, test_player):
    """Тест атаки без активного боя."""
    with patch('handlers.battle_handlers.player_service') as mock_service:
        mock_service.get_or_create.return_value = test_player

        await callback_battle_attack(mock_callback)

        # Проверяем сообщение об ошибке
        mock_callback.answer.assert_called_once()
        call_args = mock_callback.answer.call_args[0][0]
        assert "нет активного боя" in call_args


@pytest.mark.asyncio
async def test_callback_battle_defend(mock_callback, player_in_battle):
    """Тест защиты игрока."""
    player_in_battle.battle_state.monster_hp = 50

    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.monster_attack', return_value=(3, False)):

        mock_service.get_or_create.return_value = player_in_battle

        await callback_battle_defend(mock_callback)

        # Проверяем, что бой продолжается
        mock_callback.message.edit_caption.assert_called_once()
        mock_service.save_player.assert_called_once()


@pytest.mark.asyncio
async def test_callback_battle_spells(mock_callback, player_in_battle):
    """Тест показа меню заклинаний."""
    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.get_spells_battle_keyboard'):

        mock_service.get_or_create.return_value = player_in_battle

        await callback_battle_spells(mock_callback)

        # Проверяем, что клавиатура обновлена
        mock_callback.message.edit_reply_markup.assert_called_once()
        mock_callback.answer.assert_called_once()


@pytest.mark.asyncio
async def test_callback_cast_spell_success(mock_callback, player_in_battle):
    """Тест успешного применения заклинания."""
    mock_callback.data = "cast_fireball"
    player_in_battle.battle_state.monster_hp = 50
    player_in_battle.mana = 50

    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.cast_spell', return_value=(True, "⚡ Огненный шар!", 20)), \
         patch('handlers.battle_handlers.monster_attack', return_value=(5, False)):

        mock_service.get_or_create.return_value = player_in_battle

        await callback_cast_spell(mock_callback)

        # Проверяем, что бой продолжается
        mock_callback.message.edit_caption.assert_called_once()


@pytest.mark.asyncio
async def test_callback_cast_spell_insufficient_mana(mock_callback, player_in_battle):
    """Тест применения заклинания без маны."""
    mock_callback.data = "cast_fireball"
    player_in_battle.mana = 0

    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.cast_spell', return_value=(False, "Недостаточно маны", 0)):

        mock_service.get_or_create.return_value = player_in_battle

        await callback_cast_spell(mock_callback)

        # Проверяем, что показано предупреждение
        mock_callback.answer.assert_called_once()
        call_args = mock_callback.answer.call_args[0][0]
        assert "маны" in call_args


@pytest.mark.asyncio
async def test_callback_battle_potions(mock_callback, player_in_battle):
    """Тест показа меню зелий."""
    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.get_potions_battle_keyboard'):

        mock_service.get_or_create.return_value = player_in_battle

        await callback_battle_potions(mock_callback)

        # Проверяем, что клавиатура обновлена
        mock_callback.message.edit_reply_markup.assert_called_once()
        mock_callback.answer.assert_called_once()


@pytest.mark.asyncio
async def test_callback_use_potion_success(mock_callback, player_in_battle):
    """Тест успешного использования зелья."""
    mock_callback.data = "use_health"
    player_in_battle.hp = 50
    player_in_battle.potions = {"health": 1}

    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.use_potion', return_value=(True, "💚 Восстановлено 50 HP!")), \
         patch('handlers.battle_handlers.monster_attack', return_value=(5, False)):

        mock_service.get_or_create.return_value = player_in_battle

        await callback_use_potion(mock_callback)

        # Проверяем, что бой продолжается
        mock_callback.message.edit_caption.assert_called_once()


@pytest.mark.asyncio
async def test_callback_battle_flee_success(mock_callback, player_in_battle):
    """Тест успешного побега."""
    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.flee_battle', return_value=True):

        mock_service.get_or_create.return_value = player_in_battle

        await callback_battle_flee(mock_callback)

        # Проверяем, что бой завершён
        assert player_in_battle.battle_state is None
        mock_callback.message.edit_caption.assert_called_once()


@pytest.mark.asyncio
async def test_callback_battle_flee_fail(mock_callback, player_in_battle):
    """Тест неудачного побега."""
    player_in_battle.battle_state.monster_hp = 50

    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.flee_battle', return_value=False), \
         patch('handlers.battle_handlers.monster_attack', return_value=(5, False)):

        mock_service.get_or_create.return_value = player_in_battle

        await callback_battle_flee(mock_callback)

        # Проверяем, что бой продолжается
        assert player_in_battle.battle_state is not None
        mock_callback.message.edit_caption.assert_called_once()


@pytest.mark.asyncio
async def test_callback_battle_flee_from_boss(mock_callback, player_in_battle):
    """Тест попытки побега от босса."""
    player_in_battle.battle_state.is_boss = True

    with patch('handlers.battle_handlers.player_service') as mock_service:
        mock_service.get_or_create.return_value = player_in_battle

        await callback_battle_flee(mock_callback)

        # Проверяем, что побег невозможен
        mock_callback.answer.assert_called_once()
        call_args = mock_callback.answer.call_args[0][0]
        assert "босса" in call_args


@pytest.mark.asyncio
async def test_callback_battle_back(mock_callback, player_in_battle):
    """Тест возврата к действиям боя."""
    with patch('handlers.battle_handlers.player_service') as mock_service, \
         patch('handlers.battle_handlers.get_battle_keyboard'):

        mock_service.get_or_create.return_value = player_in_battle

        await callback_battle_back(mock_callback)

        # Проверяем, что клавиатура обновлена
        mock_callback.message.edit_reply_markup.assert_called_once()
        mock_callback.answer.assert_called_once()


def test_format_battle_status(test_player, test_battle_state):
    """Тест форматирования статуса боя."""
    test_player.hp = 80
    test_player.max_hp = 100
    test_player.mana = 30
    test_player.max_mana = 50

    test_battle_state.monster_hp = 20
    test_battle_state.monster_max_hp = 30
    test_battle_state.turn = 3

    result = format_battle_status(test_player, test_battle_state)

    # Проверяем наличие ключевых элементов
    assert "БОЙ" in result
    assert "Ход 3" in result
    assert test_battle_state.monster_name in result
    assert "80/100" in result  # HP игрока
    assert "30/50" in result   # Мана игрока
