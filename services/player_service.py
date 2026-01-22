"""Сервис управления игроками."""
from typing import Optional
from models import Player
from .data_repository import DataRepository


class PlayerService:
    """Сервис для работы с игроками (синглтон)."""

    _instance: Optional['PlayerService'] = None
    _repository: DataRepository
    _cache: dict[int, Player]

    def __new__(cls, repository: Optional[DataRepository] = None):
        """Создать или получить экземпляр синглтона."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._repository = repository or DataRepository()
            cls._instance._cache = {}
        return cls._instance

    @property
    def repository(self) -> DataRepository:
        """Получить репозиторий."""
        return self._repository

    def get_or_create(self, user_id: int) -> Player:
        """Получить или создать игрока."""
        # Проверяем кэш
        if user_id in self._cache:
            return self._cache[user_id]

        # Проверяем репозиторий
        player_data = self._repository.get_player_data(user_id)

        if player_data is None:
            # Создаем нового игрока
            player = Player(user_id=user_id)
            self._repository.save_player(player)
        else:
            # Загружаем из данных
            player = Player.from_dict(player_data)

        # Кэшируем
        self._cache[user_id] = player
        return player

    def save_player(self, player: Player) -> bool:
        """Сохранить игрока."""
        # Обновляем кэш
        self._cache[player.user_id] = player
        # Сохраняем в репозиторий
        return self._repository.save_player(player)

    def update_player(self, user_id: int, **kwargs) -> Player:
        """Обновить поля игрока и сохранить."""
        player = self.get_or_create(user_id)
        for key, value in kwargs.items():
            if hasattr(player, key):
                setattr(player, key, value)
        self.save_player(player)
        return player

    def invalidate_cache(self, user_id: Optional[int] = None) -> None:
        """Очистить кэш для игрока или всех игроков."""
        if user_id is not None:
            self._cache.pop(user_id, None)
        else:
            self._cache.clear()

    def get_top_players(self, limit: int = 10) -> list[tuple[str, Player]]:
        """Получить топ игроков по уровню и золоту."""
        all_data = self._repository.get_all_players()
        players = []

        for uid, data in all_data.items():
            player = Player.from_dict(data)
            players.append((uid, player))

        # Сортировка по уровню и золоту
        players.sort(key=lambda x: (x[1].level, x[1].gold), reverse=True)
        return players[:limit]


def get_player_service() -> PlayerService:
    """Получить глобальный экземпляр PlayerService."""
    return PlayerService()
