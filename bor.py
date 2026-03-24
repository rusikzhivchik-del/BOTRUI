import os
import random
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command

# ------------------- НАСТРОЙКИ -------------------
API_TOKEN = os.getenv("BOT_TOKEN")  # токен из ENV
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")  # username без @

# ------------------- ИНИЦИАЛИЗАЦИЯ -------------------
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ------------------- ГЛОБАЛЬНЫЕ -------------------
BOT_ACTIVE = True
ALLOWED_USERS = {ADMIN_USERNAME} if ADMIN_USERNAME else set()

user_activity = {}
suspicious_log = []
user_last_request = {}

# ------------------- ДАННЫЕ -------------------
signals = [
    ("BUY 🟢", "Покупка — ожидается рост цены"),
    ("SELL 🔴", "Понижение — ожидается падение цены")
]

phrases = [
    "Сильный паттерн Smart Money PA обнаружен",
    "Анализ графика завершён",
    "График показывает точку входа"
]

confidence_range = (68, 91)
durations = [1, 2, 3]

entry_comments = [
    "Цена подошла к ключевой зоне сопротивления, крупные игроки активно продают.",
    "Формируется структура падения, сигнал подтверждается объёмом.",
    "Тест зоны ликвидности дал подтверждение входа.",
    "Отскок от зоны спроса с импульсом продавцов.",
    "Резкий откат от сопротивления подтверждает вход.",
]

# ------------------- ОТСЛЕЖИВАНИЕ -------------------
@dp.message()
async def track_users(message: Message):
    username = message.from_user.username or "NO_USERNAME"
    user_id = message.from_user.id

    user_activity[user_id] = {
        "username": username,
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if username not in ALLOWED_USERS:
        suspicious_log.append({
            "username": username,
            "user_id": user_id,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": message.text
        })

# ------------------- АНТИ-ФЛУД -------------------
def is_flood(user_id):
    now = asyncio.get_event_loop().time()
    if user_id in user_last_request and now - user_last_request[user_id] < 5:
        return True
    user_last_request[user_id] = now
    return False

# ------------------- АДМИН КОМАНДЫ -------------------
def is_admin(message: Message):
    return message.from_user.username == ADMIN_USERNAME

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Отправь скрин графика 📊")

@dp.message(Command("users"))
async def list_users(message: Message):
    if not is_admin(message):
        return

    if not user_activity:
        await message.answer("Нет пользователей")
        return

    text = "👥 Пользователи:\n\n"
    for user in user_activity.values():
        text += f"@{user['username']} | {user['last_seen']}\n"

    await message.answer(text)

@dp.message(Command("logs"))
async def logs(message: Message):
    if not is_admin(message):
        return

    if not suspicious_log:
        await message.answer("Нет подозрительной активности")
        return

    text = "🚨 Логи:\n\n"
    for log in suspicious_log[-10:]:
        text += f"@{log['username']} | {log['time']}\n{log['text']}\n\n"

    await message.answer(text)

@dp.message(Command("adduser"))
async def add_user(message: Message):
    if not is_admin(message):
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Используй: /adduser username")
        return

    username = parts[1].lstrip("@")
    ALLOWED_USERS.add(username)

    await message.answer(f"Добавлен @{username}")

@dp.message(Command("deluser"))
async def del_user(message: Message):
    if not is_admin(message):
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Используй: /deluser username")
        return

    username = parts[1].lstrip("@")
    ALLOWED_USERS.discard(username)

    await message.answer(f"Удалён @{username}")

@dp.message(Command("stopbot"))
async def stop_bot(message: Message):
    global BOT_ACTIVE
    if is_admin(message):
        BOT_ACTIVE = False
        await message.answer("Бот остановлен")

@dp.message(Command("startbot"))
async def start_bot(message: Message):
    global BOT_ACTIVE
    if is_admin(message):
        BOT_ACTIVE = True
        await message.answer("Бот запущен")

# ------------------- ФОТО -------------------
@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):
    if not BOT_ACTIVE:
        return await message.answer("Бот выключен")

    username = message.from_user.username
    if not username or username not in ALLOWED_USERS:
        return await message.answer("Нет доступа")

    if is_flood(message.from_user.id):
        return await message.answer("Не спамь")

    wait_time = random.randint(3, 8)
    await message.answer(f"Анализ {wait_time} сек...")
    await asyncio.sleep(wait_time)

    signal, desc = random.choice(signals)

    response = (
        f"🎯 {random.choice(phrases)}\n\n"
        f"💹 {signal} на {random.choice(durations)} мин\n"
        f"📊 Уверенность: {random.randint(*confidence_range)}%\n\n"
        f"📉 {desc}\n\n"
        f"💡 {random.choice(entry_comments)}\n\n"
        f"⚠️ Не фин. рекомендация"
    )

    await message.answer(response)

# ------------------- ЗАПУСК -------------------
if __name__ == "__main__":
    if not API_TOKEN:
        raise ValueError("BOT_TOKEN не задан!")

    asyncio.run(dp.start_polling(bot))
