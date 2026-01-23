"""Тесты обработчиков квестов."""
import pytest
from unittest.mock import patch
from handlers.quest_handlers import show_quests, claim_quest_reward, refresh_quests


@pytest.mark.asyncio
async def test_show_quests(mock_message, test_player):
    """Тест показа квестов."""
    with patch('handlers.quest_handlers.player_service') as mock_service, \
         patch('handlers.quest_handlers.format_quest_status', return_value="📜 Ежедневный квест"), \
         patch('handlers.quest_handlers.quest_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await show_quests(mock_message)

        # Проверяем, что информация отправлена
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "квест" in call_args.lower()
        mock_service.save_player.assert_called_once()


@pytest.mark.asyncio
async def test_claim_quest_reward_success(mock_message, test_player):
    """Тест успешного получения награды за квест."""
    with patch('handlers.quest_handlers.player_service') as mock_service, \
         patch('handlers.quest_handlers.claim_daily_reward', return_value=(True, "🎁 Награда получена!")), \
         patch('handlers.quest_handlers.main_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await claim_quest_reward(mock_message)

        # Проверяем, что награда получена
        mock_service.save_player.assert_called_once()
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "Награда" in call_args or "🎁" in call_args


@pytest.mark.asyncio
async def test_claim_quest_reward_not_ready(mock_message, test_player):
    """Тест получения награды при незавершённом квесте."""
    with patch('handlers.quest_handlers.player_service') as mock_service, \
         patch('handlers.quest_handlers.claim_daily_reward', return_value=(False, "❌ Квест ещё не выполнен!")):

        mock_service.get_or_create.return_value = test_player

        await claim_quest_reward(mock_message)

        # Проверяем сообщение об ошибке
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "не выполнен" in call_args.lower() or "❌" in call_args


@pytest.mark.asyncio
async def test_refresh_quests(mock_message, test_player):
    """Тест обновления информации о квестах."""
    with patch('handlers.quest_handlers.player_service') as mock_service, \
         patch('handlers.quest_handlers.format_quest_status', return_value="📜 Обновлённый квест"), \
         patch('handlers.quest_handlers.quest_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await refresh_quests(mock_message)

        # Проверяем, что информация обновлена
        mock_message.answer.assert_called_once()
        mock_service.save_player.assert_called_once()
