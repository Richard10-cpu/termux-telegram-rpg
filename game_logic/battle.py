"""Логика боя."""
import random
from dataclasses import dataclass
from models import Player, Monster, BattleState
from data import MONSTER_TEMPLATES, LOCATIONS
from data.monsters import BOSS_NAME_TO_KEY


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


def create_boss_monster(boss_name: str) -> Monster | None:
    """Создать монстра-босса по имени."""
    boss_key = BOSS_NAME_TO_KEY.get(boss_name)
    if not boss_key or boss_key not in MONSTER_TEMPLATES:
        return None

    template = MONSTER_TEMPLATES[boss_key]
    return Monster.from_template(template)


# Новые функции для пошагового боя

def create_battle_state(monster: Monster, is_boss: bool = False, is_elite: bool = False) -> BattleState:
    """Создать состояние боя."""
    return BattleState(
        monster_key=monster.key,
        monster_name=monster.name,
        monster_hp=monster.hp,
        monster_max_hp=monster.max_hp,
        monster_power=monster.power,
        monster_exp=monster.exp,
        monster_gold_min=monster.gold_range[0],
        monster_gold_max=monster.gold_range[1],
        is_boss=is_boss,
        is_elite=is_elite
    )


def player_attack(player: Player, state: BattleState) -> tuple[int, bool]:
    """Атака игрока. Возвращает (урон, крит?)."""
    crit = random.random() < 0.15  # 15% шанс крита
    damage = calculate_damage(player.power)
    if crit:
        damage = int(damage * 1.5)
    return damage, crit


def monster_attack(player: Player, state: BattleState) -> tuple[int, bool]:
    """Атака монстра. Возвращает (урон, промах игрока?)."""
    dodge = random.random() < 0.10  # 10% шанс уклонения
    if dodge:
        return 0, True

    damage = calculate_damage(state.monster_power)

    # Если игрок защищается - урон снижается на 50%
    if state.defending:
        damage = damage // 2

    return damage, False


def flee_battle(player: Player) -> bool:
    """Попытка сбежать. Возвращает True если успешно."""
    return random.random() < 0.60  # 60% шанс побега
