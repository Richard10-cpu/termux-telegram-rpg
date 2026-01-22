FROM python:3.12-slim

WORKDIR /app

# Установ зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать код бота
COPY . .

# Переменная окружения для файла данных (в корне проекта, не в modules/data!)
ENV DATA_FILE=/app/players_rpg.json

CMD ["python", "bot.py"]
