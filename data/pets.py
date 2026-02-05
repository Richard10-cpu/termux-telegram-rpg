"""Система питомцев и компаньонов."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Pet:
    """Питомец."""
    pet_id: str
    name: str
    pet_type: str
    emoji: str
    description: str
    # Бонусы
    hp_bonus: int = 0
    power_bonus: int = 0
    mana_bonus: int = 0
    gold_bonus: float = 0.0  # Множитель золота (0.1 = +10%)
    exp_bonus: float = 0.0  # Множитель опыта
    # Особые способности
    special_ability: Optional[str] = None
    ability_description: Optional[str] = None
    # Требования
    required_level: int = 1
    rarity: str = "common"


PETS = {
    "cat": Pet(
        pet_id="cat",
        name="Мурзик",
        pet_type="cat",
        emoji="🐱",
        description="Милый кот, найденный в лесу. Приносит удачу!",
        gold_bonus=0.05,  # +5% золота
        special_ability="lucky",
        ability_description="Шанс найти дополнительное золото после боя",
        rarity="common"
    ),

    "wolf": Pet(
        pet_id="wolf",
        name="Клык",
        pet_type="wolf",
        emoji="🐺",
        description="Верный волк-компаньон. Помогает в бою!",
        power_bonus=15,
        special_ability="pack_hunter",
        ability_description="Наносит дополнительный урон врагам",
        required_level=5,
        rarity="rare"
    ),

    "dragon": Pet(
        pet_id="dragon",
        name="Дрейк",
        pet_type="dragon",
        emoji="🐉",
        description="Могучий дракон! Вырос из яйца и предан вам.",
        hp_bonus=100,
        power_bonus=50,
        mana_bonus=50,
        exp_bonus=0.25,  # +25% опыта
        special_ability="dragon_breath",
        ability_description="Может использовать драконье дыхание в бою",
        required_level=20,
        rarity="legendary"
    ),

    "phoenix": Pet(
        pet_id="phoenix",
        name="Феникс",
        pet_type="phoenix",
        emoji="🔥",
        description="Бессмертная огненная птица. Возрождается из пепла!",
        hp_bonus=50,
        mana_bonus=100,
        special_ability="rebirth",
        ability_description="Один раз спасает от смерти, воскрешая вас",
        required_level=25,
        rarity="legendary"
    ),

    "fairy": Pet(
        pet_id="fairy",
        name="Искорка",
        pet_type="fairy",
        emoji="🧚",
        description="Маленькая фея-помощница. Восстанавливает ману!",
        mana_bonus=50,
        special_ability="mana_regeneration",
        ability_description="Восстанавливает 5 маны после каждого боя",
        required_level=10,
        rarity="rare"
    ),

    "owl": Pet(
        pet_id="owl",
        name="Мудрейший",
        pet_type="owl",
        emoji="🦉",
        description="Мудрая сова. Увеличивает получаемый опыт!",
        exp_bonus=0.15,  # +15% опыта
        special_ability="wisdom",
        ability_description="Увеличивает получаемый опыт",
        required_level=8,
        rarity="rare"
    ),

    "slime": Pet(
        pet_id="slime",
        name="Слизняк",
        pet_type="slime",
        emoji="💧",
        description="Милый слизняк. Немного помогает во всём!",
        hp_bonus=10,
        power_bonus=5,
        mana_bonus=10,
        gold_bonus=0.03,
        exp_bonus=0.03,
        special_ability="versatile",
        ability_description="Небольшие бонусы ко всему",
        rarity="common"
    ),

    "unicorn": Pet(
        pet_id="unicorn",
        name="Единорог",
        pet_type="unicorn",
        emoji="🦄",
        description="Легендарный единорог. Лечит вас после боя!",
        hp_bonus=75,
        mana_bonus=75,
        special_ability="healing_aura",
        ability_description="Восстанавливает 20 HP после каждого боя",
        required_level=30,
        rarity="legendary"
    ),

    "robot": Pet(
        pet_id="robot",
        name="R2-X7",
        pet_type="robot",
        emoji="🤖",
        description="Боевой робот из другого измерения!",
        power_bonus=30,
        special_ability="analyze",
        ability_description="Показывает слабости врагов (+10% урона)",
        required_level=15,
        rarity="epic"
    ),

    "ghost": Pet(
        pet_id="ghost",
        name="Призрак",
        pet_type="ghost",
        emoji="👻",
        description="Дружелюбный призрак. Пугает врагов!",
        mana_bonus=40,
        special_ability="intimidate",
        ability_description="Враги иногда убегают от страха",
        required_level=12,
        rarity="rare"
    )
}


def get_pet(pet_id: str) -> Optional[Pet]:
    """Получить питомца по ID."""
    return PETS.get(pet_id)


def get_available_pets(player_level: int) -> list[Pet]:
    """Получить доступных питомцев для уровня."""
    return [pet for pet in PETS.values() if pet.required_level <= player_level]


def apply_pet_bonuses(player, pet: Pet):
    """Применить бонусы питомца к игроку."""
    # Эти бонусы применяются временно при экипировке питомца
    pass  # Реализация зависит от системы экипировки


def get_pet_description(pet: Pet, owned: bool = False) -> str:
    """Получить описание питомца."""
    status = "✅ У вас есть" if owned else "🔒 Не получен"

    rarity_colors = {
        "common": "⚪",
        "rare": "🔵",
        "epic": "🟣",
        "legendary": "🟡"
    }

    text = f"{pet.emoji} {pet.name} {rarity_colors.get(pet.rarity, '')}\n"
    text += f"Статус: {status}\n"
    text += f"📝 {pet.description}\n\n"

    bonuses = []
    if pet.hp_bonus > 0:
        bonuses.append(f"+{pet.hp_bonus} HP")
    if pet.power_bonus > 0:
        bonuses.append(f"+{pet.power_bonus} Силы")
    if pet.mana_bonus > 0:
        bonuses.append(f"+{pet.mana_bonus} Маны")
    if pet.gold_bonus > 0:
        bonuses.append(f"+{int(pet.gold_bonus * 100)}% золота")
    if pet.exp_bonus > 0:
        bonuses.append(f"+{int(pet.exp_bonus * 100)}% опыта")

    if bonuses:
        text += f"💪 Бонусы: {', '.join(bonuses)}\n"

    if pet.special_ability:
        text += f"✨ Способность: {pet.ability_description}\n"

    text += f"📊 Требуется уровень: {pet.required_level}"

    return text
