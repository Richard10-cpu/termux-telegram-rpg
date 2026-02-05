"""Система крафта и алхимии."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CraftingRecipe:
    """Рецепт крафта."""
    recipe_id: str
    result_item: str
    result_amount: int
    ingredients: dict[str, int]  # {item_name: amount}
    required_level: int
    craft_type: str  # "blacksmith", "alchemy", "enchanting"
    description: str


CRAFTING_RECIPES = {
    # === Кузнечное дело ===
    "iron_sword": CraftingRecipe(
        recipe_id="iron_sword",
        result_item="Железный меч",
        result_amount=1,
        ingredients={"Железная руда": 5, "Дерево": 2},
        required_level=3,
        craft_type="blacksmith",
        description="Простой но надёжный меч"
    ),

    "steel_armor": CraftingRecipe(
        recipe_id="steel_armor",
        result_item="Стальная броня",
        result_amount=1,
        ingredients={"Стальные слитки": 10, "Кожа": 5},
        required_level=8,
        craft_type="blacksmith",
        description="Прочная броня из стали"
    ),

    "legendary_blade": CraftingRecipe(
        recipe_id="legendary_blade",
        result_item="Клинок легенды",
        result_amount=1,
        ingredients={
            "Мифриловая руда": 20,
            "Драконья чешуя": 5,
            "Осколок души": 3,
            "Кристалл маны": 10
        },
        required_level=30,
        craft_type="blacksmith",
        description="Легендарный клинок невероятной силы"
    ),

    # === Алхимия ===
    "health_potion_craft": CraftingRecipe(
        recipe_id="health_potion_craft",
        result_item="Зелье здоровья",
        result_amount=3,
        ingredients={"Красная трава": 2, "Вода": 1},
        required_level=1,
        craft_type="alchemy",
        description="Базовое лечебное зелье"
    ),

    "mana_potion_craft": CraftingRecipe(
        recipe_id="mana_potion_craft",
        result_item="Зелье маны",
        result_amount=3,
        ingredients={"Синий цветок": 2, "Вода": 1},
        required_level=1,
        craft_type="alchemy",
        description="Восстанавливает ману"
    ),

    "greater_health_potion": CraftingRecipe(
        recipe_id="greater_health_potion",
        result_item="Большое зелье здоровья",
        result_amount=1,
        ingredients={
            "Зелье здоровья": 3,
            "Золотой корень": 1,
            "Кристалл жизни": 1
        },
        required_level=15,
        craft_type="alchemy",
        description="Мощное лечебное зелье (+150 HP)"
    ),

    "elixir_of_power": CraftingRecipe(
        recipe_id="elixir_of_power",
        result_item="Эликсир силы",
        result_amount=1,
        ingredients={
            "Драконья кровь": 1,
            "Сердце демона": 1,
            "Звёздная пыль": 3
        },
        required_level=25,
        craft_type="alchemy",
        description="Навсегда увеличивает силу на 20"
    ),

    "philosophers_stone": CraftingRecipe(
        recipe_id="philosophers_stone",
        result_item="Философский камень",
        result_amount=1,
        ingredients={
            "Золото": 1000,
            "Кристалл маны": 50,
            "Эссенция жизни": 10,
            "Частица хаоса": 1
        },
        required_level=35,
        craft_type="alchemy",
        description="Легендарный артефакт алхимиков"
    ),

    # === Зачарование ===
    "enchant_fire": CraftingRecipe(
        recipe_id="enchant_fire",
        result_item="Руна огня",
        result_amount=1,
        ingredients={"Огненный кристалл": 5, "Пергамент": 1},
        required_level=10,
        craft_type="enchanting",
        description="Добавляет оружию урон огнём"
    ),

    "enchant_ice": CraftingRecipe(
        recipe_id="enchant_ice",
        result_item="Руна льда",
        result_amount=1,
        ingredients={"Ледяной кристалл": 5, "Пергамент": 1},
        required_level=10,
        craft_type="enchanting",
        description="Добавляет оружию урон льдом"
    ),

    "enchant_thunder": CraftingRecipe(
        recipe_id="enchant_thunder",
        result_item="Руна грома",
        result_amount=1,
        ingredients={"Кристалл молнии": 5, "Пергамент": 1},
        required_level=10,
        craft_type="enchanting",
        description="Добавляет оружию урон молнией"
    ),

    "enchant_lifesteal": CraftingRecipe(
        recipe_id="enchant_lifesteal",
        result_item="Руна вампиризма",
        result_amount=1,
        ingredients={
            "Кровь вампира": 3,
            "Душа нежити": 5,
            "Тёмный кристалл": 10
        },
        required_level=20,
        craft_type="enchanting",
        description="Добавляет оружию вампиризм 10%"
    ),

    # === Особые крафты ===
    "magical_pet_food": CraftingRecipe(
        recipe_id="magical_pet_food",
        result_item="Магический корм",
        result_amount=5,
        ingredients={"Мясо": 3, "Кристалл маны": 1},
        required_level=5,
        craft_type="alchemy",
        description="Усиливает питомцев"
    ),

    "teleport_scroll": CraftingRecipe(
        recipe_id="teleport_scroll",
        result_item="Свиток телепорта",
        result_amount=1,
        ingredients={"Пергамент": 1, "Эфирная пыль": 5},
        required_level=12,
        craft_type="enchanting",
        description="Мгновенно телепортирует в деревню"
    ),

    "resurrection_stone": CraftingRecipe(
        recipe_id="resurrection_stone",
        result_item="Камень воскрешения",
        result_amount=1,
        ingredients={
            "Кристалл жизни": 10,
            "Душа феникса": 1,
            "Слеза ангела": 3
        },
        required_level=30,
        craft_type="enchanting",
        description="Воскрешает при смерти (одноразовый)"
    ),
}


@dataclass
class Material:
    """Материал для крафта."""
    material_id: str
    name: str
    description: str
    rarity: str
    emoji: str
    # Где можно найти
    sources: list[str]  # "mining", "fishing", "monster_drop", "gathering"


MATERIALS = {
    # === Руды ===
    "iron_ore": Material(
        "iron_ore", "Железная руда", "Обычная железная руда",
        "common", "⛏️", ["mining"]
    ),
    "steel_ingot": Material(
        "steel_ingot", "Стальной слиток", "Выплавленная сталь",
        "common", "🔩", ["blacksmith"]
    ),
    "mithril_ore": Material(
        "mithril_ore", "Мифриловая руда", "Редкая магическая руда",
        "epic", "💎", ["mining"]
    ),

    # === Травы и цветы ===
    "red_herb": Material(
        "red_herb", "Красная трава", "Лечебная трава",
        "common", "🌿", ["gathering"]
    ),
    "blue_flower": Material(
        "blue_flower", "Синий цветок", "Магический цветок",
        "common", "🌸", ["gathering"]
    ),
    "golden_root": Material(
        "golden_root", "Золотой корень", "Редкий корень с целебными свойствами",
        "rare", "🥕", ["gathering"]
    ),

    # === Кристаллы ===
    "mana_crystal": Material(
        "mana_crystal", "Кристалл маны", "Чистая кристаллизованная мана",
        "rare", "💎", ["mining", "monster_drop"]
    ),
    "life_crystal": Material(
        "life_crystal", "Кристалл жизни", "Содержит эссенцию жизни",
        "epic", "💚", ["monster_drop"]
    ),
    "chaos_shard": Material(
        "chaos_shard", "Частица хаоса", "Фрагмент Первозданного Хаоса",
        "legendary", "⚡", ["boss_drop"]
    ),

    # === Монстровые дропы ===
    "dragon_scale": Material(
        "dragon_scale", "Драконья чешуя", "Прочная чешуя дракона",
        "rare", "🐉", ["monster_drop"]
    ),
    "demon_heart": Material(
        "demon_heart", "Сердце демона", "Пульсирующее сердце демона",
        "epic", "❤️", ["monster_drop"]
    ),
    "soul_fragment": Material(
        "soul_fragment", "Осколок души", "Фрагмент потерянной души",
        "rare", "👻", ["monster_drop"]
    ),

    # === Прочее ===
    "leather": Material(
        "leather", "Кожа", "Обработанная кожа",
        "common", "🦴", ["monster_drop"]
    ),
    "wood": Material(
        "wood", "Дерево", "Крепкая древесина",
        "common", "🪵", ["gathering"]
    ),
    "parchment": Material(
        "parchment", "Пергамент", "Чистый пергамент для записей",
        "common", "📜", ["shop"]
    ),
}


def get_recipe(recipe_id: str) -> Optional[CraftingRecipe]:
    """Получить рецепт по ID."""
    return CRAFTING_RECIPES.get(recipe_id)


def get_recipes_by_type(craft_type: str, player_level: int) -> list[CraftingRecipe]:
    """Получить рецепты по типу крафта."""
    return [
        recipe for recipe in CRAFTING_RECIPES.values()
        if recipe.craft_type == craft_type and recipe.required_level <= player_level
    ]


def can_craft(player_inventory: list[str], recipe: CraftingRecipe) -> tuple[bool, str]:
    """Проверить, можно ли скрафтить предмет."""
    missing = []

    for ingredient, amount in recipe.ingredients.items():
        count = player_inventory.count(ingredient)
        if count < amount:
            missing.append(f"{ingredient}: {count}/{amount}")

    if missing:
        return False, "Не хватает материалов:\n" + "\n".join(missing)

    return True, ""


def craft_item(player_inventory: list[str], recipe: CraftingRecipe) -> tuple[bool, str]:
    """Скрафтить предмет."""
    can, msg = can_craft(player_inventory, recipe)

    if not can:
        return False, msg

    # Убрать ингредиенты
    for ingredient, amount in recipe.ingredients.items():
        for _ in range(amount):
            player_inventory.remove(ingredient)

    # Добавить результат
    for _ in range(recipe.result_amount):
        player_inventory.append(recipe.result_item)

    return True, (
        f"✨ Крафт успешен!\n\n"
        f"Создано: {recipe.result_item} x{recipe.result_amount}\n"
        f"📝 {recipe.description}"
    )
