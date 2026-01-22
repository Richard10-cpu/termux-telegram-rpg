"""Сервисы приложения."""
from .data_repository import DataRepository
from .player_service import PlayerService, get_player_service

__all__ = [
    'DataRepository',
    'PlayerService',
    'get_player_service',
]
