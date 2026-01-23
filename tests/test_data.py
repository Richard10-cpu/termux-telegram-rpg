"""Тесты для статических данных игры."""
import pytest
from models import ItemType
from data import SHOP_ITEMS, MONSTER_TEMPLATES, LOCATIONS
from data.story_chapters import get_chapter, get_all_chapters, get_available_chapters


class TestShopItems:
    """Тесты предметов магазина."""

    def test_shop_items_structure(self):
        """Структура предметов магазина."""
        assert len(SHOP_ITEMS) > 0
        for key, shop_item in SHOP_ITEMS.items():
            assert shop_item.item is not None
            assert hasattr(shop_item.item, 'name')
            assert hasattr(shop_item.item, 'cost')

    def test_weapons_have_power_bonus(self):
        """Оружие имеет бонус к силе."""
        weapons = [v for v in SHOP_ITEMS.values() if v.item.item_type == ItemType.WEAPON]
        for shop_item in weapons:
            assert shop_item.item.power_bonus > 0

    def test_armor_has_hp_bonus(self):
        """Броня имеет бонус к HP."""
        armors = [v for v in SHOP_ITEMS.values() if v.item.item_type == ItemType.ARMOR]
        for shop_item in armors:
            assert shop_item.item.max_hp_bonus > 0

    def test_spells_have_mana_cost(self):
        """Заклинания имеют стоимость маны."""
        spells = [v for v in SHOP_ITEMS.values() if v.item.item_type == ItemType.SPELL]
        for shop_item in spells:
            assert shop_item.item.mana_cost > 0
            assert shop_item.item.is_spell is True

    def test_fireball_spell(self):
        """Конкретное заклинание - огненный шар."""
        fireball = SHOP_ITEMS.get("fireball")
        assert fireball is not None
        assert "Огненный шар" in fireball.item.name
        assert fireball.item.spell_damage > 0
        assert fireball.item.required_level >= 1

    def test_unique_items(self):
        """Уникальные предметы."""
        unique_count = sum(1 for v in SHOP_ITEMS.values() if v.unique)
        assert unique_count > 0  # Есть уникальные предметы

    def test_consumables_not_unique(self):
        """Расходуемые материалы не уникальны."""
        consumables = [v for v in SHOP_ITEMS.values() if v.item.item_type == ItemType.CONSUMABLE]
        for shop_item in consumables:
            assert shop_item.unique is False


class TestStoryChapters:
    """Тесты сюжетных глав."""

    def test_get_all_chapters(self):
        """Получение всех глав."""
        chapters = get_all_chapters()
        assert len(chapters) == 4  # 4 главы в игре
        assert chapters[0].chapter_id == 1
        assert chapters[-1].chapter_id == 4

    def test_get_chapter_by_id(self):
        """Получение главы по ID."""
        chapter = get_chapter(1)
        assert chapter is not None
        assert chapter.chapter_id == 1
        assert "Пробуждение" in chapter.title

    def test_get_chapter_invalid_id(self):
        """Несуществующая глава."""
        chapter = get_chapter(999)
        assert chapter is None

    def test_chapter_1_requirements(self):
        """Требования главы 1."""
        chapter = get_chapter(1)
        assert chapter.unlock_level == 1
        assert chapter.location_requirement == "forest"
        assert chapter.boss_name == "Вожак гоблинов"

    def test_chapter_4_final(self):
        """Финальная глава."""
        chapter = get_chapter(4)
        assert chapter.unlock_level == 15
        assert "Тенебрис" in chapter.boss_name

    def test_get_available_chapters_level_1(self):
        """Доступные главы для уровня 1."""
        chapters = get_available_chapters(1)
        assert len(chapters) >= 1
        assert chapters[0].chapter_id == 1

    def test_get_available_chapters_level_10(self):
        """Доступные главы для уровня 10."""
        chapters = get_available_chapters(10)
        assert len(chapters) >= 3

    def test_all_chapters_have_rewards(self):
        """Все главы имеют награды."""
        chapters = get_all_chapters()
        for chapter in chapters:
            assert chapter.reward_gold > 0
            assert chapter.reward_exp > 0


class TestLocations:
    """Тесты локаций."""

    def test_locations_exist(self):
        """Существование локаций."""
        assert "village" in LOCATIONS
        assert "forest" in LOCATIONS
        assert "cave" in LOCATIONS
        assert "mountain" in LOCATIONS

    def test_village_safe(self):
        """Деревня безопасная."""
        village = LOCATIONS["village"]
        assert len(village.enemies) == 0  # Врагов нет


class TestMonsterTemplates:
    """Тесты шаблонов монстров."""

    def test_monsters_exist(self):
        """Существование монстров."""
        assert len(MONSTER_TEMPLATES) > 0
        assert "goblin" in MONSTER_TEMPLATES
        assert "dragon" in MONSTER_TEMPLATES

    def test_monster_template_structure(self):
        """Структура шаблона."""
        for key, template in MONSTER_TEMPLATES.items():
            assert template.hp > 0
            assert template.power > 0
            assert template.exp > 0
            assert template.gold_max >= template.gold_min

    def test_monster_level_ranges(self):
        """Диапазоны уровней."""
        for template in MONSTER_TEMPLATES.values():
            assert template.max_level >= template.min_level
            assert template.min_level >= 1

    def test_boss_monsters_exist(self):
        """Существование боссов."""
        assert "goblin_chief" in MONSTER_TEMPLATES
        assert "skeleton_king" in MONSTER_TEMPLATES
        assert "orc_warlord" in MONSTER_TEMPLATES
        assert "ancient_dragon" in MONSTER_TEMPLATES
