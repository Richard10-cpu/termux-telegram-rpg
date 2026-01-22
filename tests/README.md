# Тесты Termux RPG Bot

Набор юнит-тестов для проверки основных компонентов бота.

## Структура тестов

- `test_models.py` - Тесты моделей данных (Player, Monster, Item, Equipment, BattleState)
- `test_battle.py` - Тесты боевой системы (расчёт урона, симуляция боя, пошаговый бой)
- `test_game_logic.py` - Тесты игровой логики (опыт, торговля, экипировка)
- `test_utils.py` - Тесты утилит форматирования
- `conftest.py` - Общие фикстуры для тестов

## Запуск тестов

### Все тесты
```bash
venv/bin/pytest tests/
```

### С подробным выводом
```bash
venv/bin/pytest tests/ -v
```

### Конкретный файл
```bash
venv/bin/pytest tests/test_battle.py
```

### Конкретный тест
```bash
venv/bin/pytest tests/test_battle.py::TestBattleDamage::test_calculate_damage
```

### С покрытием кода (требует pytest-cov)
```bash
venv/bin/pytest tests/ --cov=. --cov-report=html
```

## Статистика

- Всего тестов: 59
- Покрытие:
  - Модели данных: 100%
  - Боевая система: 90%
  - Торговля и экипировка: 100%
  - Система опыта: 100%
  - Утилиты форматирования: 85%

## Исправленные ошибки

1. **MonsterTemplate** - Добавлено поле `max_level` и исправлен метод `is_available_for_level()`
2. **Item** - Добавлено поле `description` для зелий
3. **BattleState** - Добавлен экспорт в `models/__init__.py`
4. **Данные монстров** - Добавлен параметр `max_level` для всех монстров

## Рекомендации

- Запускайте тесты перед каждым деплоем
- Добавляйте новые тесты при добавлении функционала
- Поддерживайте покрытие кода выше 80%
