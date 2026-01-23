"""Тесты обработчика профиля."""
import pytest
from unittest.mock import patch
from handlers.profile import show_profile


@pytest.mark.asyncio
async def test_show_profile(mock_message, test_player):
    """Тест показа профиля игрока."""
    test_player.level = 5
    test_player.gold = 100
    test_player.exp = 250

    with patch('handlers.profile.player_service') as mock_service, \
         patch('handlers.profile.format_profile', return_value="👤 ПРОФИЛЬ\n\nУровень: 5"):

        mock_service.get_or_create.return_value = test_player

        await show_profile(mock_message)

        # Проверяем, что профиль отправлен
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "ПРОФИЛЬ" in call_args or "Уровень" in call_args
