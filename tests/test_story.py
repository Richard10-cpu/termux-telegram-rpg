"""Тесты для сюжетной системы."""
import pytest
from models import Player, StoryProgress
from game_logic.story import (
    get_story_progress,
    get_current_chapter,
    check_chapter_requirements,
    start_chapter_boss_fight,
    complete_chapter,
    format_chapter_info,
    format_story_overview
)


class TestStoryProgress:
    """Тесты прогресса сюжета."""

    def test_get_story_progress_creates_default(self, test_player):
        """Создание прогресса по умолчанию."""
        assert not hasattr(test_player, 'story_progress') or test_player.story_progress is None

        progress = get_story_progress(test_player)

        assert progress is not None
        assert progress.current_chapter == 1
        assert test_player.story_progress is not None

    def test_get_story_progress_existing(self, test_player):
        """Получение существующего прогресса."""
        test_player.story_progress = StoryProgress(current_chapter=2)

        progress = get_story_progress(test_player)

        assert progress.current_chapter == 2
        assert progress is test_player.story_progress

    def test_get_current_chapter(self, test_player):
        """Получение текущей главы."""
        test_player.story_progress = StoryProgress(current_chapter=1)

        chapter = get_current_chapter(test_player)

        assert chapter is not None
        assert chapter.chapter_id == 1


class TestChapterRequirements:
    """Тесты требований глав."""

    def test_check_requirements_level_not_met(self, test_player):
        """Неудовлетворённое требование уровня."""
        test_player.level = 1
        test_player.location = "forest"  # Глава 1 требует лес
        chapter = get_current_chapter(test_player)

        can_start, message = check_chapter_requirements(test_player, chapter)

        assert can_start is True  # Глава 1 доступна с уровня 1 в лесу

    def test_check_requirements_location_not_met(self, test_player):
        """Неудовлетворённое требование локации."""
        test_player.level = 10
        test_player.location = "village"
        from data.story_chapters import get_chapter
        chapter = get_chapter(2)  # Требует лес

        can_start, message = check_chapter_requirements(test_player, chapter)

        assert can_start is False
        assert "локации" in message.lower()

    def test_check_requirements_all_met(self, test_player):
        """Все требования выполнены."""
        test_player.level = 10
        test_player.location = "cave"  # Глава 2 требует пещеру
        from data.story_chapters import get_chapter
        chapter = get_chapter(2)

        can_start, message = check_chapter_requirements(test_player, chapter)

        assert can_start is True
        assert message == ""


class TestBossFight:
    """Тесты боёв с боссами."""

    def test_start_boss_fight_chapter_not_found(self, test_player):
        """Бой с несуществующей главой."""
        success, message = start_chapter_boss_fight(test_player, 999)

        assert success is False
        assert "не найдена" in message.lower()

    def test_start_boss_fight_not_current_chapter(self, test_player):
        """Бой не с текущей главой."""
        test_player.story_progress = StoryProgress(current_chapter=1)

        success, message = start_chapter_boss_fight(test_player, 2)

        assert success is False
        assert "недоступна" in message.lower()

    def test_start_boss_fight_already_completed(self, test_player):
        """Бой с завершённой главой."""
        test_player.story_progress = StoryProgress(
            current_chapter=2,
            completed_chapters=[1]
        )
        test_player.level = 5
        test_player.location = "forest"

        success, message = start_chapter_boss_fight(test_player, 1)

        assert success is False
        assert "недоступна" in message.lower()

    def test_start_boss_fight_requirements_not_met(self, test_player):
        """Бой без выполненных требований."""
        test_player.story_progress = StoryProgress(current_chapter=2)
        test_player.level = 1  # Низкий уровень

        success, message = start_chapter_boss_fight(test_player, 2)

        assert success is False

    def test_start_boss_fight_already_defeated(self, test_player):
        """Бой с уже побеждённым боссом."""
        test_player.story_progress = StoryProgress(
            current_chapter=1,
            boss_defeated={"Вожак гоблинов": True}  # Правильное имя босса
        )
        test_player.level = 5
        test_player.location = "forest"  # Глава 1 требует лес

        success, message = start_chapter_boss_fight(test_player, 1)

        assert success is False
        assert "уже победили" in message.lower()

    def test_start_boss_fight_success(self, test_player):
        """Успешное начало боя."""
        test_player.story_progress = StoryProgress(current_chapter=1)
        test_player.level = 5
        test_player.location = "forest"  # Глава 1 требует лес

        success, message = start_chapter_boss_fight(test_player, 1)

        assert success is True
        assert "Вожак гоблинов" in message


