"""Тесты для сервисов (DataRepository, PlayerService)."""
import os
import pytest
from models import Player
from services import DataRepository, PlayerService, get_player_service


class TestDataRepository:
    """Тесты репозитория данных."""

    def test_init_default_data_file(self):
        """Инициализация с файлом по умолчанию."""
        repo = DataRepository()
        assert repo.data_file == 'players_rpg.json'

    def test_init_custom_data_file(self, temp_data_file):
        """Инициализация с кастомным файлом."""
        repo = DataRepository(data_file=temp_data_file)
        assert repo.data_file == temp_data_file

    def test_load_all_file_not_exists(self, test_repository):
        """Загрузка несуществующего файла."""
        data = test_repository.load_all()
        assert data == {}

    def test_load_all_file_exists(self, test_repository_with_data):
        """Загрузка существующего файла."""
        data = test_repository_with_data.load_all()
        assert "123" in data
        assert "456" in data
        assert data["123"]["level"] == 5

    def test_load_all_uses_cache(self, test_repository_with_data):
        """Использование кэша."""
        # Первый вызов загружает данные
        data1 = test_repository_with_data.load_all()
        # Второй вызов должен использовать кэш
        data2 = test_repository_with_data.load_all()
        assert data1 is data2

    def test_load_all_invalid_json_structure(self, tmp_path):
        """Обработка неверной структуры JSON."""
        import json
        invalid_file = tmp_path / "invalid.json"
        with open(invalid_file, 'w') as f:
            json.dump(["not", "a", "dict"], f)

        repo = DataRepository(data_file=str(invalid_file))
        data = repo.load_all()
        assert data == {}

    def test_load_all_json_decode_error(self, tmp_path):
        """Обработка ошибки декодирования JSON."""
        invalid_file = tmp_path / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("not valid json {")

        repo = DataRepository(data_file=str(invalid_file))
        data = repo.load_all()
        assert data == {}

    def test_save_all_success(self, test_repository):
        """Успешное сохранение."""
        data = {"123": {"user_id": 123}}
        result = test_repository.save_all(data)
        assert result is True
        assert os.path.exists(test_repository.data_file)

    def test_save_all_updates_cache(self, test_repository):
        """Обновление кэша при сохранении."""
        data = {"123": {"user_id": 123}}
        test_repository.save_all(data)
        cached = test_repository.load_all()
        assert cached == data

    def test_get_player_data_exists(self, test_repository_with_data):
        """Получение существующего игрока."""
        player_data = test_repository_with_data.get_player_data(123)
        assert player_data is not None
        assert player_data["level"] == 5

    def test_get_player_data_not_exists(self, test_repository):
        """Получение несуществующего игрока."""
        player_data = test_repository.get_player_data(999)
        assert player_data is None

    def test_save_player(self, test_repository):
        """Сохранение игрока."""
        player = Player(user_id=123, level=5, gold=100)
        result = test_repository.save_player(player)
        assert result is True
        data = test_repository.get_player_data(123)
        assert data["user_id"] == 123

    def test_delete_player_exists(self, test_repository_with_data):
        """Удаление существующего игрока."""
        result = test_repository_with_data.delete_player(123)
        assert result is True
        data = test_repository_with_data.get_player_data(123)
        assert data is None

    def test_delete_player_not_exists(self, test_repository):
        """Удаление несуществующего игрока."""
        result = test_repository.delete_player(999)
        assert result is False

    def test_get_all_players(self, test_repository_with_data):
        """Получение всех игроков."""
        all_players = test_repository_with_data.get_all_players()
        assert len(all_players) == 2
        assert "123" in all_players
        assert "456" in all_players

    def test_clear_cache(self, test_repository_with_data):
        """Очистка кэша."""
        # Загружаем данные для заполнения кэша
        test_repository_with_data.load_all()
        assert test_repository_with_data._cache is not None

        # Очищаем кэш
        test_repository_with_data.clear_cache()
        assert test_repository_with_data._cache is None


