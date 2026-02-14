# 🚂 Деплой Termux RPG Mini App на Railway

## 📋 Пошаговая инструкция

### Шаг 1: Регистрация на Railway

1. Перейдите на https://railway.app
2. Нажмите **"Start a New Project"**
3. Войдите через **GitHub**

### Шаг 2: Подготовка репозитория

Ваш репозиторий уже готов! Файлы созданы:
- ✅ `Procfile` - команда запуска
- ✅ `requirements.txt` - зависимости Python
- ✅ `webapp_server.py` - основной сервер

### Шаг 3: Создание проекта на Railway

1. На dashboard Railway нажмите **"New Project"**
2. Выберите **"Deploy from GitHub repo"**
3. Выберите ваш репозиторий `termux-telegram-rpg`
4. Railway автоматически определит Python проект

### Шаг 4: Настройка переменных окружения

В Railway dashboard:
1. Перейдите в **Variables**
2. Добавьте переменную:
   ```
   PORT=8082
   ```

### Шаг 5: Деплой

Railway автоматически:
1. Установит зависимости из `requirements.txt`
2. Запустит сервер согласно `Procfile`
3. Выдаст публичный HTTPS URL

### Шаг 6: Получение URL

После успешного деплоя:
1. Перейдите в **Settings** → **Domains**
2. Нажмите **"Generate Domain"**
3. Скопируйте URL вида: `https://your-app.up.railway.app`

### Шаг 7: Обновление бота

1. Откройте `.env` файл
2. Измените:
   ```
   WEBAPP_URL=https://your-app.up.railway.app
   ```
3. Перезапустите бота:
   ```bash
   pkill -f bot.py
   python3 bot.py
   ```

### Шаг 8: Регистрация в BotFather

1. Откройте @BotFather в Telegram
2. Отправьте `/mybots`
3. Выберите @Gamerqer_bot
4. Выберите **"Bot Settings"** → **"Menu Button"**
5. Выберите **"Configure menu button"**
6. Отправьте URL: `https://your-app.up.railway.app`
7. Отправьте название: `🎮 Играть`

## ✅ Готово!

Теперь в вашем боте будет кнопка "🎮 Играть" которая откроет Mini App без рекламы ngrok!

## 💡 Преимущества Railway:

- ✅ Бесплатно ($5 кредитов/месяц)
- ✅ Автоматический HTTPS
- ✅ Не засыпает (в отличие от Render)
- ✅ Автодеплой при push в GitHub
- ✅ Логи и мониторинг
- ✅ Никакой рекламы

## 🔧 Полезные команды:

**Посмотреть логи:**
В Railway dashboard → **Deployments** → выберите деплой → **View Logs**

**Перезапустить:**
В Railway dashboard → **Deployments** → **Redeploy**

**Обновить код:**
Просто сделайте `git push` - Railway автоматически передеплоит!

## 📱 Использование:

После настройки откройте бота @Gamerqer_bot и нажмите кнопку меню "🎮 Играть" внизу экрана!
