import asyncio
import json
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

os.getenv("8005807392:AAGdbyxc6OUPSbZeKF4YkxCVqhk3uqvR_U4")
DATA_FILE = 'players_rpg.json'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Работа с базой данных ---

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

players = load_data()

def get_player(user_id):
    uid = str(user_id)
    if uid not in players:
        players[uid] = {
            "hp": 100, "max_hp": 100, 
            "level": 1, "exp": 0, 
            "gold": 20, "power": 10,
            "inventory": ["Деревянная палка"]
        }
        save_data(players)
    return players[uid]

# --- Клавиатуры ---

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="⚔️ В бой!"), KeyboardButton(text="👤 Профиль")],
    [KeyboardButton(text="🛒 Магазин"), KeyboardButton(text="☕ Отдых (5💰)")]
], resize_keyboard=True)

shop_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🗡️ Купить Меч (50💰)"), KeyboardButton(text="🛡️ Купить Броню (80💰)")],
    [KeyboardButton(text="⬅️ Назад")]
], resize_keyboard=True)

# --- Обработчики ---

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    get_player(message.from_user.id)
    await message.answer("🕹️ Добро пожаловать в Termux RPG! Исследуй мир, сражайся и прокачивайся.", reply_markup=main_kb)

@dp.message(F.text == "👤 Профиль")
async def profile(message: types.Message):
    p = get_player(message.from_user.id)
    inv = ", ".join(p['inventory'])
    text = (f"👤 Уровень: {p['level']}\n"
            f"❤️ HP: {p['hp']}/{p['max_hp']}\n"
            f"⚔️ Сила: {p['power']}\n"
            f"💰 Золото: {p['gold']}\n"
            f"🎒 Инвентарь: {inv}")
    await message.answer(text)

@dp.message(F.text == "🛒 Магазин")
async def shop(message: types.Message):
    await message.answer("Добро пожаловать в лавку торговца! Что купишь?", reply_markup=shop_kb)

@dp.message(F.text == "⬅️ Назад")
async def back(message: types.Message):
    await message.answer("Вы вернулись на главную.", reply_markup=main_kb)

@dp.message(F.text == "🗡️ Купить Меч (50💰)")
async def buy_sword(message: types.Message):
    uid = str(message.from_user.id)
    p = get_player(uid)
    if p['gold'] >= 50:
        if "Стальной меч" not in p['inventory']:
            p['gold'] -= 50
            p['power'] += 15
            p['inventory'].append("Стальной меч")
            save_data(players)
            await message.answer("🗡️ Вы купили Стальной меч! Сила значительно выросла.")
        else:
            await message.answer("❌ У вас уже есть этот меч!")
    else:
        await message.answer("❌ Недостаточно золота!")

@dp.message(F.text == "⚔️ В бой!")
async def battle(message: types.Message):
    uid = str(message.from_user.id)
    p = get_player(uid)

    if p['hp'] <= 15:
        return await message.answer("⚠️ Вы слишком слабы для боя! Отдохните.")

    # Логика противника
    enemy_hp = 20 + (p['level'] * 5)
    damage_to_player = random.randint(5, 12)
    
    # Игрок побеждает
    p['hp'] -= damage_to_player
    reward_gold = random.randint(5, 15)
    p['gold'] += reward_gold
    p['exp'] += 20

    msg = f"⚔️ Вы победили монстра!\n💔 Получено урона: {damage_to_player}\n💰 Найдено золота: {reward_gold}"

    if p['exp'] >= p['level'] * 60:
        p['level'] += 1
        p['max_hp'] += 25
        p['hp'] = p['max_hp']
        p['power'] += 5
        msg += f"\n\n🆙 УРОВЕНЬ ПОВЫШЕН! Теперь вы {p['level']} уровня! Сила и HP выросли."

    save_data(players)
    await message.answer(msg)

@dp.message(F.text == "☕ Отдых (5💰)")
async def heal(message: types.Message):
    uid = str(message.from_user.id)
    p = get_player(uid)
    if p['gold'] >= 5:
        p['gold'] -= 5
        p['hp'] = p['max_hp']
        save_data(players)
        await message.answer("☕ Вы отлично отдохнули и восстановили здоровье!")
    else:
        await message.answer("❌ Не хватает золота!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

