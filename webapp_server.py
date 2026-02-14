"""Веб-сервер для Telegram Mini App."""
import asyncio
import logging
from aiohttp import web
from aiohttp.web import middleware
import hashlib
import hmac
import urllib.parse
import os
from dotenv import load_dotenv
from services import get_player_service

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
player_service = get_player_service()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_telegram_data(init_data: str, bot_token: str) -> dict | None:
    """Проверка подлинности данных от Telegram Web App."""
    try:
        # Парсим init_data
        data = dict(urllib.parse.parse_qsl(init_data))

        # В режиме разработки можем пропустить валидацию
        if not init_data:
            return {'user': {'id': 1, 'first_name': 'Test User'}}

        # Извлекаем hash
        received_hash = data.pop('hash', None)
        if not received_hash:
            return None

        # Создаем data_check_string
        data_check_arr = [f"{k}={v}" for k, v in sorted(data.items())]
        data_check_string = '\n'.join(data_check_arr)

        # Вычисляем секретный ключ
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()

        # Вычисляем hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        # Сравниваем
        if calculated_hash != received_hash:
            return None

        # Парсим user
        import json
        user_data = json.loads(data.get('user', '{}'))
        return {'user': user_data}

    except Exception as e:
        logger.error(f"Ошибка валидации: {e}")
        return None


@middleware
async def cors_middleware(request, handler):
    """Middleware для CORS."""
    # Обработка preflight запросов
    if request.method == 'OPTIONS':
        response = web.Response()
    else:
        response = await handler(request)

    # Добавляем CORS заголовки
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@middleware
async def auth_middleware(request, handler):
    """Middleware для аутентификации."""
    # Пропускаем статические файлы
    if request.path.startswith('/static/') or request.path == '/' or request.path == '/health' or request.path == '/healthz':
        return await handler(request)

    # Для API проверяем заголовок Authorization
    if request.path.startswith('/api/'):
        auth_header = request.headers.get('Authorization', '')

        # В режиме разработки
        if not auth_header:
            request['user_id'] = 1  # Тестовый пользователь
        else:
            validated = validate_telegram_data(auth_header, TELEGRAM_BOT_TOKEN)
            if not validated:
                return web.json_response({'error': 'Unauthorized'}, status=401)
            request['user_id'] = validated['user']['id']

    return await handler(request)


# Handlers

async def index(request):
    """Главная страница Mini App."""
    with open('webapp/templates/index.html', 'r', encoding='utf-8') as f:
        return web.Response(text=f.read(), content_type='text/html')


async def test_page(request):
    """Тестовая страница для диагностики."""
    with open('webapp/templates/test.html', 'r', encoding='utf-8') as f:
        return web.Response(text=f.read(), content_type='text/html')


async def get_player(request):
    """Получить данные игрока."""
    try:
        user_id = request['user_id']
        player = player_service.get_or_create(user_id)

        # Преобразуем в словарь
        # Вычисляем опыт до следующего уровня
        exp_to_next_level = player.level * 100

        player_data = {
            'id': player.user_id,
            'name': f'Герой #{player.user_id}',  # Генерируем имя
            'level': player.level,
            'hp': player.hp,
            'max_hp': player.max_hp,
            'mana': player.mana,
            'max_mana': player.max_mana,
            'power': player.power,
            'gold': player.gold,
            'exp': player.exp,
            'exp_to_next_level': exp_to_next_level,
            'location': player.location,
            'inventory': player.inventory
        }

        return web.json_response(player_data)

    except Exception as e:
        logger.error(f"Ошибка получения игрока: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def travel(request):
    """Переместиться в локацию."""
    try:
        user_id = request['user_id']
        data = await request.json()
        location = data.get('location')

        if not location:
            return web.json_response({'error': 'Location required'}, status=400)

        player = player_service.get_or_create(user_id)
        player.location = location
        player_service.save(player)

        return web.json_response({'success': True, 'location': location})

    except Exception as e:
        logger.error(f"Ошибка перемещения: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def fight(request):
    """Сразиться с врагом."""
    try:
        user_id = request['user_id']
        data = await request.json()
        enemy_key = data.get('enemy')
        action = data.get('action', 'attack')

        if not enemy_key:
            return web.json_response({'error': 'Enemy required'}, status=400)

        player = player_service.get_or_create(user_id)

        # TODO: Реализовать полноценную боевую систему
        # Пока возвращаем заглушку

        return web.json_response({
            'success': True,
            'action': action,
            'player_hp': player.hp,
            'enemy_hp': 50
        })

    except Exception as e:
        logger.error(f"Ошибка боя: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def rest(request):
    """Отдохнуть."""
    try:
        user_id = request['user_id']
        player = player_service.get_or_create(user_id)

        if player.location != 'village':
            return web.json_response({'error': 'Can only rest in village'}, status=400)

        cost = 20
        if player.gold < cost:
            return web.json_response({'error': 'Not enough gold'}, status=400)

        player.gold -= cost
        player.hp = player.max_hp
        player.mana = player.max_mana
        player_service.save(player)

        return web.json_response({
            'success': True,
            'hp': player.hp,
            'mana': player.mana,
            'gold': player.gold
        })

    except Exception as e:
        logger.error(f"Ошибка отдыха: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def get_inventory(request):
    """Получить инвентарь."""
    try:
        user_id = request['user_id']
        player = player_service.get_or_create(user_id)

        return web.json_response({
            'inventory': player.inventory
        })

    except Exception as e:
        logger.error(f"Ошибка получения инвентаря: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def buy_item(request):
    """Купить предмет."""
    try:
        user_id = request['user_id']
        data = await request.json()
        item_id = data.get('item_id')

        if not item_id:
            return web.json_response({'error': 'Item ID required'}, status=400)

        player = player_service.get_or_create(user_id)

        # TODO: Реализовать систему покупки

        return web.json_response({'success': True})

    except Exception as e:
        logger.error(f"Ошибка покупки: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def healthcheck(request):
    """Health check endpoint."""
    return web.json_response({
        'status': 'ok',
        'service': 'termux-rpg-miniapp',
        'version': '1.0.0'
    })


def setup_routes(app):
    """Настроить маршруты."""
    # Главная страница
    app.router.add_get('/', index)
    app.router.add_get('/test', test_page)  # Тестовая страница

    # Health check
    app.router.add_get('/health', healthcheck)
    app.router.add_get('/healthz', healthcheck)  # Kubernetes style

    # API endpoints
    app.router.add_get('/api/player', get_player)
    app.router.add_post('/api/travel', travel)
    app.router.add_post('/api/fight', fight)
    app.router.add_post('/api/rest', rest)
    app.router.add_get('/api/inventory', get_inventory)
    app.router.add_post('/api/buy', buy_item)

    # Статические файлы
    app.router.add_static('/static/', path='webapp/static', name='static')


async def init_app():
    """Инициализация приложения."""
    app = web.Application(middlewares=[cors_middleware, auth_middleware])
    setup_routes(app)
    return app


async def main():
    """Запуск сервера."""
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    logger.info(f"🚀 Mini App сервер запущен на http://0.0.0.0:{port}")
    logger.info("📱 Откройте в Telegram Web App или браузере")

    # Держим сервер запущенным
    await asyncio.Event().wait()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Сервер остановлен")
