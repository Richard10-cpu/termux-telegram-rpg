"""Тесты для системы магии."""
import pytest
from models import Player, BattleState
from game_logic.magic import (
    get_spell_by_key,
    get_spell_by_name,
    cast_spell,
    use_potion
)


class TestSpellRetrieval:
    """Тесты получения заклинаний."""

    def test_get_spell_by_key_exists(self):
        """Получение существующего заклинания по ключу."""
        spell = get_spell_by_key("fireball")
        assert spell is not None
        assert spell.name == "⚡ Огненный шар"
        assert spell.spell_damage > 0

    def test_get_spell_by_key_not_exists(self):
        """Получение несуществующего заклинания."""
        spell = get_spell_by_key("nonexistent_spell")
        assert spell is None

    def test_get_spell_by_key_not_spell(self):
        """Получение предмета, не являющегося заклинанием."""
        item = get_spell_by_key("wooden_sword")
        assert item is None  # Не заклинание

    def test_get_spell_by_name_exists(self):
        """Получение заклинания по названию."""
        spell = get_spell_by_name("⚡ Огненный шар")
        assert spell is not None
        assert spell.mana_cost > 0

    def test_get_spell_by_name_not_exists(self):
        """Получение несуществующего заклинания по названию."""
        spell = get_spell_by_name("Несуществующее заклинание")
        assert spell is None

    def test_get_spell_by_name_not_spell(self):
        """Получение не-заклинания по названию."""
        item = get_spell_by_name("Деревянная палка")
        assert item is None  # Не заклинание


class TestCastSpell:
    """Тесты применения заклинаний."""

    def test_cast_spell_not_found(self, test_player, test_battle_state):
        """Применение несуществующего заклинания."""
        success, message, damage = cast_spell(test_player, "fake_spell", test_battle_state)
        assert success is False
        assert "не найдено" in message.lower()
        assert damage == 0

    def test_cast_spell_not_learned(self, test_player, test_battle_state):
        """Применение неизученного заклинания."""
        success, message, damage = cast_spell(test_player, "fireball", test_battle_state)
        assert success is False
        assert "не изучали" in message.lower()
        assert damage == 0

    def test_cast_spell_not_enough_mana(self, player_with_spells, test_battle_state):
        """Применение с недостатком маны."""
        player_with_spells.mana = 5  # Мало маны для заклинания
        success, message, damage = cast_spell(player_with_spells, "fireball", test_battle_state)
        assert success is False
        assert "Недостаточно маны" in message
        assert damage == 0

    def test_cast_damage_spell_success(self, player_with_spells, test_battle_state):
        """Успешное применение уронного заклинания."""
        initial_hp = test_battle_state.monster_hp
        success, message, damage = cast_spell(player_with_spells, "fireball", test_battle_state)

        assert success is True
        assert damage > 0
        assert test_battle_state.monster_hp < initial_hp
        assert player_with_spells.mana < 50  # Мана уменьшилась

    def test_cast_heal_spell_success(self, player_with_spells, test_battle_state):
        """Успешное применение лечебного заклинания."""
        player_with_spells.hp = 50
        player_with_spells.max_hp = 100
        player_with_spells.spells = ["✨ Исцеление"]

        initial_hp = player_with_spells.hp
        success, message, damage = cast_spell(player_with_spells, "heal", test_battle_state)

        assert success is True
        assert player_with_spells.hp > initial_hp
        assert damage == 0

    def test_cast_heal_when_full_hp(self, player_with_spells, test_battle_state):
        """Лечение при полном HP."""
        player_with_spells.hp = 100
        player_with_spells.max_hp = 100
        player_with_spells.spells = ["✨ Исцеление"]

        success, message, damage = cast_spell(player_with_spells, "heal", test_battle_state)

        assert success is True
        assert player_with_spells.hp == 100  # HP не превышает максимум


class TestUsePotion:
    """Тесты использования зелий."""

    def test_use_health_potion_success(self, test_player):
        """Использование зелья здоровья."""
        test_player.hp = 50
        test_player.max_hp = 100
        test_player.potions = {"health_potion": 2}

        success, message = use_potion(test_player, "health_potion")

        assert success is True
        assert test_player.hp > 50
        assert test_player.potions["health_potion"] == 1

    def test_use_health_potion_partial_heal(self, test_player):
        """Зелье здоровья при частичном восстановлении."""
        test_player.hp = 80
        test_player.max_hp = 100
        test_player.potions = {"health_potion": 1}

        success, message = use_potion(test_player, "health_potion")

        assert success is True
        assert test_player.hp == 100  # Полное восстановление
        assert test_player.potions["health_potion"] == 0

    def test_use_mana_potion_success(self, test_player):
        """Использование зелья маны."""
        test_player.mana = 10
        test_player.max_mana = 50
        test_player.potions = {"mana_potion": 1}

        success, message = use_potion(test_player, "mana_potion")

        assert success is True
        assert test_player.mana > 10
        assert test_player.potions["mana_potion"] == 0

    def test_use_power_potion(self, test_player):
        """Использование зелья силы."""
        test_player.potions = {"power_potion": 1}

        success, message = use_potion(test_player, "power_potion")

        assert success is True
        assert "Зелье силы" in message
        assert test_player.potions["power_potion"] == 0

    def test_use_potion_not_have(self, test_player):
        """Использование отсутствующего зелья."""
        test_player.potions = {}

        success, message = use_potion(test_player, "health_potion")

        assert success is False
        assert "нет этого зелья" in message.lower()

    def test_use_potion_not_exists(self, test_player):
        """Использование несуществующего зелья."""
        test_player.potions = {"fake_potion": 1}

        success, message = use_potion(test_player, "fake_potion")

        assert success is False
        assert "не найдено" in message.lower()
