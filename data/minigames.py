"""Мини-игры: казино, арена, рыбалка."""
import random
from dataclasses import dataclass
from typing import Optional


# ============= КАЗИНО =============

def play_slots(bet: int) -> tuple[str, int]:
    """Игровой автомат (слоты)."""
    symbols = ["🍒", "🍋", "🍊", "⭐", "💎", "7️⃣"]
    weights = [30, 25, 20, 15, 8, 2]  # Вероятности

    reels = random.choices(symbols, weights=weights, k=3)
    display = " | ".join(reels)

    # Выигрышные комбинации
    if reels[0] == reels[1] == reels[2]:
        symbol = reels[0]
        multipliers = {
            "🍒": 5,
            "🍋": 10,
            "🍊": 15,
            "⭐": 25,
            "💎": 50,
            "7️⃣": 100
        }
        multiplier = multipliers.get(symbol, 5)
        winnings = bet * multiplier

        return f"🎰 [ {display} ]\n\n🎉 ДЖЕКПОТ! x{multiplier}\n💰 Выигрыш: {winnings} золота!", winnings

    elif reels[0] == reels[1] or reels[1] == reels[2]:
        # Два одинаковых
        winnings = bet * 2
        return f"🎰 [ {display} ]\n\n✨ Пара! x2\n💰 Выигрыш: {winnings} золота!", winnings

    else:
        return f"🎰 [ {display} ]\n\n😔 Проигрыш...\n💸 Потеряно: {bet} золота", -bet


def play_dice(bet: int, guess: int) -> tuple[str, int]:
    """Игра в кости (угадай число 1-6)."""
    if guess < 1 or guess > 6:
        return "❌ Неверное число! Выберите от 1 до 6.", 0

    roll = random.randint(1, 6)

    if roll == guess:
        winnings = bet * 5
        return f"🎲 Выпало: {roll}\n\n🎉 УГАДАЛИ! x5\n💰 Выигрыш: {winnings} золота!", winnings
    else:
        return f"🎲 Выпало: {roll}\n\n😔 Не угадали (ваше: {guess})\n💸 Потеряно: {bet} золота", -bet


def play_roulette(bet: int, bet_type: str, value: Optional[int] = None) -> tuple[str, int]:
    """Рулетка."""
    number = random.randint(0, 36)
    color = "🔴" if number % 2 == 1 else "⚫" if number > 0 else "🟢"

    result = f"🎡 Выпало: {number} {color}\n\n"

    if bet_type == "number" and value == number:
        winnings = bet * 35
        return result + f"🎉 ПРЯМОЕ ПОПАДАНИЕ! x35\n💰 Выигрыш: {winnings} золота!", winnings

    elif bet_type == "color":
        if (value == "red" and color == "🔴") or (value == "black" and color == "⚫"):
            winnings = bet * 2
            return result + f"✅ Цвет угадан! x2\n💰 Выигрыш: {winnings} золота!", winnings

    elif bet_type == "even":
        if number > 0 and number % 2 == 0:
            winnings = bet * 2
            return result + f"✅ Чётное! x2\n💰 Выигрыш: {winnings} золота!", winnings

    elif bet_type == "odd":
        if number % 2 == 1:
            winnings = bet * 2
            return result + f"✅ Нечётное! x2\n💰 Выигрыш: {winnings} золота!", winnings

    return result + f"😔 Проигрыш...\n💸 Потеряно: {bet} золота", -bet


# ============= АРЕНА =============

@dataclass
class ArenaOpponent:
    """Противник на арене."""
    name: str
    level: int
    hp: int
    power: int
    reward_gold: int
    reward_exp: int
    emoji: str


ARENA_OPPONENTS = {
    "novice": ArenaOpponent(
        name="Новичок Боб",
        level=5,
        hp=50,
        power=10,
        reward_gold=100,
        reward_exp=50,
        emoji="🗡️"
    ),
    "warrior": ArenaOpponent(
        name="Воин Гром",
        level=10,
        hp=120,
        power=20,
        reward_gold=300,
        reward_exp=150,
        emoji="⚔️"
    ),
    "champion": ArenaOpponent(
        name="Чемпион Арены",
        level=20,
        hp=300,
        power=40,
        reward_gold=1000,
        reward_exp=500,
        emoji="🏆"
    ),
    "legend": ArenaOpponent(
        name="Легенда Стальная Рука",
        level=30,
        hp=600,
        power=60,
        reward_gold=3000,
        reward_exp=1500,
        emoji="👑"
    ),
    "god": ArenaOpponent(
        name="Бог Войны Арес",
        level=40,
        hp=1200,
        power=90,
        reward_gold=10000,
        reward_exp=5000,
        emoji="⚡"
    )
}


def get_arena_opponent(tier: str) -> Optional[ArenaOpponent]:
    """Получить противника для арены."""
    return ARENA_OPPONENTS.get(tier)


def get_available_arena_opponents(player_level: int) -> list[tuple[str, ArenaOpponent]]:
    """Получить доступных противников."""
    return [
        (key, opp) for key, opp in ARENA_OPPONENTS.items()
        if player_level >= opp.level - 5  # Доступны если ур. игрока не ниже на 5
    ]


# ============= РЫБАЛКА =============

@dataclass
class Fish:
    """Рыба."""
    name: str
    rarity: str  # common, rare, epic, legendary
    value: int  # Цена продажи
    emoji: str
    weight_min: float
    weight_max: float


