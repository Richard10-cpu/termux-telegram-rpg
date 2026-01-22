"""Тесты для моделей данных."""
import pytest
from models import Player, Equipment, BattleState, Monster, MonsterTemplate, Item, ItemType


class TestPlayer:
    """Тесты модели игрока."""

    def test_player_creation(self, test_player):
        """Тест создания игрока."""
        assert test_player.user_id == 123456789
        assert test_player.hp == 100
        assert test_player.max_hp == 100
        assert test_player.level == 1
        assert test_player.gold == 20
        assert test_player.power == 10

    def test_player_to_dict(self, test_player):
        """Тест сериализации игрока в словарь."""
        data = test_player.to_dict()
        assert isinstance(data, dict)
        assert data['user_id'] == 123456789
        assert data['hp'] == 100
        assert data['level'] == 1

    def test_player_from_dict(self):
        """Тест десериализации игрока из словаря."""
        data = {
            'user_id': 987654321,
            'hp': 50,
            'max_hp': 100,
            'level': 5,
            'exp': 100,
            'gold': 500,
            'power': 25,
            'inventory': ['Стальной меч'],
            'location': 'forest'
        }
        player = Player.from_dict(data)
        assert player.user_id == 987654321
        assert player.hp == 50
        assert player.level == 5
        assert player.gold == 500


class TestEquipment:
    """Тесты экипировки."""

    def test_equipment_creation(self):
        """Тест создания экипировки."""
        equipment = Equipment(weapon="Стальной меч", armor="Кожаная броня")
        assert equipment.weapon == "Стальной меч"
        assert equipment.armor == "Кожаная броня"

    def test_equipment_to_dict(self):
        """Тест сериализации экипировки."""
        equipment = Equipment(weapon="Меч", armor="Броня")
        data = equipment.to_dict()
        assert data['weapon'] == "Меч"
        assert data['armor'] == "Броня"

    def test_equipment_from_dict(self):
        """Тест десериализации экипировки."""
        data = {'weapon': 'Топор', 'armor': None}
        equipment = Equipment.from_dict(data)
        assert equipment.weapon == 'Топор'
        assert equipment.armor is None


class TestBattleState:
    """Тесты состояния боя."""

    def test_battle_state_creation(self, test_battle_state):
        """Тест создания состояния боя."""
        assert test_battle_state.monster_name == "Тестовый слайм"
        assert test_battle_state.monster_hp > 0
        assert test_battle_state.turn == 1
        assert not test_battle_state.defending

    def test_battle_state_to_dict(self, test_battle_state):
        """Тест сериализации состояния боя."""
        data = test_battle_state.to_dict()
        assert isinstance(data, dict)
        assert data['monster_name'] == "Тестовый слайм"
        assert 'monster_hp' in data

    def test_battle_state_from_dict(self):
        """Тест десериализации состояния боя."""
        data = {
            'monster_key': 'slime',
            'monster_name': 'Слайм',
            'monster_hp': 20,
            'monster_max_hp': 30,
            'monster_power': 5,
            'monster_exp': 10,
            'monster_gold_min': 5,
            'monster_gold_max': 10,
            'is_boss': False,
            'turn': 3
        }
        state = BattleState.from_dict(data)
        assert state.monster_name == 'Слайм'
        assert state.monster_hp == 20
        assert state.turn == 3


class TestMonster:
    """Тесты монстров."""

    def test_monster_creation(self, test_monster):
        """Тест создания монстра."""
        assert test_monster.name == "Тестовый слайм"
        assert test_monster.hp > 0
        assert test_monster.power > 0

    def test_monster_from_template(self):
        """Тест создания монстра из шаблона."""
        template = MonsterTemplate(
            key="goblin",
            name="Гоблин",
            hp=50,
            power=8,
            exp=15,
            gold_min=8,
            gold_max=15,
            min_level=1,
            max_level=10
        )
        monster = Monster.from_template(template)
        assert monster.name == "Гоблин"
        assert monster.hp == 50
        assert monster.max_hp == 50
        assert monster.key == "goblin"

    def test_monster_level_availability(self):
        """Тест доступности монстра по уровню."""
        template = MonsterTemplate(
            key="dragon",
            name="Дракон",
            hp=500,
            power=50,
            exp=200,
            gold_min=100,
            gold_max=200,
            min_level=10,
            max_level=20
        )
        assert template.is_available_for_level(5) is False
        assert template.is_available_for_level(15) is True
        assert template.is_available_for_level(25) is False


class TestItem:
    """Тесты предметов."""

    def test_item_creation(self, test_weapon):
        """Тест создания предмета."""
        assert test_weapon.name == "Тестовый меч"
        assert test_weapon.item_type == ItemType.WEAPON
        assert test_weapon.cost == 50
        assert test_weapon.power_bonus == 10

    def test_item_is_equipable(self, test_weapon, test_armor):
        """Тест проверки экипируемости предмета."""
        assert test_weapon.is_equipable is True
        assert test_armor.is_equipable is True

        potion = Item(
            key="health_potion",
            name="Зелье здоровья",
            item_type=ItemType.CONSUMABLE,
            cost=25
        )
        assert potion.is_equipable is False

    def test_item_is_spell(self):
        """Тест проверки является ли предмет заклинанием."""
        spell = Item(
            key="fireball",
            name="Огненный шар",
            item_type=ItemType.SPELL,
            cost=100,
            mana_cost=15,
            spell_damage=40
        )
        assert spell.is_spell is True

        weapon = Item(
            key="sword",
            name="Меч",
            item_type=ItemType.WEAPON,
            cost=50
        )
        assert weapon.is_spell is False
