"""Побочные квесты с уникальными историями."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SideQuest:
    """Побочный квест."""
    quest_id: str
    title: str
    description: str
    story_text: str  # Развёрнутая история квеста
    required_level: int
    required_chapter: int
    npc_giver: Optional[str]  # Кто даёт квест
    quest_type: str  # "kill", "collect", "explore", "escort"
    target: int  # Сколько нужно выполнить
    target_key: str  # Что нужно (monster_key, item_key, location_key)
    reward_gold: int
    reward_exp: int
    reward_item: Optional[str] = None
    repeatable: bool = False  # Можно ли повторять квест
    hidden: bool = False  # Скрытый квест (не показывается в списке)


# ============= ПОБОЧНЫЕ КВЕСТЫ =============

SIDE_QUESTS: dict[str, SideQuest] = {
    # Квесты начальных уровней
    "lost_cat": SideQuest(
        quest_id="lost_cat",
        title="🐱 Потерянный кот",
        description="Найти кота старушки Марты",
        story_text=(
            "🏘️ Старушка Марта в слезах:\n\n"
            "— Мой Мурзик пропал! Он убежал в Тёмный лес, гоняя мышь. "
            "Там опасно, а он такой маленький! Пожалуйста, найди его!\n\n"
            "Она даёт вам любимое лакомство Мурзика - вяленую рыбку. "
            "Нужно обыскать лес и найти кота."
        ),
        required_level=2,
        required_chapter=1,
        npc_giver="elder",
        quest_type="explore",
        target=1,
        target_key="forest",
        reward_gold=25,
        reward_exp=15,
        repeatable=False
    ),

    "bandits_trouble": SideQuest(
        quest_id="bandits_trouble",
        title="🗡️ Проблема с бандитами",
        description="Зачистить логово бандитов",
        story_text=(
            "👴 Старейшина Эрион обеспокоен:\n\n"
            "— Банда разбойников обосновалась в пещере. "
            "Они грабят караваны и похищают людей. "
            "Нужен смелый воин, который разберётся с ними. "
            "Убей 10 бандитов и верни похищенные товары."
        ),
        required_level=4,
        required_chapter=2,
        npc_giver="elder",
        quest_type="kill",
        target=10,
        target_key="skeleton",
        reward_gold=100,
        reward_exp=75,
        reward_item="Стальной меч",
        repeatable=False
    ),

    "mysterious_artifact": SideQuest(
        quest_id="mysterious_artifact",
        title="🔮 Таинственный артефакт",
        description="Исследовать странный артефакт",
        story_text=(
            "🧙‍♀️ Маг Элария взволнована:\n\n"
            "— Я обнаружила упоминание о древнем артефакте, спрятанном в горах. "
            "Он называется 'Око Истины' и якобы позволяет видеть сквозь иллюзии. "
            "Мне нужен кто-то достаточно сильный, чтобы добраться туда. "
            "Победи 5 драконов на горе и принеси мне любые странные предметы, что найдёшь."
        ),
        required_level=12,
        required_chapter=3,
        npc_giver="mage",
        quest_type="kill",
        target=5,
        target_key="dragon",
        reward_gold=300,
        reward_exp=200,
        reward_item="Око Истины",
        repeatable=False
    ),

    "ghost_ship": SideQuest(
        quest_id="ghost_ship",
        title="👻 Корабль-призрак",
        description="Исследовать затонувший корабль",
        story_text=(
            "⚓ Моряк Коралл рассказывает леге��ду:\n\n"
            "— Видел я корабль-призрак в морской бездне. "
            "Говорят, на нём до сих пор находятся сокровища капитана. "
            "Но охраняют их души утонувших моряков - морские упыри. "
            "Если сможешь победить 15 морских змеев и кракенов, найдёшь обломки корабля.\n\n"
            "Награда того стоит - капитан был очень богат."
        ),
        required_level=18,
        required_chapter=5,
        npc_giver="sailor",
        quest_type="kill",
        target=15,
        target_key="sea_serpent",
        reward_gold=750,
        reward_exp=400,
        reward_item="Сундук капитана",
        repeatable=False
    ),

    "forbidden_knowledge": SideQuest(
        quest_id="forbidden_knowledge",
        title="📚 Запретное знание",
        description="Найти утерянные тома магии",
        story_text=(
            "📚 Учёный Аркадиус ищет древние книги:\n\n"
            "— В руинах империи когда-то была величайшая библиотека. "
            "Большинство книг уничтожено, но некоторые тома всё ещё там. "
            "Мне нужны три книги: Том Пламени, Том Льда и Том Молний. "
            "Их охраняют големы и личи. Победи 20 из них и ищи книги в обломках.\n\n"
            "Взамен я научу тебя древней магии."
        ),
        required_level=23,
        required_chapter=6,
        npc_giver="scholar",
        quest_type="kill",
        target=20,
        target_key="golem",
        reward_gold=1000,
        reward_exp=600,
        reward_item="Книга древней магии",
        repeatable=False
    ),

    "souls_redemption": SideQuest(
        quest_id="souls_redemption",
        title="✝️ Искупление душ",
        description="Освободить заточённые души",
        story_text=(
            "⚔️ Валерия, охотница на демонов, просит о помощи:\n\n"
            "— Демоны не просто убивают - они забирают души своих жертв. "
            "Эти души заточены в кристаллах и мучаются вечно. "
            "Я освободила многих, но мне нужна помощь.\n\n"
            "Уничтожь 25 демонов и адских гончих. В их логове найдёшь кристаллы душ. "
            "Разбей их и освободи невинных.\n\n"
            "Это единственный способ дать им покой."
        ),
        required_level=28,
        required_chapter=7,
        npc_giver="demon_hunter",
        quest_type="kill",
        target=25,
        target_key="demon",
        reward_gold=2000,
        reward_exp=1000,
        reward_item="Святой амулет",
        repeatable=False
    ),

    "echo_of_eternity": SideQuest(
        quest_id="echo_of_eternity",
        title="♾️ Эхо вечности",
        description="Найти осколки реальности",
        story_text=(
            "🔮 Оракул говорит загадками:\n\n"
            "— В Пустоте реальность распадается на осколки. "
            "Каждый осколок - это мир, который мог бы быть. "
            "Сущности Пустоты охраняют эти осколки. "
            "Собери 30 из них, и ты узнаешь правду о происхождении Хаоса.\n\n"
            "Эти знания могут изменить всё. "
            "Или ничего. Время одновременно линейно и цикличнсо здесь."
        ),
        required_level=33,
        required_chapter=8,
        npc_giver="oracle",
        quest_type="kill",
        target=30,
        target_key="void_entity",
        reward_gold=5000,
        reward_exp=2500,
        reward_item="Осколок вечности",
        repeatable=False
    ),

    # Скрытый квест
    "the_shadow_truth": SideQuest(
        quest_id="the_shadow_truth",
        title="🎭 Теневая правда",
        description="Раскрыть тайну Незнакомца",
        story_text=(
            "🎭 Таинственный незнакомец наконец раскрывается:\n\n"
            "— Ты прошёл долгий путь, герой. Пора узнать правду. "
            "Я - тот, кто всё это начал. Тысячу лет назад я расколол Первозданный Хаос, "
            "думая спасти мир. Но этим лишь отсрочил неизбежное.\n\n"
            "Теперь ты повторяешь мой путь. Но у тебя есть шанс закончить правильно. "
            "Если победишь 50 порождений Хаоса, я передам тебе свою силу. "
            "Тогда у тебя будет выбор - исправить мою ошибку или повторить её.\n\n"
            "Выбор всегда был иллюзией. Но делать его всё равно нужно."
        ),
        required_level=35,
        required_chapter=8,
        npc_giver="mysterious_stranger",
        quest_type="kill",
        target=50,
        target_key="chaos_spawn",
        reward_gold=10000,
        reward_exp=5000,
        reward_item="Сила Творца",
        repeatable=False,
        hidden=True
    ),

    # Повторяемые квесты
    "bounty_goblins": SideQuest(
        quest_id="bounty_goblins",
        title="💰 Награда за гоблинов",
        description="Охота на гоблинов (повторяемый)",
        story_text=(
            "🔨 Кузнец Торин предлагает постоянную работу:\n\n"
            "— Гоблины - вечная проблема. Убивай их сколько хочешь, "
            "я плачу за каждого. 5 гоблинов = награда. Просто и выгодно!"
        ),
        required_level=1,
        required_chapter=1,
        npc_giver="blacksmith",
        quest_type="kill",
        target=5,
        target_key="goblin",
        reward_gold=30,
        reward_exp=20,
        repeatable=True
    ),

    "bounty_dragons": SideQuest(
        quest_id="bounty_dragons",
        title="🐉 Охота на драконов",
        description="Охота на драконов (повторяемый)",
        story_text=(
            "🧙‍♀️ Элария нуждается в драконьих чешуйках:\n\n"
            "— Драконья чешуя - ценнейший магический компонент. "
            "Принеси мне доказательство убийства 3 драконов, "
            "и я щедро награжу тебя."
        ),
        required_level=10,
        required_chapter=3,
        npc_giver="mage",
        quest_type="kill",
        target=3,
        target_key="dragon",
        reward_gold=200,
        reward_exp=150,
        repeatable=True
    )
}


def get_side_quest(quest_id: str) -> SideQuest | None:
    """Получить побочный квест по ID."""
    return SIDE_QUESTS.get(quest_id)


def get_available_side_quests(player_level: int, player_chapter: int) -> list[SideQuest]:
    """Получить доступные побочные квесты."""
    return [
        quest for quest in SIDE_QUESTS.values()
        if quest.required_level <= player_level
        and quest.required_chapter <= player_chapter
        and not quest.hidden
    ]


def get_hidden_quests(player_level: int, player_chapter: int) -> list[SideQuest]:
    """Получить скрытые квесты (для особых условий)."""
    return [
        quest for quest in SIDE_QUESTS.values()
        if quest.required_level <= player_level
        and quest.required_chapter <= player_chapter
        and quest.hidden
    ]
