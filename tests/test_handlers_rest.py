"""Тесты обработчиков отдыха и рейтинга."""
import pytest
from unittest.mock import patch, Mock
from handlers.rest_handlers import rest_and_heal, show_rating_inline


@pytest.mark.asyncio
async def test_rest_and_heal_success(mock_message, test_player):
    """Тест успешного отдыха."""
    test_player.gold = 50
    test_player.hp = 50
    test_player.max_hp = 100
    test_player.mana = 20
    test_player.max_mana = 50

    with patch('handlers.rest_handlers.player_service') as mock_service:
        mock_service.get_or_create.return_value = test_player

        await rest_and_heal(mock_message)

        # Проверяем, что здоровье и мана восстановлены
        assert test_player.hp == test_player.max_hp
        assert test_player.mana == test_player.max_mana
        assert test_player.gold == 35  # 50 - 15
        mock_service.save_player.assert_called_once()
        mock_message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_rest_and_heal_insufficient_gold(mock_message, test_player):
    """Тест отдыха без достаточного золота."""
    test_player.gold = 10  # Меньше 15
    test_player.hp = 50
    test_player.max_hp = 100

    with patch('handlers.rest_handlers.player_service') as mock_service:
        mock_service.get_or_create.return_value = test_player

        await rest_and_heal(mock_message)

        # Проверяем, что здоровье не изменилось
        assert test_player.hp == 50
        assert test_player.gold == 10
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "Не хватает золота" in call_args


@pytest.mark.asyncio
async def test_show_rating_inline_with_players(mock_message):
    """Тест показа рейтинга с игроками."""
    top_players = [
        Mock(user_id=1, level=10, gold=1000),
        Mock(user_id=2, level=8, gold=500)
    ]

    with patch('handlers.rest_handlers.player_service') as mock_service, \
         patch('handlers.rest_handlers.format_top_players', return_value="🏆 ТОП ИГРОКОВ"):

        mock_service.get_top_players.return_value = top_players

        await show_rating_inline(mock_message)

        # Проверяем, что рейтинг отправлен
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "ТОП" in call_args


@pytest.mark.asyncio
async def test_show_rating_inline_empty(mock_message):
    """Тест показа пустого рейтинга."""
    with patch('handlers.rest_handlers.player_service') as mock_service:
        mock_service.get_top_players.return_value = []

        await show_rating_inline(mock_message)

        # Проверяем сообщение о пустом рейтинге
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "нет игроков" in call_args.lower()
