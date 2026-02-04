"""Данные NPC и диалогов."""
from models.npc import NPC, NPCType, Dialogue, DialogueChoice, DialogueChoiceEffect

# ============= NPC ПЕРСОНАЖИ =============

NPCS: dict[str, NPC] = {
    "elder": NPC(
        key="elder",
        name="Старейшина Эрион",
        npc_type=NPCType.STORY,
        location="village",
        description="Мудрый старейшина деревни, хранитель древних знаний.",
        first_dialogue_id="elder_intro",
        emoji="👴",
        available_from_chapter=1
    ),
    "blacksmith": NPC(
        key="blacksmith",
        name="Кузнец Торин",
        npc_type=NPCType.MERCHANT,
        location="village",
        description="Опытный кузнец, мастер своего дела.",
        first_dialogue_id="blacksmith_intro",
        emoji="🔨",
        available_from_chapter=1
    ),
    "mage": NPC(
        key="mage",
        name="Маг Элария",
        npc_type=NPCType.STORY,
        location="village",
        description="Загадочная волшебница, изучающая древнюю магию.",
        first_dialogue_id="mage_intro",
        emoji="🧙‍♀️",
        available_from_chapter=3
    ),
    "sailor": NPC(
        key="sailor",
        name="Моряк Коралл",
        npc_type=NPCType.STORY,
        location="abyss",
        description="Старый моряк, переживший встречу с Левиафаном.",
        first_dialogue_id="sailor_intro",
        emoji="⚓",
        available_from_chapter=5
    ),
    "scholar": NPC(
        key="scholar",
        name="Учёный Аркадиус",
        npc_type=NPCType.STORY,
        location="ruins",
        description="Археолог, исследующий руины древней империи.",
        first_dialogue_id="scholar_intro",
        emoji="📚",
        available_from_chapter=6
    ),
    "demon_hunter": NPC(
        key="demon_hunter",
        name="Охотница на демонов Валерия",
        npc_type=NPCType.COMPANION,
        location="hell",
        description="Легендарная воительница, посвятившая жизнь борьбе со злом.",
        first_dialogue_id="hunter_intro",
        emoji="⚔️",
        available_from_chapter=7
    ),
    "oracle": NPC(
        key="oracle",
        name="Оракул",
        npc_type=NPCType.STORY,
        location="void",
        description="Древняя сущность, знающая прошлое и будущее.",
        first_dialogue_id="oracle_intro",
        emoji="🔮",
        available_from_chapter=8
    ),
    "mysterious_stranger": NPC(
        key="mysterious_stranger",
        name="Таинственный незнакомец",
        npc_type=NPCType.QUEST_GIVER,
        location="forest",
        description="Фигура в тёмном плаще, появляющаяся в лесу.",
        first_dialogue_id="stranger_intro",
        emoji="🎭",
        available_from_chapter=2
    )
}

# ============= ДИАЛОГИ =============

