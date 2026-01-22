"""Логика боя."""
import random
from dataclasses import dataclass
from models import Player, Monster
from data import MONSTER_TEMPLATES, LOCATIONS


@dataclass
class BattleResult:
    """Результат боя."""
    victory: bool
    player_hp: int
    gold_earned: int = 0
    exp_earned: int = 0
    gold_lost: int = 0
    log: str = ""

    @property
    def message(self) -> str:
        """Сформировать сообщение о результате боя."""
        if self.victory:
            msg = f"🎉 {self.log}Вы победили!\n"
            msg += f"💰 Найдено золота: {self.gold_earned}\n"
            msg += f"📊 Получено опыта: {self.exp_earned}"
            return msg
        else:
            msg = f"💀 {self.log}Вы проиграли...\n"
            msg += f"💸 Потеряно золота: {self.gold_lost}\n"
            msg += "💡 Отдохните и попробуйте снова!"
            return msg


def calculate_damage(power: int) -> int:
    """Рассчитать урон."""
    return random.randint(power // 2, power)


def select_monster_for_location(location_key: str, player_level: int) -> Monster | None:
    """Выбрать монстра для локации с учётом уровня игрока."""
    location = LOCATIONS.get(location_key)
    if not location or not location.has_enemies:
        return None

    # Фильтруем монстров по уровню
    available_monsters = [
        MONSTER_TEMPLATES[key]
        for key in location.enemies
        if key in MONSTER_TEMPLATES and MONSTER_TEMPLATES[key].is_available_for_level(player_level)
    ]

    if not available_monsters:
        return None

    template = random.choice(available_monsters)
    return Monster.from_template(template)


def simulate_battle(player: Player, monster: Monster) -> BattleResult:
    """Симулировать бой."""
    player_hp = player.hp
    player_gold = player.gold  # Сохраняем текущее золото
    enemy_hp = monster.hp

    log = f"⚔️ Бой с {monster.name}!\n"

    while player_hp > 0 and enemy_hp > 0:
        # Удар игрока
        player_damage = calculate_damage(player.power)
        enemy_hp -= player_damage
        if enemy_hp <= 0:
            break

        # Удар врага
        enemy_damage = calculate_damage(monster.power)
        player_hp -= enemy_damage

    victory = player_hp > 0

    if victory:
        gold_earned = random.randint(monster.gold_range[0], monster.gold_range[1])
        return BattleResult(
            victory=True,
            player_hp=player_hp,
            gold_earned=gold_earned,
            exp_earned=monster.exp,
            log=log
        )
    else:
        gold_lost = min(player_gold // 2, 20)
        return BattleResult(
            victory=False,
            player_hp=1,
            gold_lost=gold_lost,
            log=log
        )


def apply_battle_result(player: Player, result: BattleResult) -> None:
    """Применить результат боя к игроку."""
    player.hp = result.player_hp

    if result.victory:
        player.gold += result.gold_earned
        player.exp += result.exp_earned
        player.total_kills += 1
    else:
        player.gold -= result.gold_lost
