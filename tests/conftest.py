"""Конфигурация pytest и общие фикстуры."""
import os
import pytest
from unittest.mock import AsyncMock, Mock
from models import Player, Monster, MonsterTemplate, Item, ItemType, Equipment, BattleState


@pytest.fixture
def test_player():
    """Создать тестового игрока."""
    return Player(
        user_id=123456789,
        hp=100,
        max_hp=100,
        mana=50,
        max_mana=50,
        level=1,
        exp=0,
        gold=20,
        power=10,
        inventory=["Деревянная палка"],
        location="village"
    )


# Фикстуры для сервисов
@pytest.fixture
def temp_data_file(tmp_path):
    """Временный файл для тестирования репозитория."""
    return str(tmp_path / "test_players.json")


@pytest.fixture
def test_repository(temp_data_file):
    """Репозиторий с временным файлом."""
    from services import DataRepository
    repo = DataRepository(data_file=temp_data_file)
    yield repo
    if os.path.exists(temp_data_file):
        os.remove(temp_data_file)


@pytest.fixture
def test_repository_with_data(test_repository):
    """Репозиторий с тестовыми данными."""
    test_data = {
        "123": {"user_id": 123, "level": 5, "gold": 100},
        "456": {"user_id": 456, "level": 10, "gold": 500}
    }
    test_repository.save_all(test_data)
    return test_repository


@pytest.fixture
def fresh_player_service(test_repository):
    """Новый экземпляр PlayerService для каждого теста."""
    from services import PlayerService
    PlayerService._instance = None
    return PlayerService(repository=test_repository)


# Фикстуры для игровой логики
@pytest.fixture
def player_with_spells(test_player):
    """Игрок с изученными заклинаниями."""
    test_player.spells = ["⚡ Огненный шар", "✨ Исцеление"]
    test_player.mana = 50
    test_player.max_mana = 50
    return test_player


@pytest.fixture
def player_with_quests(test_player):
    """Игрок с квестами."""
    from datetime import datetime
    from models import DailyQuest
    test_player.quests = {
        "daily": DailyQuest(
            date=datetime.now().strftime("%Y-%m-%d"),
            kills=2,
            target=5,
            reward_claimed=False
        )
    }
    return test_player


@pytest.fixture
def player_with_story(test_player):
    """Игрок с прогрессом сюжета."""
    from models import StoryProgress
    test_player.story_progress = StoryProgress(
        current_chapter=1,
        completed_chapters=[],
        boss_defeated={}
    )
    return test_player


@pytest.fixture
def player_with_achievements(test_player):
    """Игрок с достижениями."""
    test_player.total_kills = 5
    test_player.gold = 50
    test_player.level = 3
    test_player.achievements = ["first_blood"]
    return test_player


@pytest.fixture
def test_monster():
    """Создать тестового монстра."""
    template = MonsterTemplate(
        key="test_slime",
        name="Тестовый слайм",
        hp=30,
        power=5,
        exp=10,
        gold_min=5,
        gold_max=10,
        min_level=1,
        max_level=5
    )
    return Monster.from_template(template)


@pytest.fixture
def test_weapon():
    """Создать тестовое оружие."""
    return Item(
        key="test_sword",
        name="Тестовый меч",
        item_type=ItemType.WEAPON,
        cost=50,
        power_bonus=10
    )


@pytest.fixture
def test_armor():
    """Создать тестовую броню."""
    return Item(
        key="test_armor",
        name="Тестовая броня",
        item_type=ItemType.ARMOR,
        cost=80,
        max_hp_bonus=20
    )


@pytest.fixture
def test_battle_state(test_monster):
    """Создать тестовое состояние боя."""
    return BattleState(
        monster_key=test_monster.key,
        monster_name=test_monster.name,
        monster_hp=test_monster.hp,
        monster_max_hp=test_monster.max_hp,
        monster_power=test_monster.power,
        monster_exp=test_monster.exp,
        monster_gold_min=test_monster.gold_range[0],
        monster_gold_max=test_monster.gold_range[1]
    )


# Фикстуры для тестирования Aiogram handlers
@pytest.fixture
def mock_message():
    """Создать мок объекта Message."""
    message = Mock()
    message.from_user = Mock()
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    message.answer_photo = AsyncMock()
    message.edit_text = AsyncMock()
    message.text = None
    return message


@pytest.fixture
def mock_callback():
    """Создать мок объекта CallbackQuery."""
    callback = Mock()
    callback.from_user = Mock()
    callback.from_user.id = 123456789
    callback.message = Mock()
    callback.message.edit_caption = AsyncMock()
    callback.message.edit_text = AsyncMock()
    callback.message.edit_reply_markup = AsyncMock()
    callback.message.delete = AsyncMock()
    callback.answer = AsyncMock()
    callback.data = None
    return callback


@pytest.fixture
def player_in_battle(test_player, test_battle_state):
    """Игрок с активным боем."""
    test_player.battle_state = test_battle_state
    test_player.hp = 100
    test_player.mana = 50
    return test_player


@pytest.fixture
def player_with_inventory(test_player):
    """Игрок с предметами в инвентаре."""
    test_player.inventory = [
        "Деревянная палка",
        "Зелье здоровья",
        "Зелье маны"
    ]
    return test_player


@pytest.fixture
def player_with_equipment(test_player):
    """Игрок с экипированными предметами."""
    test_player.equipment = Equipment(
        weapon="Железный меч",
        armor="Кожаная броня"
    )
    return test_player