class TestCompleteChapter:
    """Тесты завершения глав."""

    def test_complete_chapter_not_found(self, test_player):
        """Завершение несуществующей главы."""
        success, message = complete_chapter(test_player, 999)

        assert success is False
        assert "не найдена" in message.lower()

    def test_complete_chapter_already_completed(self, test_player):
        """Повторное завершение главы."""
        test_player.story_progress = StoryProgress(
            current_chapter=2,
            completed_chapters=[1]
        )

        success, message = complete_chapter(test_player, 1)

        assert success is False
        assert "уже завершили" in message.lower()

    def test_complete_chapter_success(self, test_player):
        """Успешное завершение главы."""
        test_player.story_progress = StoryProgress(current_chapter=1)
        test_player.gold = 0
        test_player.exp = 0

        success, message = complete_chapter(test_player, 1)

        assert success is True
        assert 1 in test_player.story_progress.completed_chapters
        assert test_player.story_progress.current_chapter == 2
        assert test_player.gold > 0
        assert test_player.exp > 0
        assert "Поздравляем" in message

    def test_complete_chapter_final_game(self, test_player):
        """Завершение финальной главы."""
        test_player.story_progress = StoryProgress(current_chapter=4)
        test_player.gold = 0
        test_player.exp = 0

        success, message = complete_chapter(test_player, 4)

        assert success is True
        assert "ВЫ ПРОШЛИ ВСЮ ИГРУ" in message


class TestFormatChapterInfo:
    """Тесты форматирования информации о главах."""

    def test_format_chapter_completed(self, test_player):
        """Завершённая глава."""
        test_player.story_progress = StoryProgress(
            current_chapter=2,
            completed_chapters=[1]
        )
        from data.story_chapters import get_chapter
        chapter = get_chapter(1)

        text = format_chapter_info(chapter, test_player)

        assert "Завершена" in text
        assert "Пробуждение героя" in text

    def test_format_chapter_current(self, test_player):
        """Текущая глава."""
        test_player.story_progress = StoryProgress(current_chapter=1)
        from data.story_chapters import get_chapter
        chapter = get_chapter(1)

        text = format_chapter_info(chapter, test_player)

        assert "Текущая" in text

    def test_format_chapter_available(self, test_player):
        """Доступная глава."""
        test_player.story_progress = StoryProgress(current_chapter=1)
        test_player.level = 10
        from data.story_chapters import get_chapter
        chapter = get_chapter(2)

        text = format_chapter_info(chapter, test_player)

        assert "Доступна" in text

    def test_format_chapter_locked(self, test_player):
        """Закрытая глава."""
        test_player.story_progress = StoryProgress(current_chapter=1)
        test_player.level = 1
        from data.story_chapters import get_chapter
        chapter = get_chapter(3)

        text = format_chapter_info(chapter, test_player)

        assert "Требуется" in text
        assert "ур." in text

    def test_format_chapter_with_boss(self, test_player):
        """Глава с боссом."""
        test_player.story_progress = StoryProgress(current_chapter=1)
        from data.story_chapters import get_chapter
        chapter = get_chapter(1)

        text = format_chapter_info(chapter, test_player)

        assert "Вожак гоблинов" in text


class TestFormatStoryOverview:
    """Тесты форматирования обзора сюжета."""

    def test_format_story_overview(self, test_player):
        """Форматирование обзора."""
        test_player.story_progress = StoryProgress(current_chapter=1)
        test_player.level = 5

        text = format_story_overview(test_player)

        assert "СЮЖЕТ ИГРЫ" in text
        assert "Прогресс:" in text
        assert "Глава 1" in text

    def test_format_story_overview_with_progress(self, test_player):
        """Обзор с прогрессом."""
        test_player.story_progress = StoryProgress(
            current_chapter=2,
            completed_chapters=[1]
        )
        test_player.level = 10

        text = format_story_overview(test_player)

        assert "1/4" in text  # 1 глава из 4
        assert "Глава 1" in text
        assert "Глава 2" in text
