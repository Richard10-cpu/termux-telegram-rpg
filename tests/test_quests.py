"""Тесты для системы квестов."""
import pytest
from datetime import datetime
from freezegun import freeze_time
from models import Player, DailyQuest, StoryProgress
from game_logic.quests import (
    get_today,
    update_daily_quest,
    increment_kills,
    can_claim_reward,
    claim_daily_reward,
    format_story_quest,
    format_daily_quest,
    format_quest_status,
    QuestConstants
)


class TestQuestHelpers:
    """Тесты вспомогательных функций."""

    @freeze_time("2024-01-15")
    def test_get_today(self):
        """Получение текущей даты."""
        assert get_today() == "2024-01-15"


class TestUpdateDailyQuest:
    """Тесты обновления дневного квеста."""

    @freeze_time("2024-01-15")
    def test_update_same_day_no_change(self, test_player):
        """Обновление в тот же день."""
        quest = DailyQuest(date="2024-01-15", kills=3, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        update_daily_quest(test_player)

        assert test_player.quests["daily"].kills == 3  # Не изменилось

    @freeze_time("2024-01-16")
    def test_update_new_day_resets(self, test_player):
        """Сброс квеста на новый день."""
        quest = DailyQuest(date="2024-01-15", kills=5, target=5, reward_claimed=True)
        test_player.quests = {"daily": quest}

        update_daily_quest(test_player)

        assert test_player.quests["daily"].date == "2024-01-16"
        assert test_player.quests["daily"].kills == 0
        assert test_player.quests["daily"].reward_claimed is False

    @freeze_time("2024-01-15")
    def test_update_creates_default_quest(self, test_player):
        """Обновление существующего квеста."""
        # test_player уже имеет quests по умолчанию из Player
        update_daily_quest(test_player)

        assert "daily" in test_player.quests
        assert test_player.quests["daily"].target == QuestConstants.DAILY_TARGET


class TestIncrementKills:
    """Тесты увеличения счётчика убийств."""

    @freeze_time("2024-01-15")
    def test_increment_kills_single(self, test_player):
        """Увеличение на 1."""
        quest = DailyQuest(date="2024-01-15", kills=0, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        completed, message = increment_kills(test_player, 1)

        assert test_player.quests["daily"].kills == 1
        assert completed is False
        assert message is None

    @freeze_time("2024-01-15")
    def test_increment_kills_multiple(self, test_player):
        """Увеличение на несколько."""
        quest = DailyQuest(date="2024-01-15", kills=2, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        completed, message = increment_kills(test_player, 2)

        assert test_player.quests["daily"].kills == 4
        assert completed is False

    @freeze_time("2024-01-15")
    def test_increment_kills_already_completed(self, test_player):
        """Увеличение уже выполненного квеста."""
        quest = DailyQuest(date="2024-01-15", kills=5, target=5, reward_claimed=True)
        test_player.quests = {"daily": quest}

        completed, message = increment_kills(test_player, 1)

        # Квест всё ещё выполнен, но kills увеличивается
        assert test_player.quests["daily"].kills == 6

    @freeze_time("2024-01-15")
    def test_increment_kills_updates_daily_first(self, test_player):
        """Обновление квеста перед инкрементом."""
        # Устаревшая дата
        quest = DailyQuest(date="2024-01-14", kills=3, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        increment_kills(test_player, 1)

        # Дата должна обновиться
        assert test_player.quests["daily"].date == "2024-01-15"


class TestCanClaimReward:
    """Тесты проверки возможности получения награды."""

    def test_can_claim_not_claimed_and_complete(self, test_player):
        """Можно получить награду."""
        quest = DailyQuest(date="2024-01-15", kills=5, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        can_claim, message = can_claim_reward(test_player)

        assert can_claim is True
        assert message == ""

    def test_can_claim_already_claimed(self, test_player):
        """Уже получена награда."""
        quest = DailyQuest(date="2024-01-15", kills=5, target=5, reward_claimed=True)
        test_player.quests = {"daily": quest}

        can_claim, message = can_claim_reward(test_player)

        assert can_claim is False
        assert "уже получили" in message.lower()

    def test_can_claim_not_complete(self, test_player):
        """Квест не выполнен."""
        quest = DailyQuest(date="2024-01-15", kills=2, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        can_claim, message = can_claim_reward(test_player)

        assert can_claim is False
        assert "ещё не выполнен" in message.lower()


class TestClaimDailyReward:
    """Тесты получения награды."""

    def test_claim_reward_success(self, test_player):
        """Успешное получение награды."""
        quest = DailyQuest(date="2024-01-15", kills=5, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        old_gold = test_player.gold
        old_exp = test_player.exp

        success, message = claim_daily_reward(test_player)

        assert success is True
        assert test_player.gold == old_gold + QuestConstants.DAILY_REWARD_GOLD
        assert test_player.exp == old_exp + QuestConstants.DAILY_REWARD_EXP
        assert test_player.quests["daily"].reward_claimed is True

    def test_claim_reward_not_complete(self, test_player):
        """Попытка получения невыполненного квеста."""
        quest = DailyQuest(date="2024-01-15", kills=2, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        success, message = claim_daily_reward(test_player)

        assert success is False

    def test_claim_reward_already_claimed(self, test_player):
        """Повторное получение."""
        quest = DailyQuest(date="2024-01-15", kills=5, target=5, reward_claimed=True)
        test_player.quests = {"daily": quest}

        success, message = claim_daily_reward(test_player)

        assert success is False


class TestFormatStoryQuest:
    """Тесты форматирования сюжетного квеста."""

    def test_format_story_quest_with_chapter(self, test_player):
        """Форматирование с активной главой."""
        test_player.story_progress = StoryProgress(current_chapter=1)
        test_player.level = 1
        test_player.location = "forest"  # Глава 1 требует лес

        text = format_story_quest(test_player)

        assert "СЮЖЕТНЫЙ КВЕСТ" in text
        assert "Пробуждение" in text
        assert "Награда за главу" in text

    def test_format_story_quest_all_completed(self, test_player):
        """Форматирование при завершённом сюжете."""
        test_player.story_progress = StoryProgress(current_chapter=99)

        text = format_story_quest(test_player)

        assert "Все сюжетные главы пройдены" in text

    def test_format_story_quest_level_requirement(self, test_player):
        """Отображение требования уровня."""
        test_player.story_progress = StoryProgress(current_chapter=2)
        test_player.level = 1

        text = format_story_quest(test_player)

        assert "Требуется уровень" in text


class TestFormatDailyQuest:
    """Тесты форматирования дневного квеста."""

    @freeze_time("2024-01-15")
    def test_format_daily_quest_in_progress(self, test_player):
        """Квест в процессе."""
        quest = DailyQuest(date="2024-01-15", kills=2, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        text = format_daily_quest(test_player)

        assert "ЕЖЕДНЕВНЫЙ КВЕСТ" in text
        assert "Прогресс:" in text
        assert "Осталось:" in text

    @freeze_time("2024-01-15")
    def test_format_daily_quest_completed(self, test_player):
        """Выполненный квест."""
        quest = DailyQuest(date="2024-01-15", kills=5, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        text = format_daily_quest(test_player)

        assert "Выполнено! Заберите награду" in text

    @freeze_time("2024-01-15")
    def test_format_daily_quest_reward_claimed(self, test_player):
        """С полученной наградой."""
        quest = DailyQuest(date="2024-01-15", kills=5, target=5, reward_claimed=True)
        test_player.quests = {"daily": quest}

        text = format_daily_quest(test_player)

        assert "Награда получена" in text

    def test_format_quest_status_combined(self, test_player):
        """Комбинированный статус."""
        test_player.story_progress = StoryProgress(current_chapter=1)
        quest = DailyQuest(date=datetime.now().strftime("%Y-%m-%d"), kills=2, target=5, reward_claimed=False)
        test_player.quests = {"daily": quest}

        text = format_quest_status(test_player)

        assert "СЮЖЕТНЫЙ КВЕСТ" in text
        assert "ЕЖЕДНЕВНЫЙ КВЕСТ" in text
