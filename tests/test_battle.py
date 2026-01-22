"""Тесты игровой логики боя."""
import pytest
from game_logic.battle import (
    calculate_damage, simulate_battle, apply_battle_result,
    create_battle_state, player_attack, monster_attack, flee_battle,
    select_monster_for_location, BattleResult
)
from models import Player, Monster, MonsterTemplate


class TestBattleDamage:
    """Тесты расчёта урона."""

    def test_calculate_damage(self):
        """Тест расчёта урона."""
        power = 20
        damage = calculate_damage(power)
        assert damage >= power // 2
        assert damage <= power

    def test_calculate_damage_range(self):
        """Тест диапазона урона."""
        power = 100
        damages = [calculate_damage(power) for _ in range(100)]
        assert all(50 <= d <= 100 for d in damages)
        assert min(damages) >= 50
        assert max(damages) <= 100


class TestBattleSimulation:
    """Тесты симуляции боя."""

    def test_simulate_battle_victory(self):
        """Тест победы в бою."""
        player = Player(
            user_id=1,
            hp=100,
            max_hp=100,
            power=50,  # Сильный игрок
            gold=20
        )
        template = MonsterTemplate(
            key="weak_slime",
            name="Слабый слайм",
            hp=10,
            power=1,
            exp=5,
            gold_min=5,
            gold_max=10,
            min_level=1,
            max_level=5
        )
        monster = Monster.from_template(template)

        result = simulate_battle(player, monster)
        assert result.victory is True
        assert result.gold_earned > 0
        assert result.exp_earned == 5
        assert result.player_hp > 0

    def test_simulate_battle_defeat(self):
        """Тест поражения в бою."""
        player = Player(
            user_id=1,
            hp=10,
            max_hp=100,
            power=1,  # Слабый игрок
            gold=100
        )
        template = MonsterTemplate(
            key="strong_dragon",
            name="Сильный дракон",
            hp=500,
            power=100,
            exp=200,
            gold_min=100,
            gold_max=200,
            min_level=10,
            max_level=20
        )
        monster = Monster.from_template(template)

        result = simulate_battle(player, monster)
        assert result.victory is False
        assert result.player_hp == 1
        assert result.gold_lost > 0
        assert result.gold_lost <= 50  # Не больше половины или 20

    def test_apply_battle_result_victory(self, test_player, test_monster):
        """Тест применения результата победы."""
        initial_gold = test_player.gold
        initial_exp = test_player.exp
        initial_kills = test_player.total_kills

        result = BattleResult(
            victory=True,
            player_hp=80,
            gold_earned=15,
            exp_earned=20
        )

        apply_battle_result(test_player, result)

        assert test_player.hp == 80
        assert test_player.gold == initial_gold + 15
        assert test_player.exp == initial_exp + 20
        assert test_player.total_kills == initial_kills + 1

    def test_apply_battle_result_defeat(self, test_player):
        """Тест применения результата поражения."""
        initial_gold = test_player.gold
        initial_kills = test_player.total_kills

        result = BattleResult(
            victory=False,
            player_hp=1,
            gold_lost=10
        )

        apply_battle_result(test_player, result)

        assert test_player.hp == 1
        assert test_player.gold == initial_gold - 10
        assert test_player.total_kills == initial_kills  # Не увеличивается


class TestStepByStepBattle:
    """Тесты пошагового боя."""

    def test_create_battle_state(self, test_monster):
        """Тест создания состояния боя."""
        state = create_battle_state(test_monster)
        assert state.monster_name == test_monster.name
        assert state.monster_hp == test_monster.hp
        assert state.turn == 1
        assert not state.is_boss

    def test_create_battle_state_boss(self, test_monster):
        """Тест создания состояния боя с боссом."""
        state = create_battle_state(test_monster, is_boss=True)
        assert state.is_boss is True
        assert not state.is_elite

    def test_player_attack_normal(self, test_player, test_battle_state):
        """Тест обычной атаки игрока."""
        damage, crit = player_attack(test_player, test_battle_state)
        assert damage >= test_player.power // 2
        if not crit:
            assert damage <= test_player.power
        else:
            assert damage <= int(test_player.power * 1.5)

    def test_monster_attack_normal(self, test_player, test_battle_state):
        """Тест обычной атаки монстра."""
        test_battle_state.defending = False
        damage, dodged = monster_attack(test_player, test_battle_state)
        if not dodged:
            assert damage >= test_battle_state.monster_power // 2
            assert damage <= test_battle_state.monster_power

    def test_monster_attack_defending(self, test_player, test_battle_state):
        """Тест атаки монстра при защите игрока."""
        test_battle_state.defending = True
        damages = []
        for _ in range(50):
            damage, dodged = monster_attack(test_player, test_battle_state)
            if not dodged and damage > 0:
                damages.append(damage)

        if damages:  # Если были попадания
            assert all(d <= test_battle_state.monster_power // 2 for d in damages)

    def test_flee_battle(self, test_player):
        """Тест попытки побега."""
        successes = sum(flee_battle(test_player) for _ in range(100))
        # Проверяем что шанс побега примерно 60%
        assert 40 <= successes <= 80  # Допускаем отклонение


class TestMonsterSelection:
    """Тесты выбора монстров."""

    def test_select_monster_for_location(self):
        """Тест выбора монстра для локации."""
        # Этот тест требует наличия данных в LOCATIONS и MONSTER_TEMPLATES
        monster = select_monster_for_location("forest", player_level=1)
        if monster:  # Если в локации есть враги
            assert isinstance(monster, Monster)
            assert monster.hp > 0

    def test_select_monster_no_enemies(self):
        """Тест выбора монстра в локации без врагов."""
        monster = select_monster_for_location("village", player_level=1)
        assert monster is None  # В деревне нет врагов


class TestBattleResult:
    """Тесты результата боя."""

    def test_battle_result_victory_message(self):
        """Тест сообщения о победе."""
        result = BattleResult(
            victory=True,
            player_hp=75,
            gold_earned=25,
            exp_earned=30,
            log="⚔️ Эпический бой!\n"
        )
        message = result.message
        assert "победили" in message.lower()
        assert "25" in message
        assert "30" in message

    def test_battle_result_defeat_message(self):
        """Тест сообщения о поражении."""
        result = BattleResult(
            victory=False,
            player_hp=1,
            gold_lost=15,
            log="💀 Тяжёлый бой...\n"
        )
        message = result.message
        assert "проиграли" in message.lower()
        assert "15" in message
