# 🎮 TERMUX RPG MINI APP - ПОЛНОЕ РУКОВОДСТВО

## 🌟 Что такое Mini App?

Telegram Mini App - это полноценное веб-приложение, которое открывается прямо в Telegram с:
- 🎨 Красивым современным интерфейсом
- ⚔️ Визуализацией боёв в реальном времени
- 🗺️ Интерактивной картой мира
- 📊 Подробной статистикой персонажа
- 🎒 Удобным управлением инвентарём

---

## 📁 Структура проекта

```
termux-telegram-rpg/
├── bot.py                 # Telegram бот (текстовый интерфейс)
├── webapp_server.py       # Веб-сервер для Mini App
└── webapp/
    ├── templates/
    │   └── index.html     # Главная страница
    └── static/
        ├── css/
        │   └── style.css  # Стили
        └── js/
            └── app.js     # Логика приложения
```

---

## 🚀 БЫСТРЫЙ СТАРТ

### Шаг 1: Установка зависимостей

```bash
pip install aiohttp python-dotenv aiogram
```

### Шаг 2: Настройка .env файла

Добавьте в `.env`:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://your-domain.com
```

### Шаг 3: Запуск веб-сервера

```bash
python3 webapp_server.py
```

Сервер запустится на `http://0.0.0.0:8080`

### Шаг 4: Запуск бота (в другом терминале)

```bash
python3 bot.py
```

### Шаг 5: Открытие Mini App

В Telegram отправьте боту команду:
```
/webapp
```

Нажмите на кнопку "🎮 Открыть Mini App"

---

## 🌐 ДЕПЛОЙ НА СЕРВЕР

### Вариант 1: Локальный тестовый сервер (ngrok)

1. Установите ngrok:
```bash
# Скачайте с https://ngrok.com/download
```

2. Запустите ngrok:
```bash
ngrok http 8080
```

3. Скопируйте HTTPS URL (например: `https://abc123.ngrok.io`)

4. Обновите `.env`:
```env
WEBAPP_URL=https://abc123.ngrok.io
```

5. Перезапустите бота

### Вариант 2: VPS/Cloud сервер

#### На Ubuntu/Debian:

1. Установите зависимости:
```bash
sudo apt update
sudo apt install python3 python3-pip nginx
pip3 install aiohttp python-dotenv aiogram
```

