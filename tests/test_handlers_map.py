"""Тесты обработчиков карты и путешествий."""
import pytest
from unittest.mock import patch, Mock
from handlers.map_handlers import show_map, travel_to_location


@pytest.mark.asyncio
async def test_show_map(mock_message, test_player):
    """Тест показа карты."""
    test_player.location = "village"

    mock_location = Mock()
    mock_location.name = "Деревня"
    mock_location.description = "Мирное место"
    mock_location.image_path = None

    with patch('handlers.map_handlers.player_service') as mock_service, \
         patch('handlers.map_handlers.format_location_info', return_value="📍 Деревня"), \
         patch('handlers.map_handlers.LOCATIONS', {"village": mock_location}), \
         patch('handlers.map_handlers.map_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await show_map(mock_message)

        # Проверяем, что информация отправлена
        mock_message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_show_map_with_image(mock_message, test_player):
    """Тест показа карты с изображением."""
    test_player.location = "forest"

    mock_location = Mock()
    mock_location.name = "Тёмный лес"
    mock_location.description = "Опасное место"
    mock_location.image_path = "assets/locations/forest.jpg"

    with patch('handlers.map_handlers.player_service') as mock_service, \
         patch('handlers.map_handlers.format_location_info', return_value="📍 Тёмный лес"), \
         patch('handlers.map_handlers.LOCATIONS', {"forest": mock_location}), \
         patch('handlers.map_handlers.map_keyboard'), \
         patch('handlers.map_handlers.FSInputFile'):

        mock_service.get_or_create.return_value = test_player

        await show_map(mock_message)

        # Проверяем, что фото отправлено
        mock_message.answer_photo.assert_called_once()


@pytest.mark.asyncio
async def test_travel_to_location(mock_message, test_player):
    """Тест перемещения в локацию."""
    mock_message.text = "🌲 Тёмный лес"
    test_player.location = "village"

    mock_location = Mock()
    mock_location.name = "Тёмный лес"
    mock_location.description = "Опасное место, полное монстров"
    mock_location.image_path = None

    with patch('handlers.map_handlers.player_service') as mock_service, \
         patch('handlers.map_handlers.LOCATIONS', {"forest": mock_location}):

        mock_service.get_or_create.return_value = test_player

        await travel_to_location(mock_message)

        # Проверяем, что локация изменена
        assert test_player.location == "forest"
        mock_service.save_player.assert_called_once()
        mock_message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_travel_all_locations(mock_message, test_player):
    """Тест перемещения во все локации."""
    locations = {
        "🏘️ Деревня": "village",
        "🌲 Тёмный лес": "forest",
        "🕳️ Пещера": "cave",
        "⛰️ Гора": "mountain"
    }

    mock_location = Mock()
    mock_location.name = "Локация"
    mock_location.description = "Описание"
    mock_location.image_path = None

    for location_text, location_key in locations.items():
        mock_message.text = location_text
        test_player.location = "village"

        with patch('handlers.map_handlers.player_service') as mock_service, \
             patch('handlers.map_handlers.LOCATIONS', {location_key: mock_location}):

            mock_service.get_or_create.return_value = test_player

            await travel_to_location(mock_message)

            # Проверяем, что локация изменена
            assert test_player.location == location_key