class TestPlayerService:
    """Тесты сервиса игроков."""

    def test_singleton_pattern(self, test_repository):
        """Проверка паттерна синглтон."""
        PlayerService._instance = None
        service1 = PlayerService(repository=test_repository)
        service2 = PlayerService(repository=test_repository)
        assert service1 is service2

    def test_repository_property(self, fresh_player_service, test_repository):
        """Свойство репозитория."""
        assert fresh_player_service.repository is test_repository

    def test_get_or_create_new_player(self, fresh_player_service):
        """Создание нового игрока."""
        player = fresh_player_service.get_or_create(999)
        assert player.user_id == 999
        assert player.level == 1  # Значение по умолчанию

    def test_get_or_create_existing_player(self, fresh_player_service):
        """Загрузка существующего игрока."""
        # Сначала создаём
        player1 = fresh_player_service.get_or_create(888)
        player1.level = 5
        fresh_player_service.save_player(player1)

        # Теперь загружаем
        player2 = fresh_player_service.get_or_create(888)
        assert player2.level == 5

    def test_get_or_create_uses_cache(self, fresh_player_service):
        """Использование кэша."""
        player1 = fresh_player_service.get_or_create(777)
        player2 = fresh_player_service.get_or_create(777)
        assert player1 is player2

    def test_save_player(self, fresh_player_service):
        """Сохранение игрока."""
        player = fresh_player_service.get_or_create(666)
        player.level = 10
        result = fresh_player_service.save_player(player)
        assert result is True

        # Проверяем через репозиторий
        data = fresh_player_service.repository.get_player_data(666)
        assert data["level"] == 10

    def test_update_player_single_field(self, fresh_player_service):
        """Обновление одного поля."""
        player = fresh_player_service.update_player(555, level=7)
        assert player.level == 7

        # Проверяем сохранение
        data = fresh_player_service.repository.get_player_data(555)
        assert data["level"] == 7

    def test_update_player_multiple_fields(self, fresh_player_service):
        """Обновление нескольких полей."""
        player = fresh_player_service.update_player(
            444,
            level=8,
            gold=500,
            power=25
        )
        assert player.level == 8
        assert player.gold == 500
        assert player.power == 25

    def test_update_player_invalid_field_ignored(self, fresh_player_service):
        """Игнорирование неверного поля."""
        player = fresh_player_service.update_player(
            333,
            level=5,
            invalid_field="should_be_ignored"
        )
        assert player.level == 5
        assert not hasattr(player, "invalid_field")

    def test_invalidate_cache_single_user(self, fresh_player_service):
        """Очистка кэша одного пользователя."""
        player1 = fresh_player_service.get_or_create(222)
        fresh_player_service.invalidate_cache(user_id=222)

        player2 = fresh_player_service.get_or_create(222)
        # Должен быть другой объект после инвалидации
        assert player1 is not player2

    def test_invalidate_cache_all_users(self, fresh_player_service):
        """Очистка кэша всех пользователей."""
        player1 = fresh_player_service.get_or_create(111)
        player2 = fresh_player_service.get_or_create(110)

        fresh_player_service.invalidate_cache()

        # Создаём новый синглтон для проверки
        PlayerService._instance = None
        new_service = PlayerService(repository=fresh_player_service.repository)

        # Кэш должен быть пуст
        assert len(new_service._cache) == 0

    def test_get_top_players_sorting(self, fresh_player_service):
        """Сортировка топа игроков."""
        # Создаём игроков с разными уровнями
        p1 = fresh_player_service.get_or_create(1)
        p1.level = 5
        p1.gold = 100
        fresh_player_service.save_player(p1)

        p2 = fresh_player_service.get_or_create(2)
        p2.level = 10
        p2.gold = 200
        fresh_player_service.save_player(p2)

        p3 = fresh_player_service.get_or_create(3)
        p3.level = 10
        p3.gold = 300
        fresh_player_service.save_player(p3)

        top = fresh_player_service.get_top_players()
        # Сортировка по (level, gold) в обратном порядке
        assert top[0][1].user_id == 3  # level=10, gold=300
        assert top[1][1].user_id == 2  # level=10, gold=200
        assert top[2][1].user_id == 1  # level=5, gold=100

    def test_get_top_players_with_limit(self, fresh_player_service):
        """Лимит топа игроков."""
        for i in range(5):
            p = fresh_player_service.get_or_create(i)
            p.level = i + 1
            fresh_player_service.save_player(p)

        top = fresh_player_service.get_top_players(limit=3)
        assert len(top) == 3

    def test_get_player_service(self):
        """Получение глобального экземпляра."""
        PlayerService._instance = None
        service = get_player_service()
        assert isinstance(service, PlayerService)
