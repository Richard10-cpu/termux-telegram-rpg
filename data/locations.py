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
        description="Тёмный лес полный опасностей."
    ),
    "cave": Location(
        key="cave",
        name="🕳️ Пещера",
        emoji="🕳️",
        enemies=["skeleton", "orc"],
        description="Тёмная пещера с нежитью и орками."
    ),
    "mountain": Location(
        key="mountain",
        name="⛰️ Гора",
        emoji="⛰️",
        enemies=["orc", "dragon"],
        description="Опасная гора с драконами!"
    )
}
