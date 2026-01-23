"""Интеграционные тесты."""
import pytest
from datetime import datetime
from models import Player, StoryProgress
from game_logic.battle import simulate_battle, apply_battle_result, select_monster_for_location
from game_logic.magic import cast_spell
from game_logic.quests import increment_kills
from game_logic.achievements import check_and_award
from data import MONSTER_TEMPLATES


class TestBattleExperienceIntegration:
    """Интеграционные тесты боя и опыта."""

    def test_complete_battle_flow(self, test_player):
        """Полный цикл боя."""
        test_player.hp = 100
        test_player.power = 20
        test_player.gold = 50
        test_player.exp = 0

        # Создаём монстра
        template = MONSTER_TEMPLATES["goblin"]
        from models import Monster
        monster = Monster.from_template(template)

        # Симулируем бой
        result = simulate_battle(test_player, monster)

        # Проверяем результат
        assert result is not None
        assert isinstance(result.victory, bool)
        assert result.player_hp >= 0

        # Применяем результат
        old_gold = test_player.gold
        old_exp = test_player.exp
        apply_battle_result(test_player, result)

        if result.victory:
            assert test_player.gold >= old_gold
            assert test_player.exp >= old_exp
            assert test_player.total_kills >= 1
        else:
            assert test_player.hp == result.player_hp

    def test_battle_with_achievements(self, test_player):
        """Бой с достижениями."""
        test_player.hp = 100
        test_player.power = 30
        test_player.gold = 50
        test_player.exp = 0
        test_player.total_kills = 0
        test_player.achievements = []

        # Создаём монстра
        template = MONSTER_TEMPLATES["wolf"]
        from models import Monster
        monster = Monster.from_template(template)

        # Симулируем бой
        result = simulate_battle(test_player, monster)
        apply_battle_result(test_player, result)

        # Проверяем достижения
        if result.victory and test_player.total_kills >= 1:
            message, new_achievements = check_and_award(test_player, "Бой завершён")
            # Могло выдать достижение "Первая кровь"
            assert isinstance(message, str)
            assert isinstance(new_achievements, list)

    def test_quest_progression_through_battles(self, test_player):
        """Прогресс квеста через бои."""
        from models import DailyQuest

        test_player.hp = 100
        test_player.power = 25
        test_player.quests = {
            "daily": DailyQuest(
                date=datetime.now().strftime("%Y-%m-%d"),
                kills=0,
                target=5,
                reward_claimed=False
            )
        }

        # Проводим несколько боёв
        for _ in range(3):
            template = MONSTER_TEMPLATES["goblin"]
            from models import Monster
            monster = Monster.from_template(template)

            result = simulate_battle(test_player, monster)
            apply_battle_result(test_player, result)

            if result.victory:
                increment_kills(test_player, 1)

        # Проверяем прогресс квеста
        assert test_player.quests["daily"].kills > 0


class TestMagicBattleIntegration:
    """Интеграционные тесты магии и боя."""

    def test_spell_usage_in_battle(self, player_with_spells, test_battle_state):
        """Использование заклинания в бою."""
        initial_mana = player_with_spells.mana
        initial_monster_hp = test_battle_state.monster_hp

        # Применяем заклинание
        success, message, damage = cast_spell(
            player_with_spells,
            "fireball",
            test_battle_state
        )

        # Проверяем эффект
        if success:
            assert player_with_spells.mana < initial_mana
            assert test_battle_state.monster_hp < initial_monster_hp


class TestServiceIntegration:
    """Интеграционные тесты сервисов."""

    def test_player_service_full_lifecycle(self, fresh_player_service):
        """Полный жизненный цикл игрока через сервис."""
        user_id = 9999

        # Создаём игрока
        player = fresh_player_service.get_or_create(user_id)
        assert player.user_id == user_id
        assert player.level == 1

        # Обновляем игрока
        player = fresh_player_service.update_player(
            user_id,
            level=5,
            gold=500,
            power=30
        )
        assert player.level == 5
        assert player.gold == 500

        # Проверяем сохранение
        data = fresh_player_service.repository.get_player_data(user_id)
        assert data["level"] == 5
        assert data["gold"] == 500

        # Проверяем в топе
        top = fresh_player_service.get_top_players()
        assert len(top) > 0