DIALOGUES: dict[str, Dialogue] = {
    # === Старейшина Эрион ===
    "elder_intro": Dialogue(
        dialogue_id="elder_intro",
        npc_key="elder",
        text=(
            "👴 *Старейшина Эрион смотрит на вас усталыми глазами*\n\n"
            "— Приветствую тебя, путник. Я Эрион, старейшина этой деревни. "
            "Видел я многое за свою долгую жизнь, но то, что происходит сейчас... "
            "Тьма пробуждается, и нам нужен герой.\n\n"
            "Скажи, готов ли ты встать на защиту этих земель?"
        ),
        choices=[
            DialogueChoice(
                text="⚔️ Я готов сражаться!",
                next_dialogue_id="elder_hero_path",
                effect=DialogueChoiceEffect.CHANGE_REPUTATION,
                effect_value="elder",
                effect_amount=10
            ),
            DialogueChoice(
                text="❓ Что происходит?",
                next_dialogue_id="elder_explain"
            ),
            DialogueChoice(
                text="💰 А что мне за это будет?",
                next_dialogue_id="elder_mercenary",
                effect=DialogueChoiceEffect.CHANGE_REPUTATION,
                effect_value="elder",
                effect_amount=-5
            )
        ],
        is_first=True
    ),
    "elder_hero_path": Dialogue(
        dialogue_id="elder_hero_path",
        npc_key="elder",
        text=(
            "👴 *Старейшина кивает с одобрением*\n\n"
            "— Вижу в твоих глазах решимость. Это хорошо. "
            "Начни с Тёмного леса - там орудуют гоблины и волки. "
            "Их вожак стал особенно дерзким. Останови его, и ты докажешь свою силу.\n\n"
            "Да хранят тебя древние!"
        ),
        choices=[
            DialogueChoice(text="✊ Я не подведу!", next_dialogue_id=None)
        ]
    ),
    "elder_explain": Dialogue(
        dialogue_id="elder_explain",
        npc_key="elder",
        text=(
            "👴 *Старейшина тяжело вздыхает*\n\n"
            "— Древнее пророчество сбывается. Темные силы, дремавшие веками, "
            "пробуждаются одна за другой. Сначала гоблины и нежить, затем драконы, "
            "а дальше... дальше будет только хуже.\n\n"
            "Но есть и другое пророчество - о герое, который остановит тьму. "
            "Возможно, это ты."
        ),
        choices=[
            DialogueChoice(text="⚔️ Тогда я попробую", next_dialogue_id="elder_hero_path"),
            DialogueChoice(text="😰 Это слишком для меня...", next_dialogue_id=None)
        ]
    ),
    "elder_mercenary": Dialogue(
        dialogue_id="elder_mercenary",
        npc_key="elder",
        text=(
            "👴 *Старейшина разочарованно качает головой*\n\n"
            "— Золото? Когда тьма поглотит мир, золото тебе не поможет, молодой человек. "
            "Но если тебе нужна награда - каждый побеждённый враг принесёт тебе опыт, "
            "золото и славу. Чем сильнее противник - тем больше награда.\n\n"
            "Решай сам, что для тебя важнее."
        ),
        choices=[
            DialogueChoice(text="Хорошо, я помогу", next_dialogue_id="elder_hero_path"),
            DialogueChoice(text="Подумаю над этим", next_dialogue_id=None)
        ]
    ),

    # === Кузнец Торин ===
    "blacksmith_intro": Dialogue(
        dialogue_id="blacksmith_intro",
        npc_key="blacksmith",
        text=(
            "🔨 *Кузнец Торин отрывается от работы над мечом*\n\n"
            "— О, новое лицо! Я Торин, лучший кузнец в этих краях. "
            "Если тебе нужно оружие или броня - ты по адресу. "
            "Правда, за хорошую работу придётся заплатить.\n\n"
            "Или может, ты сам кое-что принёс показать?"
        ),
        choices=[
            DialogueChoice(text="🛒 Покажи товары", next_dialogue_id="blacksmith_shop"),
            DialogueChoice(text="⚒️ Как ты стал кузнецом?", next_dialogue_id="blacksmith_story"),
            DialogueChoice(text="👋 До встречи", next_dialogue_id=None)
        ],
        is_first=True
    ),
    "blacksmith_shop": Dialogue(
        dialogue_id="blacksmith_shop",
        npc_key="blacksmith",
        text=(
            "🔨 *Торин показывает свои изделия*\n\n"
            "— Вот, гляди: стальной меч, топор, кожаная броня... "
            "Всё по честной цене! Используй команду /shop чтобы увидеть весь ассортимент."
        ),
        choices=[
            DialogueChoice(text="Спасибо, посмотрю", next_dialogue_id=None)
        ]
    ),
    "blacksmith_story": Dialogue(
        dialogue_id="blacksmith_story",
        npc_key="blacksmith",
        text=(
            "🔨 *Кузнец улыбается, вспоминая прошлое*\n\n"
            "— Ха! Я был искателем приключений, как и ты. Сражался с драконами, "
            "исследовал подземелья... Но потом понял - мой настоящий дар не в мече, "
            "а в молоте и наковальне. Теперь я создаю оружие для новых героев.\n\n"
            "И знаешь что? Это приносит не меньше удовлетворения!"
        ),
        choices=[
            DialogueChoice(
                text="Вдохновляющая история!",
                next_dialogue_id=None,
                effect=DialogueChoiceEffect.CHANGE_REPUTATION,
                effect_value="blacksmith",
                effect_amount=5
            )
        ]
    ),

    # === Маг Элария ===
    "mage_intro": Dialogue(
        dialogue_id="mage_intro",
        npc_key="mage",
        text=(
            "🧙‍♀️ *Элария поднимает взгляд от древнего фолианта*\n\n"
            "— А-а, ты тот самый герой, о котором все говорят. Интересно... "
            "Я чувствую в тебе силу, но она ещё дремлет. "
            "Магия - великая сила, но она требует понимания и контроля.\n\n"
            "Хочешь узнать больше о древних силах?"
        ),
        choices=[
            DialogueChoice(text="✨ Расскажи о магии", next_dialogue_id="mage_magic_lesson"),
            DialogueChoice(text="📖 Что ты изучаешь?", next_dialogue_id="mage_research"),
            DialogueChoice(text="🎁 У тебя есть заклинания?", next_dialogue_id="mage_spells")
        ],
        is_first=True,
        required_chapter=3
    ),
    "mage_magic_lesson": Dialogue(
        dialogue_id="mage_magic_lesson",
        npc_key="mage",
        text=(
            "🧙‍♀️ *Элария начинает объяснять*\n\n"
            "— Магия пронизывает весь наш мир. Заклинания требуют маны - "
            "магической энергии, которая восстанавливается с каждым новым уровнем. "
            "Чем сильнее заклинание, тем больше маны оно требует.\n\n"
            "В бою магия может дать тебе преимущество - огненный шар сожжёт врага, "
            "а исцеление вернёт тебе силы. Используй их мудро!"
        ),
        choices=[
            DialogueChoice(text="Понятно, спасибо!", next_dialogue_id=None)
        ]
    ),
    "mage_research": Dialogue(
        dialogue_id="mage_research",
        npc_key="mage",
        text=(
            "🧙‍♀️ *Элария становится серьёзной*\n\n"
            "— Я изучаю древние пророчества. То, что происходит сейчас - "
            "не случайность. Тёмные силы пробуждаются в определённом порядке. "
            "За драконом придёт нечто худшее. И за ним ещё худшее.\n\n"
            "Но есть и надежда. Пророчество говорит о герое, который объединит "
            "силу стали и магии. Продолжай свой путь, и возможно, ты узнаешь правду."
        ),
        choices=[
            DialogueChoice(text="Я постараюсь", next_dialogue_id=None)
        ]
    ),
    "mage_spells": Dialogue(
        dialogue_id="mage_spells",
        npc_key="mage",
        text=(
            "🧙‍♀️ *Элария указывает на полку с магическими свитками*\n\n"
            "— Да, у меня есть несколько заклинаний на продажу. "
            "Огненный шар, молния, ледяной взрыв... и заклинания исцеления. "
            "Загляни в магазин - там увидишь всё, что доступно."
        ),
        choices=[
            DialogueChoice(text="Отлично, посмотрю", next_dialogue_id=None)
        ]
    ),

    # === Моряк Коралл ===
    "sailor_intro": Dialogue(
        dialogue_id="sailor_intro",
        npc_key="sailor",
        text=(
            "⚓ *Старый моряк смотрит на тёмные воды*\n\n"
            "— Видел я его... Левиафана. Чудовище из легенд. "
            "Наш корабль был разорван пополам, будто игрушка. "
            "Я единственный, кто выжил.\n\n"
            "Ты идёшь туда, вниз? В бездну? "
            "Тогда возьми мой совет - не смотри ему в глаза. "
            "В них видишь собственную смерть."
        ),
        choices=[
            DialogueChoice(text="😨 Может, расскажешь подробнее?", next_dialogue_id="sailor_warning"),
            DialogueChoice(text="💪 Я не боюсь", next_dialogue_id="sailor_brave"),
            DialogueChoice(text="🎣 Как ты оказался здесь?", next_dialogue_id="sailor_story")
        ],
        is_first=True,
        required_chapter=5
    ),
    "sailor_warning": Dialogue(
        dialogue_id="sailor_warning",
        npc_key="sailor",
        text=(
            "⚓ *Моряк содрогается от воспоминаний*\n\n"
            "— Левиафан... он не просто монстр. Он - гнев самого океана. "
            "Щупальца толщиной с корабельную мачту, зубы как мечи. "
            "Но самое страшное - его песня. Она зовёт тебя вниз, в глубину...\n\n"
            "Приготовься хорошо. Запасись зельями, улучши экипировку. "
            "И главное - не иди туда один. Хотя... похоже, у тебя нет выбора."
        ),
        choices=[
            DialogueChoice(text="Спасибо за совет", next_dialogue_id=None)
        ]
    ),
    "sailor_brave": Dialogue(
        dialogue_id="sailor_brave",
        npc_key="sailor",
        text=(
            "⚓ *Моряк криво усмехается*\n\n"
            "— Храбрость или глупость? Тонкая грань. "
            "Я тоже был храбрым... до встречи с ним. "
            "Но вижу в твоих глазах что-то другое. Не просто храбрость - решимость.\n\n"
            "Ладно. Если ты действительно собираешься туда - возьми это. "
            "*Протягивает морской амулет* "
            "Он не спасёт тебя, но может дать шанс."
        ),
        choices=[
            DialogueChoice(
                text="🙏 Спасибо",
                next_dialogue_id=None,
                effect=DialogueChoiceEffect.RECEIVE_ITEM,
                effect_value="ancient_amulet"
            )
        ]
    ),
    "sailor_story": Dialogue(
        dialogue_id="sailor_story",
        npc_key="sailor",
        text=(
            "⚓ *Моряк смотрит вдаль*\n\n"
            "— Мы везли груз пряностей из южных островов. Обычный рейс. "
            "Но в ту ночь море было слишком спокойным. Слишком тихим. "
            "А потом... он появился из глубины.\n\n"
            "Я держался за обломок мачты три дня. Когда меня нашли рыбаки, "
            "я был больше мёртв, чем жив. С тех пор не выхожу в море. "
            "Но пришёл сюда - кто-то должен предупреждать таких как ты."
        ),
        choices=[
            DialogueChoice(text="Твоё предупреждение не зря", next_dialogue_id=None)
        ]
    ),

    # === Таинственный незнакомец ===
    "stranger_intro": Dialogue(
        dialogue_id="stranger_intro",
        npc_key="mysterious_stranger",
        text=(
            "🎭 *Фигура в тёмном плаще выходит из тени*\n\n"
            "— Герой... Как интересно. Ты думаешь, сражаешься со злом? "
            "Но что если я скажу тебе, что добро и зло - всего лишь точка зрения?\n\n"
            "Впрочем, не слушай меня. Я просто... наблюдатель. "
            "Но если хочешь узнать правду о том, что на самом деле происходит... "
            "Найди меня, когда дойдёшь до Пустоты."
        ),
        choices=[
            DialogueChoice(text="❓ Кто ты такой?", next_dialogue_id="stranger_identity"),
            DialogueChoice(text="😠 Говори ясно!", next_dialogue_id="stranger_cryptic"),
            DialogueChoice(text="👋 Мне некогда", next_dialogue_id=None)
        ],
        is_first=True,
        required_chapter=2
    ),
    "stranger_identity": Dialogue(
        dialogue_id="stranger_identity",
        npc_key="mysterious_stranger",
        text=(
            "🎭 *Незнакомец тихо смеётся*\n\n"
            "— Кто я? Хороший вопрос. Скажем так - я тот, кто видел начало. "
            "И, возможно, увижу конец. Или ты его изменишь? Время покажет.\n\n"
            "*Фигура начинает растворяться в тенях*\n\n"
            "— До встречи, герой. В Пустоте все маски падают..."
        ),
        choices=[
            DialogueChoice(text="...", next_dialogue_id=None)
        ]
    ),
    "stranger_cryptic": Dialogue(
        dialogue_id="stranger_cryptic",
        npc_key="mysterious_stranger",
        text=(
            "🎭 *Незнакомец качает головой*\n\n"
            "— Ясность - иллюзия для тех, кто боится сложности. "
            "Ты хочешь простых ответов, но вселенная не работает так. "
            "Каждый твой выбор создаёт новую реальность.\n\n"
            "Впрочем, узнаешь сам. Когда будешь готов."
        ),
        choices=[
            DialogueChoice(text="Странный тип...", next_dialogue_id=None)
        ]
    )
}


def get_npc(npc_key: str) -> NPC | None:
    """Получить NPC по ключу."""
    return NPCS.get(npc_key)


def get_dialogue(dialogue_id: str) -> Dialogue | None:
    """Получить диалог по ID."""
    return DIALOGUES.get(dialogue_id)


def get_npcs_in_location(location: str, player_chapter: int = 1) -> list[NPC]:
    """Получить всех NPC в локации."""
    return [
        npc for npc in NPCS.values()
        if npc.location == location and npc.available_from_chapter <= player_chapter
    ]
