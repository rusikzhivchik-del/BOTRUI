import random
import json
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

API_TOKEN = "8672741740:AAHDn8SPjl6UazjaK4ZP0zKYZoAYChq--MA"
USERS_FILE = "users.json"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 👑 ТЫ АДМИН
ADMIN_USERNAME = "rusik_tut1"

# ------------------- РАБОТА С ПОЛЬЗОВАТЕЛЯМИ -------------------

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f).get("allowed", [])
    return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump({"allowed": users}, f)

def has_access(username):
    username = username or ""
    return username in load_users()

# ------------------- КОМАНДЫ -------------------

@dp.message(Command(commands=["add"]))
async def add_user(message: Message):
    if message.from_user.username != ADMIN_USERNAME:
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer("Использование: /add username")
        return

    username = args[1].replace("@", "").strip().lower()

    users = load_users()

    if username not in users:
        users.append(username)
        save_users(users)
        await message.answer(f"✅ @{username} добавлен")
    else:
        await message.answer("❌ Уже есть в списке")

@dp.message(Command(commands=["remove"]))
async def remove_user(message: Message):
    if message.from_user.username != ADMIN_USERNAME:
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer("Использование: /remove username")
        return

    username = args[1].replace("@", "").strip().lower()

    users = load_users()

    if username in users:
        users.remove(username)
        save_users(users)
        await message.answer(f"❌ @{username} удалён")
    else:
        await message.answer("❌ Пользователь не найден")

# ------------------- СТАРТ -------------------

@dp.message(Command(commands=["start"]))
async def start(message: Message):
    if not has_access(message.from_user.username):
        await message.answer("⛔ У вас нет доступа к боту")
    else:
        await message.answer("📸 Отправь график — получишь сигнал")

# ------------------- ЛОГИКА БОТА -------------------

signals = ["BUY 🟢", "SELL 🔴"]
durations = [1, 2, 3, 4, 5]

phrases = [
    "📊 Анализ завершён...",
    "🧠 AI подтверждает сигнал",
    "🔍 Найдена точка входа",
    "⚡ Импульс усиливается"
]

patterns = [
    "Поглощение 🔥",
    "Молот 🔨",
    "Доджи ⚪",
    "Харами 🌀"
]

buy_text = [
    "Рынок показывает восходящий импульс.",
    "Цена закрепляется выше уровня.",
    "Покупатели контролируют движение."
]

sell_text = [
    "Рынок уходит вниз.",
    "Продавцы усиливают давление.",
    "Цена пробивает поддержку."
]

confidence = ["78%", "82%", "91%", "69%", "88%"]

# ------------------- ОБРАБОТКА ФОТО -------------------

@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):

    if not has_access(message.from_user.username):
        return  # игнорируем

    await asyncio.sleep(2)

    signal = random.choice(signals)
    duration = random.choice(durations)
    phrase = random.choice(phrases)
    pattern = random.choice(patterns)
    conf = random.choice(confidence)

    if "BUY" in signal:
        analysis = random.choice(buy_text)
    else:
        analysis = random.choice(sell_text)

    text = f"""
{phrase}

💹 Сигнал: {signal}
⏱ Анализ: 1 минута
⏲ Сделка: {duration} мин
📊 Уверенность: {conf}

🕯 Паттерн: {pattern}

🔎 Анализ:
{analysis}

⚠️ Не является финансовой рекомендацией
"""

    await message.answer(text)

# ------------------- ЗАПУСК -------------------

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))