2. Настройте nginx (создайте `/etc/nginx/sites-available/rpg-webapp`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

3. Активируйте конфигурацию:
```bash
sudo ln -s /etc/nginx/sites-available/rpg-webapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

4. Установите SSL сертификат (Let's Encrypt):
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

5. Создайте systemd сервис (`/etc/systemd/system/rpg-webapp.service`):
```ini
[Unit]
Description=Termux RPG Mini App
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/termux-telegram-rpg
ExecStart=/usr/bin/python3 /path/to/termux-telegram-rpg/webapp_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

6. Запустите сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable rpg-webapp
sudo systemctl start rpg-webapp
```

### Вариант 3: Heroku

1. Создайте `Procfile`:
```
web: python3 webapp_server.py
worker: python3 bot.py
```

2. Обновите `webapp_server.py` для использования переменной `PORT`:
```python
port = int(os.getenv('PORT', 8080))
site = web.TCPSite(runner, '0.0.0.0', port)
```

3. Деплой:
```bash
heroku create your-app-name
git push heroku main
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set WEBAPP_URL=https://your-app-name.herokuapp.com
```

---

## 🔧 НАСТРОЙКА TELEGRAM БОТА

### 1. Регистрация Mini App

Отправьте @BotFather:
```
/newapp
```

Выберите вашего бота, укажите:
- Название: Termux RPG
- Описание: Текстовая RPG с элементами фэнтези
- Фото: загрузите иконку
- GIF/Video: (опционально)
- URL: `https://your-domain.com`

### 2. Настройка Menu Button

```
/setmenubutton
```

Выберите бота и укажите:
- Button text: 🎮 Играть
- URL: `https://your-domain.com`

---

## 📱 ФУНКЦИОНАЛ MINI APP

### ✅ Уже реализовано:

#### 1. **Профиль игрока**
- Отображение имени и уровня
- Прогресс HP, маны и опыта
- Статистика (сила, золото)
- Текущая локация
- Быстрые действия (отдых, достижения, питомцы)

#### 2. **Карта мира**
- 8 локаций с иконками
- Индикатор текущей локации
- Рекомендуемый уровень для каждой
- Перемещение по клику

#### 3. **Боевая система**
- Выбор врага из списка
- Визуализация боя с анимациями
- HP бары для игрока и врага
- Лог боя в реальном времени
- Действия: атака, магия, предметы, побег
- Система наград (золото, опыт)
- Повышение уровня

#### 4. **Инвентарь**
- Сетка предметов
- Фильтрация по типу (всё, оружие, броня, зелья)
- Подробная информация о предметах

#### 5. **Магазин**
- Категории товаров
- Отображение баланса
- Система покупок

#### 6. **Адаптивный дизайн**
- Работает на всех устройствах
- Оптимизирован для мобильных
- Поддержка тёмной/светлой темы Telegram

### 🔄 В разработке:

- Полная интеграция с магией
- Система использования предметов
- Достижения и питомцы в UI
- Казино и мини-игры
- Крафт интерфейс
- Сюжетные события

---

## 🎨 КАСТОМИЗАЦИЯ

### Изменение цветовой схемы

Отредактируйте `webapp/static/css/style.css`:

```css
:root {
    --primary: #3390ec;      /* Основной цвет */
    --danger: #e53935;       /* Опасность/HP */
    --success: #43a047;      /* Успех */
    --warning: #fb8c00;      /* Предупреждение */
}
```

### Добавление новых страниц

1. Добавьте новый `<section>` в `index.html`
2. Создайте кнопку в навбаре
3. Добавьте обработчик в `app.js`

---

## 🐛 ОТЛАДКА

### Проверка логов сервера:

```bash
# Смотреть логи в реальном времени
python3 webapp_server.py

# Или если запущен как сервис
sudo journalctl -u rpg-webapp -f
```

### Проверка в браузере:

1. Откройте DevTools (F12)
2. Перейдите на вкладку Console
3. Проверьте Network для API запросов

### Частые проблемы:

**1. Mini App не открывается**
- Проверьте, что WEBAPP_URL правильный и доступен
- Убедитесь, что используется HTTPS (для продакшена)
- Проверьте настройки бота в BotFather

**2. Данные не загружаются**
- Проверьте, что веб-сервер запущен
- Проверьте API endpoints в Network tab
- Убедитесь, что токен бота правильный

**3. Ошибки авторизации**
- В режиме разработки используется заглушка (user_id=1)
- Для продакшена нужна валидация initData

---

## 📊 API ENDPOINTS

### GET /api/player
Получить данные игрока

**Response:**
```json
{
  "id": 123456,
  "name": "Герой",
  "level": 15,
  "hp": 250,
  "max_hp": 300,
  "mana": 100,
  "max_mana": 150,
  "power": 45,
  "gold": 1500,
  "exp": 750,
  "exp_to_next_level": 1000,
  "location": "forest",
  "inventory": ["Меч", "Зелье здоровья"]
}
```

### POST /api/travel
Переместиться в локацию

**Request:**
```json
{
  "location": "mountain"
}
```

**Response:**
```json
{
  "success": true,
  "location": "mountain"
}
```

### POST /api/fight
Атаковать врага

**Request:**
```json
{
  "enemy": "dragon",
  "action": "attack"
}
```

**Response:**
```json
{
  "success": true,
  "action": "attack",
  "player_hp": 200,
  "enemy_hp": 50
}
```

### POST /api/rest
Отдохнуть в деревне

**Response:**
```json
{
  "success": true,
  "hp": 300,
  "mana": 150,
  "gold": 1480
}
```

---

## 🔐 БЕЗОПАСНОСТЬ

### В разработке:
- Используется заглушка авторизации (user_id=1)
- Можно тестировать в браузере напрямую

### В продакшене:
- Обязательна валидация `initData` от Telegram
- Используется HTTPS
- Проверка токена бота для каждого запроса

### Включение валидации:

В `webapp_server.py` раскомментируйте проверку:
```python
# Для продакшена
if not auth_header:
    return web.json_response({'error': 'Unauthorized'}, status=401)
```

---

## 📈 ПРОИЗВОДИТЕЛЬНОСТЬ

### Оптимизация:

1. **Кэширование статических файлов**
```python
app.router.add_static('/static/', path='webapp/static',
                      name='static', show_index=True)
```

2. **Сжатие ответов**
```python
from aiohttp import web
import aiohttp_cors

# Добавить middleware для gzip
```

3. **CDN для статики**
Разместите CSS/JS на CDN (Cloudflare, AWS CloudFront)

---

## 🎯 СЛЕДУЮЩИЕ ШАГИ

1. ✅ Запустите веб-сервер локально
2. ✅ Протестируйте в браузере: `http://localhost:8080`
3. ✅ Настройте ngrok для тестирования в Telegram
4. ✅ Зарегистрируйте Mini App в @BotFather
5. ✅ Протестируйте через команду `/webapp`
6. 🔄 Доработайте функционал под свои нужды
7. 🚀 Задеплойте на VPS/облако
8. 🌟 Запустите в продакшен!

---

## 💡 ПОЛЕЗНЫЕ ССЫЛКИ

- [Telegram Mini Apps документация](https://core.telegram.org/bots/webapps)
- [aiohttp документация](https://docs.aiohttp.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [ngrok](https://ngrok.com/)
- [Let's Encrypt](https://letsencrypt.org/)

---

## 🤝 ПОДДЕРЖКА

Если возникли вопросы:
1. Проверьте логи сервера и бота
2. Откройте DevTools в браузере
3. Проверьте настройки в `.env`
4. Убедитесь, что все порты открыты

---

**Приятной игры! 🎮✨**
