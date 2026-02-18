#!/bin/bash
set -e

echo "🚀 Starting Termux RPG Mini App..."
echo "PORT: ${PORT:-8080}"

# Запуск сервера
exec python3 webapp_server.py
