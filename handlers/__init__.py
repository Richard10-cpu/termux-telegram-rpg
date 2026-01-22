"""Обработчики бота."""
from .commands import router as commands_router
from .profile import router as profile_router
from .battle_handlers import router as battle_router
from .shop_handlers import router as shop_router
from .map_handlers import router as map_router
from .quest_handlers import router as quest_router
from .rest_handlers import router as rest_router

__all__ = [
    'commands_router',
    'profile_router',
    'battle_router',
    'shop_router',
    'map_router',
    'quest_router',
    'rest_router',
]
