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
        max_level=10,
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
        max_level=10,
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
        max_level=15,
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
        max_level=20,
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
        max_level=100,
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
        max_level=100,
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
        max_level=100,
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
        max_level=100,
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
        max_level=100,
        image_path="assets/images/monsters/ancient_dragon.png"
    ),
    # Новые монстры для морской бездны
    "sea_serpent": MonsterTemplate(
        key="sea_serpent",
        name="Морской змей",
        hp=100,
        power=32,
        exp=70,
        gold_min=25,
        gold_max=50,
        min_level=18,
        max_level=100,
        image_path="assets/images/monsters/sea_serpent.png"
    ),
    "kraken": MonsterTemplate(
        key="kraken",
        name="Кракен",
        hp=130,
        power=38,
        exp=90,
        gold_min=35,
        gold_max=65,
        min_level=20,
        max_level=100,
        image_path="assets/images/monsters/kraken.png"
    ),
    # Новые монстры для руин
    "golem": MonsterTemplate(
        key="golem",
        name="Каменный голем",
        hp=160,
        power=42,
        exp=110,
        gold_min=40,
        gold_max=75,
        min_level=23,
        max_level=100,
        image_path="assets/images/monsters/golem.png"
    ),
    "lich": MonsterTemplate(
        key="lich",
        name="Лич",
        hp=140,
        power=48,
        exp=130,
        gold_min=50,
        gold_max=85,
        min_level=25,
        max_level=100,
        image_path="assets/images/monsters/lich.png"
    ),
    # Новые монстры для преисподней
    "demon": MonsterTemplate(
        key="demon",
        name="Демон",
        hp=180,
        power=52,
        exp=150,
        gold_min=60,
        gold_max=100,
        min_level=28,
        max_level=100,
        image_path="assets/images/monsters/demon.png"
    ),
    "hellhound": MonsterTemplate(
        key="hellhound",
        name="Адская гончая",
        hp=150,
        power=50,
        exp=140,
        gold_min=55,
        gold_max=95,
        min_level=28,
        max_level=100,
        image_path="assets/images/monsters/hellhound.png"
    ),
    # Новые монстры для пустоты
    "void_entity": MonsterTemplate(
        key="void_entity",
        name="Сущность Пустоты",
        hp=220,
        power=58,
        exp=180,
        gold_min=75,
        gold_max=120,
        min_level=33,
        max_level=100,
        image_path="assets/images/monsters/void_entity.png"
    ),
    "chaos_spawn": MonsterTemplate(
        key="chaos_spawn",
        name="Порождение Хаоса",
        hp=200,
        power=60,
        exp=200,
        gold_min=80,
        gold_max=130,
        min_level=33,
        max_level=100,
        image_path="assets/images/monsters/chaos_spawn.png"
    ),
    # Новые сюжетные боссы
    "leviathan": MonsterTemplate(
        key="leviathan",
        name="Левиафан, Повелитель глубин",
        hp=500,
        power=55,
        exp=800,
        gold_min=300,
        gold_max=450,
        min_level=20,
        max_level=100,
        image_path="assets/images/monsters/leviathan.png"
    ),
    "archmage_maleficus": MonsterTemplate(
        key="archmage_maleficus",
        name="Архимаг-Предатель Малефикус",
        hp=700,
        power=65,
        exp=1200,
        gold_min=500,
        gold_max=700,
        min_level=25,
        max_level=100,
        image_path="assets/images/monsters/archmage_maleficus.png"
    ),
    "abaddon": MonsterTemplate(
        key="abaddon",
        name="Абаддон, Повелитель демонов",
        hp=1000,
        power=75,
        exp=2000,
        gold_min=800,
        gold_max=1200,
        min_level=30,
        max_level=100,
        image_path="assets/images/monsters/abaddon.png"
    ),
    "primordial_chaos": MonsterTemplate(
        key="primordial_chaos",
        name="Первозданный Хаос",
        hp=1500,
        power=90,
        exp=5000,
        gold_min=2000,
        gold_max=3000,
        min_level=35,
        max_level=100,
        image_path="assets/images/monsters/primordial_chaos.png"
    )
}


# Маппинг имён боссов на их ключи
BOSS_NAME_TO_KEY = {
    "Вожак гоблинов": "goblin_chief",
    "Король скелетов": "skeleton_king",
    "Вождь орков": "orc_warlord",
    "Древний дракон Тенебрис": "ancient_dragon",
    "Левиафан, Повелитель глубин": "leviathan",
    "Архимаг-Предатель Малефикус": "archmage_maleficus",
    "Абаддон, Повелитель демонов": "abaddon",
    "Первозданный Хаос": "primordial_chaos"
}
