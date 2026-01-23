"""Тесты обработчиков магазина."""
import pytest
from unittest.mock import patch, Mock
from handlers.shop_handlers import (
    open_shop,
    callback_shop_main,
    callback_shop_equipment,
    callback_shop_spells,
    callback_shop_potions,
    callback_buy_item,
    callback_shop_close,
    go_back
)
from models import Item, ItemType, ShopItem


@pytest.mark.asyncio
async def test_open_shop(mock_message, test_player):
    """Тест открытия магазина."""
    test_player.gold = 100

    with patch('handlers.shop_handlers.player_service') as mock_service, \
         patch('handlers.shop_handlers.get_shop_main_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await open_shop(mock_message)

        # Проверяем, что ответ отправлен
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "магазин" in call_args.lower()
        assert "100" in call_args  # Золото игрока


@pytest.mark.asyncio
async def test_callback_shop_main(mock_callback, test_player):
    """Тест главного меню магазина."""
    test_player.gold = 100

    with patch('handlers.shop_handlers.player_service') as mock_service, \
         patch('handlers.shop_handlers.get_shop_main_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await callback_shop_main(mock_callback)

        # Проверяем, что текст обновлён
        mock_callback.message.edit_text.assert_called_once()
        mock_callback.answer.assert_called_once()


@pytest.mark.asyncio
async def test_callback_shop_equipment(mock_callback, test_player):
    """Тест показа категории оружия."""
    test_player.gold = 100

    with patch('handlers.shop_handlers.player_service') as mock_service, \
         patch('handlers.shop_handlers.get_equipment_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await callback_shop_equipment(mock_callback)

        # Проверяем, что текст обновлён
        mock_callback.message.edit_text.assert_called_once()
        call_args = mock_callback.message.edit_text.call_args[0][0]
        assert "ОРУЖИЕ" in call_args or "БРОНЯ" in call_args


@pytest.mark.asyncio
async def test_callback_shop_spells(mock_callback, test_player):
    """Тест показа категории заклинаний."""
    test_player.gold = 100
    test_player.level = 5

    with patch('handlers.shop_handlers.player_service') as mock_service, \
         patch('handlers.shop_handlers.get_spells_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await callback_shop_spells(mock_callback)

        # Проверяем, что текст обновлён
        mock_callback.message.edit_text.assert_called_once()
        call_args = mock_callback.message.edit_text.call_args[0][0]
        assert "ЗАКЛИНАНИЯ" in call_args


@pytest.mark.asyncio
async def test_callback_shop_potions(mock_callback, test_player):
    """Тест показа категории зелий."""
    test_player.gold = 100

    with patch('handlers.shop_handlers.player_service') as mock_service, \
         patch('handlers.shop_handlers.get_potions_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await callback_shop_potions(mock_callback)

        # Проверяем, что текст обновлён
        mock_callback.message.edit_text.assert_called_once()
        call_args = mock_callback.message.edit_text.call_args[0][0]
        assert "ЗЕЛЬЯ" in call_args


@pytest.mark.asyncio
async def test_callback_buy_item_success(mock_callback, test_player):
    """Тест успешной покупки предмета."""
    mock_callback.data = "buy_wooden_sword"
    test_player.gold = 100

    # Создаём мок предмета
    mock_item = Item(
        key="wooden_sword",
        name="Деревянный меч",
        item_type=ItemType.WEAPON,
        cost=30,
        power_bonus=5
    )
    mock_shop_item = ShopItem(item=mock_item, unique=True)

    with patch('handlers.shop_handlers.player_service') as mock_service, \
         patch('handlers.shop_handlers.SHOP_ITEMS', {"wooden_sword": mock_shop_item}), \
         patch('handlers.shop_handlers.purchase_item', return_value=(True, "✅ Куплено!")), \
         patch('handlers.shop_handlers.get_equipment_keyboard'):

        mock_service.get_or_create.return_value = test_player

        await callback_buy_item(mock_callback)

        # Проверяем, что покупка прошла
        mock_service.save_player.assert_called_once()
        mock_callback.answer.assert_called_once()
        call_args = mock_callback.answer.call_args[0][0]
        assert "Куплено" in call_args or "✅" in call_args


@pytest.mark.asyncio
async def test_callback_buy_item_insufficient_gold(mock_callback, test_player):
    """Тест покупки без достаточного золота."""
    mock_callback.data = "buy_iron_sword"
    test_player.gold = 10

    # Создаём мок предмета
    mock_item = Item(
        key="iron_sword",
        name="Железный меч",
        item_type=ItemType.WEAPON,
        cost=100,
        power_bonus=15
    )
    mock_shop_item = ShopItem(item=mock_item, unique=True)

    with patch('handlers.shop_handlers.player_service') as mock_service, \
         patch('handlers.shop_handlers.SHOP_ITEMS', {"iron_sword": mock_shop_item}), \
         patch('handlers.shop_handlers.purchase_item', return_value=(False, "❌ Недостаточно золота!")):

        mock_service.get_or_create.return_value = test_player

        await callback_buy_item(mock_callback)

        # Проверяем, что показано сообщение об ошибке
        mock_callback.answer.assert_called_once()
        call_args = mock_callback.answer.call_args[0][0]
        assert "золота" in call_args.lower() or "❌" in call_args


@pytest.mark.asyncio
async def test_callback_buy_item_level_requirement(mock_callback, test_player):
    """Тест покупки предмета с требованием уровня."""
    mock_callback.data = "buy_fireball_spell"
    test_player.gold = 500
    test_player.level = 1

    # Создаём мок заклинания с требованием уровня
    mock_item = Item(
        key="fireball_spell",
        name="⚡ Огненный шар",
        item_type=ItemType.SPELL,
        cost=200,
        spell_damage=30,
        mana_cost=15,
        required_level=5
    )
    mock_shop_item = ShopItem(item=mock_item, unique=True)

    with patch('handlers.shop_handlers.player_service') as mock_service, \
         patch('handlers.shop_handlers.SHOP_ITEMS', {"fireball_spell": mock_shop_item}), \
         patch('handlers.shop_handlers.purchase_item', return_value=(False, "❌ Требуется 5 уровень! У вас 1.")):

        mock_service.get_or_create.return_value = test_player

        await callback_buy_item(mock_callback)

        # Проверяем, что показано сообщение об уровне
        mock_callback.answer.assert_called_once()
        call_args = mock_callback.answer.call_args[0][0]
        assert "уровень" in call_args.lower() or "❌" in call_args


@pytest.mark.asyncio
async def test_callback_buy_item_not_found(mock_callback, test_player):
    """Тест покупки несуществующего предмета."""
    mock_callback.data = "buy_unknown_item"

    with patch('handlers.shop_handlers.player_service') as mock_service, \
         patch('handlers.shop_handlers.SHOP_ITEMS', {}):

        mock_service.get_or_create.return_value = test_player

        await callback_buy_item(mock_callback)

        # Проверяем, что показано сообщение об ошибке
        mock_callback.answer.assert_called_once()
        call_args = mock_callback.answer.call_args[0][0]
        assert "не найден" in call_args.lower()


@pytest.mark.asyncio
async def test_callback_shop_close(mock_callback):
    """Тест закрытия магазина."""
    await callback_shop_close(mock_callback)

    # Проверяем, что сообщение удалено
    mock_callback.message.delete.assert_called_once()
    mock_callback.answer.assert_called_once()


@pytest.mark.asyncio
async def test_go_back(mock_message):
    """Тест возврата в главное меню."""
    with patch('handlers.shop_handlers.main_keyboard'):
        await go_back(mock_message)

        # Проверяем, что отправлено сообщение
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "главн" in call_args.lower()
