#!/bin/bash

# Останов всех предыдущих экземпляров
pkill -f webapp_server.py
sleep 1

# Очистка кэша Python
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# Активация venv и запуск
source venv/bin/activate
export PORT=8888
python3 -u webapp_server.py
