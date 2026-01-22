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
    )
}
