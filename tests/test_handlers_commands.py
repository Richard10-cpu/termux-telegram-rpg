"""Тесты обработчиков команд."""
import pytest
from unittest.mock import patch, Mock
from handlers.commands import cmd_start, cmd_equip, cmd_top
from models import StoryProgress


@pytest.mark.asyncio
async def test_cmd_start_new_player(mock_message, test_player):
    """Тест команды /start для нового игрока."""
    # Создаём мок главы
    mock_chapter = Mock()
    mock_chapter.title = "Глава 1: Начало приключения"
    mock_chapter.boss_name = "Лесной тролль"

    with patch('handlers.commands.player_service') as mock_service, \
         patch('handlers.commands.get_current_chapter', return_value=mock_chapter), \
         patch('handlers.commands.main_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await cmd_start(mock_message)

        # Проверяем, что отправлено приветственное сообщение
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "Добро пожаловать" in call_args
        assert "Глава 1" in call_args
        assert "Лесной тролль" in call_args


@pytest.mark.asyncio
async def test_cmd_start_with_chapter(mock_message, player_with_story):
    """Тест команды /start с активной главой."""
    # Создаём мок главы
    mock_chapter = Mock()
    mock_chapter.title = "Глава 2: Темный лес"
    mock_chapter.boss_name = "Темный маг"

    with patch('handlers.commands.player_service') as mock_service, \
         patch('handlers.commands.get_current_chapter', return_value=mock_chapter), \
         patch('handlers.commands.main_keyboard'):

        mock_service.get_or_create.return_value = player_with_story

        await cmd_start(mock_message)

        # Проверяем наличие информации о главе
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "Глава 2" in call_args


@pytest.mark.asyncio
async def test_cmd_start_completed_story(mock_message, test_player):
    """Тест команды /start для игрока, завершившего сюжет."""
    with patch('handlers.commands.player_service') as mock_service, \
         patch('handlers.commands.get_current_chapter', return_value=None), \
         patch('handlers.commands.main_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await cmd_start(mock_message)

        # Проверяем сообщение о завершении сюжета
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "прошли все главы" in call_args


@pytest.mark.asyncio
async def test_cmd_equip_success(mock_message, test_player):
    """Тест успешной экипировки предмета."""
    mock_message.text = "/equip Железный меч"
    test_player.inventory = ["Железный меч"]

    with patch('handlers.commands.player_service') as mock_service, \
         patch('handlers.commands.equip_item', return_value=(True, "✅ Экипировано: Железный меч")):

        mock_service.get_or_create.return_value = test_player

        await cmd_equip(mock_message)

        # Проверяем, что предмет экипирован
        mock_service.save_player.assert_called_once()
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "Экипировано" in call_args or "✅" in call_args


@pytest.mark.asyncio
async def test_cmd_equip_missing_args(mock_message, test_player):
    """Тест команды /equip без аргументов."""
    mock_message.text = "/equip"

    with patch('handlers.commands.player_service') as mock_service:
        mock_service.get_or_create.return_value = test_player

        await cmd_equip(mock_message)

        # Проверяем сообщение об ошибке
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "Укажите предмет" in call_args


@pytest.mark.asyncio
async def test_cmd_equip_item_not_found(mock_message, test_player):
    """Тест экипировки несуществующего предмета."""
    mock_message.text = "/equip Мифический меч"
    test_player.inventory = ["Деревянная палка"]

    with patch('handlers.commands.player_service') as mock_service, \
         patch('handlers.commands.equip_item', return_value=(False, "❌ Предмет не найден в инвентаре")):

        mock_service.get_or_create.return_value = test_player

        await cmd_equip(mock_message)

        # Проверяем сообщение об ошибке
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "не найден" in call_args.lower() or "❌" in call_args


@pytest.mark.asyncio
async def test_cmd_top_with_players(mock_message):
    """Тест команды /top с игроками."""
    # Создаём мок игроков
    top_players = [
        Mock(user_id=1, level=10, gold=1000, total_kills=50),
        Mock(user_id=2, level=8, gold=500, total_kills=30),
        Mock(user_id=3, level=5, gold=200, total_kills=15)
    ]

    with patch('handlers.commands.player_service') as mock_service, \
         patch('handlers.commands.format_top_players', return_value="🏆 ТОП-10 ИГРОКОВ\n\n1. Игрок 1"):

        mock_service.get_top_players.return_value = top_players

        await cmd_top(mock_message)

        # Проверяем, что отправлен рейтинг
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "ТОП" in call_args or "Игрок" in call_args


@pytest.mark.asyncio
async def test_cmd_top_empty(mock_message):
    """Тест команды /top без игроков."""
    with patch('handlers.commands.player_service') as mock_service:
        mock_service.get_top_players.return_value = []

        await cmd_top(mock_message)

        # Проверяем сообщение о пустом рейтинге
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "нет игроков" in call_args.lower()
