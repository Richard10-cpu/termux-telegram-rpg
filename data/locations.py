"""Статические данные локаций."""
from models import Location

LOCATIONS: dict[str, Location] = {
    "village": Location(
        key="village",
        name="🏘️ Деревня",
        emoji="🏘️",
        enemies=[],
        description="Мирное место для отдыха и торговли.",
        image_path="assets/images/locations/village.png"
    ),
    "forest": Location(
        key="forest",
        name="🌲 Тёмный лес",
        emoji="🌲",
        enemies=["goblin", "wolf"],
        description="Тёмный лес полный опасностей.",
        image_path="assets/images/locations/forest.png"
    ),
    "cave": Location(
        key="cave",
        name="🕳️ Пещера",
        emoji="🕳️",
        enemies=["skeleton", "orc"],
        description="Тёмная пещера с нежитью и орками.",
        image_path="assets/images/locations/cave.png"
    ),
    "mountain": Location(
        key="mountain",
        name="⛰️ Гора",
        emoji="⛰️",
        enemies=["orc", "dragon"],
        description="Опасная гора с драконами!",
        image_path="assets/images/locations/mountain.png"
    ),
    "abyss": Location(
        key="abyss",
        name="🌊 Морская бездна",
        emoji="🌊",
        enemies=["sea_serpent", "kraken"],
        description="Тёмные глубины океана, полные древних ужасов.",
        image_path="assets/images/locations/abyss.png"
    ),
    "ruins": Location(
        key="ruins",
        name="🏛️ Руины империи",
        emoji="🏛️",
        enemies=["golem", "lich"],
        description="Остатки некогда великой магической цивилизации.",
        image_path="assets/images/locations/ruins.png"
    ),
    "hell": Location(
        key="hell",
        name="🔥 Преисподняя",
        emoji="🔥",
        enemies=["demon", "hellhound"],
        description="Мир вечного пламени и страданий.",
        image_path="assets/images/locations/hell.png"
    ),
    "void": Location(
        key="void",
        name="⚡ Пустота",
        emoji="⚡",
        enemies=["void_entity", "chaos_spawn"],
        description="Место за гранью реальности, где законы природы не действуют.",
        image_path="assets/images/locations/void.png"
    )
}
