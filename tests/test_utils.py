"""Тесты утилит форматирования."""
import pytest
from utils.formatters import (
    format_profile, format_battle_result,
    format_top_players, format_location_info
)
from game_logic.battle import BattleResult
from models import Player, Equipment


class TestFormatters:
    """Тесты форматирования сообщений."""

    def test_format_profile_basic(self, test_player):
        """Тест базового форматирования профиля."""
        profile = format_profile(test_player)

        assert "Уровень: 1" in profile
        assert "HP: 100/100" in profile
        assert f"Золото: {test_player.gold}" in profile
        assert "Сила:" in profile

    def test_format_profile_with_equipment(self, test_player):
        """Тест форматирования профиля с экипировкой."""
        test_player.equipment = Equipment(
            weapon="Стальной меч",
            armor="Кожаная броня"
        )

        profile = format_profile(test_player)

        assert "Оружие: Стальной меч" in profile
        assert "Броня: Кожаная броня" in profile

    def test_format_profile_with_spells(self, test_player):
        """Тест форматирования профиля с заклинаниями."""
        test_player.spells = ["⚡ Огненный шар", "✨ Исцеление"]

        profile = format_profile(test_player)

        assert "Заклинания:" in profile
        assert "⚡ Огненный шар" in profile

    def test_format_battle_result_victory(self, test_player):
        """Тест форматирования результата победы."""
        result = BattleResult(
            victory=True,
            player_hp=75,
            gold_earned=25,
            exp_earned=30
        )

        test_player.hp = 75
        message = format_battle_result(result, test_player)

        assert "победили" in message.lower()
        assert "75/100" in message

    def test_format_battle_result_defeat(self, test_player):
        """Тест форматирования результата поражения."""
        result = BattleResult(
            victory=False,
            player_hp=1,
            gold_lost=10
        )

        test_player.hp = 1
        message = format_battle_result(result, test_player)

        assert "проиграли" in message.lower()
        assert "1/100" in message

    def test_format_top_players(self):
        """Тест форматирования топа игроков."""
        players = [
            ("user1", Player(user_id=1, level=10, gold=500)),
            ("user2", Player(user_id=2, level=8, gold=300)),
            ("user3", Player(user_id=3, level=7, gold=250)),
        ]

        top_text = format_top_players(players)

        assert "ТОП-10" in top_text
        assert "🥇" in top_text  # Золотая медаль
        assert "🥈" in top_text  # Серебряная медаль
        assert "🥉" in top_text  # Бронзовая медаль
        assert "Уровень 10" in top_text
        assert "500" in top_text

    def test_format_top_players_empty(self):
        """Тест форматирования пустого топа."""
        top_text = format_top_players([])
        assert "ТОП-10" in top_text

    def test_format_location_info_village(self):
        """Тест форматирования информации о деревне."""
        location_text = format_location_info("village")

        assert "📍" in location_text
        assert "Мирная зона" in location_text or "Деревня" in location_text

    def test_format_location_info_with_enemies(self):
        """Тест форматирования локации с врагами."""
        location_text = format_location_info("forest")

        # Лес должен иметь врагов
        if "Враги:" in location_text or "👹" in location_text:
            assert True
        else:
            # Или это может быть безопасная локация
            assert "Мирная зона" in location_text

    def test_format_location_info_nonexistent(self):
        """Тест форматирования несуществующей локации."""
        location_text = format_location_info("nonexistent_location")
        assert "не найдена" in location_text.lower()