FISH_TYPES = {
    "carp": Fish("Карп", "common", 10, "🐟", 0.5, 2.0),
    "salmon": Fish("Лосось", "common", 25, "🐠", 1.0, 3.0),
    "tuna": Fish("Тунец", "rare", 50, "🐡", 2.0, 5.0),
    "swordfish": Fish("Меч-рыба", "rare", 100, "🗡️🐟", 5.0, 15.0),
    "shark": Fish("Акула", "epic", 300, "🦈", 20.0, 50.0),
    "whale": Fish("Кит", "epic", 500, "🐋", 100.0, 300.0),
    "kraken": Fish("Кракен", "legendary", 2000, "🦑", 500.0, 1000.0),
    "sea_dragon": Fish("Морской дракон", "legendary", 5000, "🐉", 1000.0, 2000.0),
    "boot": Fish("Старый ботинок", "trash", 1, "👢", 0.1, 0.5),
    "treasure": Fish("Сундук с сокровищами", "legendary", 10000, "💎", 10.0, 20.0),
}


def go_fishing() -> tuple[str, int, Optional[str]]:
    """Порыбачить."""
    # Вероятности поимки
    chances = {
        "trash": 0.15,
        "common": 0.50,
        "rare": 0.25,
        "epic": 0.08,
        "legendary": 0.02
    }

    rarity = random.choices(
        list(chances.keys()),
        weights=list(chances.values())
    )[0]

    # Выбрать рыбу подходящей редкости
    fish_pool = [f for f in FISH_TYPES.values() if f.rarity == rarity]
    fish = random.choice(fish_pool)

    weight = round(random.uniform(fish.weight_min, fish.weight_max), 2)
    value = int(fish.value * (1 + weight / 10))  # Цена зависит от веса

    rarity_text = {
        "trash": "🗑️ Мусор",
        "common": "⚪ Обычная",
        "rare": "🔵 Редкая",
        "epic": "🟣 Эпическая",
        "legendary": "🟡 ЛЕГЕНДАРНАЯ"
    }

    msg = (
        f"🎣 Клюёт!\n\n"
        f"{fish.emoji} {fish.name}\n"
        f"Редкость: {rarity_text.get(rarity, '')}\n"
        f"Вес: {weight} кг\n"
        f"💰 Стоимость: {value} золота"
    )

    # Шанс найти особый предмет
    special_item = None
    if rarity == "legendary" and random.random() < 0.5:
        special_items = ["Жемчужина океана", "Коралловый амулет", "Морская звезда"]
        special_item = random.choice(special_items)
        msg += f"\n\n✨ Бонус: {special_item}!"

    return msg, value, special_item


# ============= BLACKJACK =============

def blackjack_deal() -> list[int]:
    """Раздать две карты."""
    return [random.randint(1, 11), random.randint(1, 11)]


def blackjack_hit() -> int:
    """Взять ещё карту."""
    return random.randint(1, 11)


def blackjack_calculate(cards: list[int]) -> int:
    """Подсчитать очки."""
    total = sum(cards)
    # Если туз (11) даёт перебор, считаем его за 1
    aces = cards.count(11)
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total


def play_blackjack_round(player_cards: list[int], dealer_cards: list[int], bet: int) -> tuple[str, int]:
    """Раунд блэкджека."""
    player_score = blackjack_calculate(player_cards)
    dealer_score = blackjack_calculate(dealer_cards)

    result = f"🃏 Ваши карты: {player_cards} = {player_score}\n"
    result += f"🎴 Карты дилера: {dealer_cards} = {dealer_score}\n\n"

    if player_score > 21:
        return result + f"💥 Перебор! Вы проиграли.\n💸 Потеряно: {bet} золота", -bet

    if dealer_score > 21:
        winnings = bet * 2
        return result + f"🎉 Дилер перебрал! Вы выиграли!\n💰 Выигрыш: {winnings} золота", winnings

    if player_score == 21:
        winnings = bet * 3
        return result + f"🎊 BLACKJACK! x3\n💰 Выигрыш: {winnings} золота", winnings

    if player_score > dealer_score:
        winnings = bet * 2
        return result + f"✅ Вы выиграли!\n💰 Выигрыш: {winnings} золота", winnings

    elif player_score == dealer_score:
        return result + f"🤝 Ничья! Ставка возвращена.", 0

    else:
        return result + f"😔 Дилер выиграл.\n💸 Потеряно: {bet} золота", -bet


# ============= COINFLIP =============

def play_coinflip(bet: int, choice: str) -> tuple[str, int]:
    """Подбрасывание монеты."""
    result = random.choice(["heads", "tails"])
    result_emoji = "👑" if result == "heads" else "⚙️"
    choice_text = "Орёл" if choice == "heads" else "Решка"
    result_text = "Орёл" if result == "heads" else "Решка"

    msg = f"🪙 Подбрасываем монету...\n\n"
    msg += f"Ваш выбор: {choice_text}\n"
    msg += f"Выпало: {result_emoji} {result_text}\n\n"

    if choice == result:
        winnings = bet * 2
        return msg + f"🎉 Угадали! x2\n💰 Выигрыш: {winnings} золота!", winnings
    else:
        return msg + f"😔 Не угадали...\n💸 Потеряно: {bet} золота", -bet
