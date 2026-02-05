"""Система случайных событий и встреч."""
from dataclasses import dataclass
from typing import Optional
import random


@dataclass
class RandomEvent:
    """Случайное событие."""
    event_id: str
    title: str
    description: str
    probability: float  # 0.0 - 1.0 (шанс срабатывания)
    min_level: int
    max_level: int
    location: Optional[str] = None  # None = любая локация
    choices: list[tuple[str, dict]] = None  # (текст, {effect_type: value})

    def __post_init__(self):
        if self.choices is None:
            self.choices = []


# ============= СЛУЧАЙНЫЕ СОБЫТИЯ =============

RANDOM_EVENTS = {
    # === Позитивные события ===
    "treasure_chest": RandomEvent(
        event_id="treasure_chest",
        title="💎 Неожиданная находка",
        description=(
            "🗺️ Блуждая по локации, вы замечаете что-то блестящее под камнем.\n"
            "Подойдя ближе, вы находите старый сундук!\n\n"
            "Внутри вас ждёт сюрприз..."
        ),
        probability=0.15,
        min_level=1,
        max_level=100,
        choices=[
            ("🔓 Открыть сундук", {"gold": (50, 200), "exp": (25, 100)}),
            ("🚶 Пройти мимо", {"nothing": True})
        ]
    ),

    "mysterious_merchant": RandomEvent(
        event_id="mysterious_merchant",
        title="🎭 Странный торговец",
        description=(
            "🌟 Из тумана появляется загадочная фигура в капюшоне.\n\n"
            "— Приветствую, путник! Ищешь редкие товары?\n"
            "У меня есть кое-что особенное... но только для избранных.\n\n"
            "Торговец раскрывает плащ, показывая сверкающие артефакты."
        ),
        probability=0.08,
        min_level=5,
        max_level=100,
        choices=[
            ("💰 Купить за 500 золота", {"buy_random_item": True, "gold": -500}),
            ("🤝 Попросить скидку (Харизма)", {"discount_item": True, "gold": -250}),
            ("👋 Отказаться", {"nothing": True})
        ]
    ),

    "fairy_blessing": RandomEvent(
        event_id="fairy_blessing",
        title="🧚 Благословение феи",
        description=(
            "✨ Маленькая светящаяся фея кружится вокруг вас!\n\n"
            "— Спасибо, что не разрушаешь природу в своих путешествиях!\n"
            "В награду я дам тебе своё благословение.\n\n"
            "Фея касается вашего лба волшебной палочкой."
        ),
        probability=0.05,
        min_level=1,
        max_level=100,
        choices=[
            ("💖 +50 HP навсегда", {"permanent_hp": 50}),
            ("⚡ +30 Силы навсегда", {"permanent_power": 30}),
            ("✨ +50 Маны навсегда", {"permanent_mana": 50})
        ]
    ),

    "time_warp": RandomEvent(
        event_id="time_warp",
        title="⏰ Временной парадокс",
        description=(
            "🌀 Реальность вокруг начинает искажаться!\n\n"
            "Вы видите себя из будущего, который передаёт вам предмет:\n"
            "— Тебе это понадобится. Поверь мне, я знаю.\n\n"
            "Не успеваете спросить, как ваш двойник исчезает."
        ),
        probability=0.03,
        min_level=10,
        max_level=100,
        choices=[
            ("🎁 Взять предмет", {"future_item": True}),
        ]
    ),

    # === Нейтральные события ===
    "wandering_bard": RandomEvent(
        event_id="wandering_bard",
        title="🎵 Странствующий бард",
        description=(
            "🎸 Вы встречаете весёлого барда, играющего на лютне.\n\n"
            "— О! Герой! Позволь мне сочинить балладу о твоих подвигах!\n"
            "Или... может, хочешь услышать легенды о древних сокровищах?"
        ),
        probability=0.12,
        min_level=1,
        max_level=100,
        choices=[
            ("🎵 Послушать легенду (+подсказка)", {"hint": True}),
            ("💰 Дать 50 золота (+репутация)", {"gold": -50, "reputation": 10}),
            ("👋 Уйти", {"nothing": True})
        ]
    ),

    "mysterious_portal": RandomEvent(
        event_id="mysterious_portal",
        title="🌀 Загадочный портал",
        description=(
            "🔮 Перед вами возникает светящийся портал!\n\n"
            "Из него доносятся странные звуки...\n"
            "Войти? Это может быть опасно... или выгодно."
        ),
        probability=0.07,
        min_level=8,
        max_level=100,
        choices=[
            ("🚪 Войти в портал", {"random_teleport": True}),
            ("🏃 Убежать", {"nothing": True})
        ]
    ),

    # === Негативные события (с юмором) ===
    "banana_peel": RandomEvent(
        event_id="banana_peel",
        title="🍌 Банановая кожура",
        description=(
            "😱 Вы наступаете на банановую кожуру и падаете!\n\n"
            "КАК ОНА ЗДЕСЬ ОКАЗАЛАСЬ?!\n\n"
            "Вы получаете небольшой урон... и урон по самолюбию."
        ),
        probability=0.05,
        min_level=1,
        max_level=100,
        choices=[
            ("😤 Встать", {"damage": 10}),
        ]
    ),

    "sneaky_thief": RandomEvent(
        event_id="sneaky_thief",
        title="🥷 Ловкий воришка",
        description=(
            "👤 Вы чувствуете, как кто-то роется в вашем кармане!\n\n"
            "Оборачиваетесь - и видите убегающую фигуру!\n"
            "Погнаться или забить?"
        ),
        probability=0.06,
        min_level=3,
        max_level=100,
        choices=[
            ("🏃 Погнаться (50% вернуть х2)", {"chase_thief": True}),
            ("😔 Смириться с потерей", {"gold": -100})
        ]
    ),

    # === Очень редкие события ===
    "ancient_spirit": RandomEvent(
        event_id="ancient_spirit",
        title="👻 Древний дух",
        description=(
            "🌙 Призрачная фигура материализуется перед вами.\n\n"
            "— Смертный... Я наблюдал за тобой. Ты достоин.\n"
            "Прими мой дар - частицу моей силы из прошлой эпохи.\n\n"
            "Дух касается вашей груди, и вы чувствуете прилив энергии!"
        ),
        probability=0.01,
        min_level=15,
        max_level=100,
        choices=[
            ("🙏 Принять дар", {"permanent_hp": 100, "permanent_power": 50, "permanent_mana": 100}),
        ]
    ),

    "dragon_egg": RandomEvent(
        event_id="dragon_egg",
        title="🥚 Драконье яйцо",
        description=(
            "🔥 ВЫ НАШЛИ ДРАКОНЬЕ ЯЙЦО!\n\n"
            "Оно тёплое и пульсирует. Внутри что-то шевелится.\n\n"
            "Что делать с ним?"
        ),
        probability=0.005,
        min_level=20,
        max_level=100,
        location="mountain",
        choices=[
            ("🐣 Забрать себе (питомец дракон!)", {"dragon_pet": True}),
            ("💰 Продать (5000 золота)", {"gold": 5000}),
            ("🏔️ Оставить", {"nothing": True})
        ]
    ),

    "lottery_win": RandomEvent(
        event_id="lottery_win",
        title="🎰 ДЖЕКПОТ!",
        description=(
            "🎉 НЕВЕРОЯТНО! ВЫ ВЫИГРАЛИ В ЛОТЕРЕЮ!\n\n"
            "Проходя мимо таверны, вам вручают билет:\n"
            "— Поздравляем! Вы 1000-й посетитель!\n\n"
            "💰 ВЫ ПОЛУЧАЕТЕ 10000 ЗОЛОТА! 💰"
        ),
        probability=0.001,
        min_level=1,
        max_level=100,
        choices=[
            ("🎊 УРААА!", {"gold": 10000, "exp": 500}),
        ]
    ),

    # === Пасхалки ===
    "matrix_reference": RandomEvent(
        event_id="matrix_reference",
        title="💊 Красная или синяя?",
        description=(
            "🕴️ Человек в чёрных очках предлагает вам выбор:\n\n"
            "— Красная таблетка - узнаешь правду о мире.\n"
            "Синяя таблетка - останешься в неведении, но получишь силу.\n\n"
            "Что выберешь?"
        ),
        probability=0.02,
        min_level=10,
        max_level=100,
        choices=[
            ("🔴 Красная (секретная информация)", {"matrix_red": True}),
            ("🔵 Синяя (+100 силы)", {"permanent_power": 100})
        ]
    ),

    "cake_is_a_lie": RandomEvent(
        event_id="cake_is_a_lie",
        title="🎂 Обещанный торт",
        description=(
            "🤖 Вы находите записку:\n\n"
            "'Пройдите испытание, и получите торт.'\n\n"
            "Вы проходите испытание... но торта нет.\n"
            "Только ещё одна записка: 'The cake is a lie.'\n\n"
            "Зато вы получаете достижение!"
        ),
        probability=0.015,
        min_level=5,
        max_level=100,
        choices=[
            ("😢 Где мой торт?!", {"achievement": "cake_is_a_lie", "gold": 300}),
        ]
    ),

    "arrow_to_the_knee": RandomEvent(
        event_id="arrow_to_the_knee",
        title="🏹 Стрела в колено",
        description=(
            "🛡️ Старый стражник останавливает вас:\n\n"
            "— Раньше я был искателем приключений, как ты...\n"
            "Но потом мне прилетела стрела в колено.\n\n"
            "Он показывает шрам и вздыхает."
        ),
        probability=0.03,
        min_level=1,
        max_level=100,
        location="village",
        choices=[
            ("😄 Это классика!", {"exp": 50}),
            ("🤔 Лечить надо было", {"gold": 100})
        ]
    ),

    # === Зловещие события ===
    "ominous_whisper": RandomEvent(
        event_id="ominous_whisper",
        title="👁️ Зловещий шёпот",
        description=(
            "🌑 Вы слышите шёпот в темноте:\n\n"
            "'Ты думаешь, ты герой? Ты всего лишь пешка в большой игре...'\n\n"
            "Шёпот затихает. Вас охватывает беспокойство."
        ),
        probability=0.04,
        min_level=10,
        max_level=100,
        choices=[
            ("😰 Это что было?", {"sanity": -10}),
        ]
    ),
}


