"""Статические данные монстров."""
from models import MonsterTemplate

MONSTER_TEMPLATES: dict[str, MonsterTemplate] = {
    "goblin": MonsterTemplate(
        key="goblin",
        name="Гоблин",
        hp=25,
        power=8,
        exp=15,
        gold_min=3,
        gold_max=8,
        min_level=1,
        image_path="assets/images/monsters/goblin.png"
    ),
    "wolf": MonsterTemplate(
        key="wolf",
        name="Волк",
        hp=35,
        power=12,
        exp=20,
        gold_min=5,
        gold_max=12,
        min_level=1,
        image_path="assets/images/monsters/wolf.png"
    ),
    "skeleton": MonsterTemplate(
        key="skeleton",
        name="Скелет",
        hp=40,
        power=15,
        exp=25,
        gold_min=8,
        gold_max=15,
        min_level=3,
        image_path="assets/images/monsters/skeleton.png"
    ),
    "orc": MonsterTemplate(
        key="orc",
        name="Орк",
        hp=55,
        power=18,
        exp=35,
        gold_min=10,
        gold_max=20,
        min_level=5,
        image_path="assets/images/monsters/orc.png"
    ),
    "dragon": MonsterTemplate(
        key="dragon",
        name="Дракон",
        hp=80,
        power=25,
        exp=50,
        gold_min=20,
        gold_max=40,
        min_level=8,
        image_path="assets/images/monsters/dragon.png"
    ),
    # Сюжетные боссы
    "goblin_chief": MonsterTemplate(
        key="goblin_chief",
        name="Вожак гоблинов",
        hp=60,
        power=15,
        exp=50,
        gold_min=30,
        gold_max=50,
        min_level=1,
        image_path="assets/images/monsters/goblin_chief.png"
    ),
    "skeleton_king": MonsterTemplate(
        key="skeleton_king",
        name="Король скелетов",
        hp=120,
        power=22,
        exp=100,
        gold_min=50,
        gold_max=80,
        min_level=5,
        image_path="assets/images/monsters/skeleton_king.png"
    ),
    "orc_warlord": MonsterTemplate(
        key="orc_warlord",
        name="Вождь орков",
        hp=200,
        power=30,
        exp=200,
        gold_min=100,
        gold_max=150,
        min_level=10,
        image_path="assets/images/monsters/orc_warlord.png"
    ),
    "ancient_dragon": MonsterTemplate(
        key="ancient_dragon",
        name="Древний дракон Тенебрис",
        hp=350,
        power=40,
        exp=500,
        gold_min=200,
        gold_max=300,
        min_level=15,
        image_path="assets/images/monsters/ancient_dragon.png"
    )
}


# Маппинг имён боссов на их ключи
BOSS_NAME_TO_KEY = {
    "Вожак гоблинов": "goblin_chief",
    "Король скелетов": "skeleton_king",
    "Вождь орков": "orc_warlord",
    "Древний дракон Тенебрис": "ancient_dragon"
}
