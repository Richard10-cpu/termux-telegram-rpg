"""Конфигурация pytest и общие фикстуры."""
import pytest
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