def get_random_event(player_level: int, location: str) -> Optional[RandomEvent]:
    """Получить случайное событие."""
    available_events = [
        event for event in RANDOM_EVENTS.values()
        if (event.min_level <= player_level <= event.max_level
            and (event.location is None or event.location == location)
            and random.random() < event.probability)
    ]

    if available_events:
        return random.choice(available_events)
    return None


def apply_event_choice(choice_effect: dict, player) -> str:
    """Применить эффект выбора события."""
    messages = []

    if "gold" in choice_effect:
        gold_range = choice_effect["gold"]
        if isinstance(gold_range, tuple):
            amount = random.randint(gold_range[0], gold_range[1])
            player.gold += amount
            messages.append(f"💰 Получено {amount} золота!")
        else:
            player.gold += gold_range
            if gold_range > 0:
                messages.append(f"💰 Получено {gold_range} золота!")
            else:
                messages.append(f"💸 Потеряно {abs(gold_range)} золота!")

    if "exp" in choice_effect:
        exp_range = choice_effect["exp"]
        if isinstance(exp_range, tuple):
            amount = random.randint(exp_range[0], exp_range[1])
        else:
            amount = exp_range
        player.exp += amount
        messages.append(f"📊 Получено {amount} опыта!")

    if "permanent_hp" in choice_effect:
        amount = choice_effect["permanent_hp"]
        player.max_hp += amount
        player.hp = player.max_hp
        messages.append(f"💖 Максимальное HP увеличено на {amount}!")

    if "permanent_power" in choice_effect:
        amount = choice_effect["permanent_power"]
        player.power += amount
        messages.append(f"⚡ Сила навсегда увеличена на {amount}!")

    if "permanent_mana" in choice_effect:
        amount = choice_effect["permanent_mana"]
        player.max_mana += amount
        player.mana = player.max_mana
        messages.append(f"✨ Максимальная мана увеличена на {amount}!")

    if "damage" in choice_effect:
        amount = choice_effect["damage"]
        player.hp = max(1, player.hp - amount)
        messages.append(f"💔 Получен урон: {amount} HP!")

    if "buy_random_item" in choice_effect:
        # Логика покупки случайного предмета
        if player.gold >= 500:
            rare_items = ["Око Истины", "Сундук капитана", "Святой амулет"]
            item = random.choice(rare_items)
            player.inventory.append(item)
            messages.append(f"🎁 Вы получили: {item}!")
        else:
            messages.append("❌ Недостаточно золота!")

    if "dragon_pet" in choice_effect:
        player.inventory.append("🐉 Драконий питомец")
        messages.append("🐣 Драчкон вылупился! Теперь он ваш верный спутник!")

    if "chase_thief" in choice_effect:
        if random.random() < 0.5:
            amount = 200
            player.gold += amount
            messages.append(f"✅ Вы поймали вора и вернули {amount} золота!")
        else:
            messages.append("❌ Вор сбежал... Потеряно 100 золота.")
            player.gold = max(0, player.gold - 100)

    if "matrix_red" in choice_effect:
        messages.append(
            "🔴 Вы видите код Матрицы... Всё вокруг - цифры.\n"
            "Открыта секретная информация: В файле STORY_FEATURES.md "
            "есть полная документация по всем системам игры!"
        )

    if "nothing" in choice_effect:
        messages.append("Вы продолжаете свой путь.")

    return "\n".join(messages)
