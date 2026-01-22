"""Тесты игровой логики (опыт, торговля, экипировка)."""
import pytest
from game_logic.experience import exp_for_level, check_level_up, add_experience
from game_logic.trading import (
    get_item_type, can_purchase_item, purchase_item,
    equip_item, get_item_by_name
)
from models import Player, ItemType


class TestExperience:
    """Тесты системы опыта и уровней."""

    def test_exp_for_level(self):
        """Тест расчёта необходимого опыта для уровня."""
        assert exp_for_level(1) == 60
        assert exp_for_level(2) == 120
        assert exp_for_level(5) == 300

    def test_check_level_up_no_level_up(self, test_player):
        """Тест проверки уровня без повышения."""
        test_player.exp = 50
        test_player.level = 1
        level_up, message = check_level_up(test_player)
        assert level_up is False
        assert message is None
        assert test_player.level == 1

    def test_check_level_up_success(self, test_player):
        """Тест успешного повышения уровня."""
        test_player.exp = 60
        test_player.level = 1
        test_player.hp = 80
        old_max_hp = test_player.max_hp
        old_power = test_player.power

        level_up, message = check_level_up(test_player)

        assert level_up is True
        assert message is not None
        assert "УРОВЕНЬ ПОВЫШЕН" in message
        assert test_player.level == 2
        assert test_player.max_hp > old_max_hp
        assert test_player.power > old_power
        assert test_player.hp == test_player.max_hp  # Полное лечение

    def test_add_experience(self, test_player):
        """Тест добавления опыта."""
        test_player.exp = 0
        test_player.level = 1

        # Добавляем опыт, но недостаточно для уровня
        level_up, _ = add_experience(test_player, 30)
        assert level_up is False
        assert test_player.exp == 30
        assert test_player.level == 1

        # Добавляем ещё опыт, достаточно для уровня
        level_up, message = add_experience(test_player, 30)
        assert level_up is True
        assert message is not None
        assert test_player.exp == 60
        assert test_player.level == 2


class TestTrading:
    """Тесты торговли."""

    def test_get_item_type(self):
        """Тест определения типа предмета."""
        assert get_item_type("Стальной меч") == ItemType.WEAPON
        assert get_item_type("Кожаная броня") == ItemType.ARMOR

    def test_can_purchase_item_not_found(self, test_player):
        """Тест покупки несуществующего предмета."""
        can_buy, message = can_purchase_item(test_player, "nonexistent_item")
        assert can_buy is False
        assert "не найден" in message.lower()

    def test_can_purchase_item_not_enough_gold(self, test_player):
        """Тест покупки при недостатке золота."""
        test_player.gold = 10
        can_buy, message = can_purchase_item(test_player, "steel_sword")
        assert can_buy is False
        assert "недостаточно золота" in message.lower()

    def test_can_purchase_item_success(self, test_player):
        """Тест успешной проверки возможности покупки."""
        test_player.gold = 100
        can_buy, message = can_purchase_item(test_player, "steel_sword")
        assert can_buy is True
        assert message == ""

    def test_purchase_item_weapon(self, test_player):
        """Тест покупки оружия."""
        test_player.gold = 100
        old_power = test_player.power

        success, message = purchase_item(test_player, "steel_sword")

        assert success is True
        assert "купили" in message.lower()
        assert test_player.gold < 100
        assert test_player.power > old_power
        assert "Стальной меч" in test_player.inventory

    def test_purchase_item_armor(self, test_player):
        """Тест покупки брони."""
        test_player.gold = 100
        old_max_hp = test_player.max_hp

        success, message = purchase_item(test_player, "leather_armor")

        assert success is True
        assert "купили" in message.lower()
        assert test_player.max_hp > old_max_hp
        assert "Кожаная броня" in test_player.inventory

    def test_purchase_spell_low_level(self, test_player):
        """Тест покупки заклинания при низком уровне."""
        test_player.level = 1
        test_player.gold = 200

        can_buy, message = can_purchase_item(test_player, "fireball")

        assert can_buy is False
        assert "требуется" in message.lower()

    def test_purchase_spell_success(self, test_player):
        """Тест успешной покупки заклинания."""
        test_player.level = 5
        test_player.gold = 200

        success, message = purchase_item(test_player, "fireball")

        assert success is True
        assert "изучили" in message.lower()
        assert "⚡ Огненный шар" in test_player.spells

    def test_purchase_potion(self, test_player):
        """Тест покупки зелья."""
        test_player.gold = 100

        success, message = purchase_item(test_player, "health_potion")

        assert success is True
        assert test_player.potions.get("health_potion", 0) == 1

        # Покупаем ещё одно
        success, message = purchase_item(test_player, "health_potion")
        assert success is True
        assert test_player.potions["health_potion"] == 2


class TestEquipment:
    """Тесты экипировки."""

    def test_equip_item_not_in_inventory(self, test_player):
        """Тест экипировки предмета, которого нет в инвентаре."""
        success, message = equip_item(test_player, "Несуществующий меч")
        assert success is False
        assert "нет этого предмета" in message.lower()

    def test_equip_weapon(self, test_player):
        """Тест экипировки оружия."""
        test_player.inventory.append("Стальной меч")

        success, message = equip_item(test_player, "Стальной меч")

        assert success is True
        assert "экипировали" in message.lower()
        assert test_player.equipment.weapon == "Стальной меч"
        assert "Стальной меч" not in test_player.inventory

    def test_equip_armor(self, test_player):
        """Тест экипировки брони."""
        test_player.inventory.append("Кожаная броня")

        success, message = equip_item(test_player, "Кожаная броня")

        assert success is True
        assert "экипировали" in message.lower()
        assert test_player.equipment.armor == "Кожаная броня"
        assert "Кожаная броня" not in test_player.inventory

    def test_equip_replace_weapon(self, test_player):
        """Тест замены экипированного оружия."""
        test_player.inventory.append("Стальной меч")
        test_player.equipment.weapon = "Деревянная палка"

        success, message = equip_item(test_player, "Стальной меч")

        assert success is True
        assert test_player.equipment.weapon == "Стальной меч"
        assert "Деревянная палка" in test_player.inventory
        assert "Стальной меч" not in test_player.inventory

    def test_get_item_by_name(self):
        """Тест поиска предмета по названию."""
        item = get_item_by_name("Стальной меч")
        assert item is not None
        assert item.name == "Стальной меч"
        assert item.item_type == ItemType.WEAPON

        item = get_item_by_name("Несуществующий предмет")
        assert item is None
