"""Репозиторий для работы с данными игроков."""
import json
import os
from typing import Dict, Optional
from models import Player


class DataRepository:
    """Репозиторий для загрузки и сохранения данных игроков."""

    def __init__(self, data_file: str = 'players_rpg.json'):
        """Инициализировать репозиторий."""
        self.data_file = data_file
        self._cache: Optional[Dict[str, dict]] = None

    def load_all(self) -> Dict[str, dict]:
        """Загрузить все данные из файла."""
        if self._cache is not None:
            return self._cache

        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        print(f"⚠️ Неверная структура данных в {self.data_file}, создаем новую базу")
                        return {}
                    self._cache = data
                    return data
        except json.JSONDecodeError as e:
            print(f"⚠️ Ошибка чтения JSON: {e}")
        except Exception as e:
            print(f"⚠️ Неизвестная ошибка при загрузке: {e}")
        self._cache = {}
        return {}

    def save_all(self, data: Dict[str, dict]) -> bool:
        """Сохранить все данные в файл."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self._cache = data
            return True
        except Exception as e:
            print(f"⚠️ Ошибка при сохранении: {e}")
            return False

    def get_player_data(self, user_id: int) -> Optional[dict]:
        """Получить данные игрока по ID."""
        data = self.load_all()
        return data.get(str(user_id))

    def save_player(self, player: Player) -> bool:
        """Сохранить данные игрока."""
        data = self.load_all()
        data[str(player.user_id)] = player.to_dict()
        return self.save_all(data)

    def delete_player(self, user_id: int) -> bool:
        """Удалить данные игрока."""
        data = self.load_all()
        if str(user_id) in data:
            del data[str(user_id)]
            return self.save_all(data)
        return False

    def get_all_players(self) -> Dict[str, dict]:
        """Получить всех игроков."""
        return self.load_all()

    def clear_cache(self) -> None:
        """Очистить кэш."""
        self._cache = None
