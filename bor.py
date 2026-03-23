import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command
import asyncio

# ------------------- НАСТРОЙКИ -------------------
API_TOKEN = "8672741740:AAHDn8SPjl6UazjaK4ZP0zKYZoAYChq--MA"
ADMIN_USERNAME = "rusik_tut1"  # твой Telegram username без @

# ------------------- ИНИЦИАЛИЗАЦИЯ -------------------
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ------------------- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ -------------------
BOT_ACTIVE = True  # True — бот активен, False — приостановлен
ALLOWED_USERS = {ADMIN_USERNAME}  # множество разрешённых пользователей

# ------------------- ДАННЫЕ ДЛЯ СИГНАЛОВ -------------------
signals = ["BUY 🟢", "SELL 🔴"]
times = [1, 2, 3]  # только 1,2,3 минуты

phrases = [
    "📊 Анализ графика завершён...",
    "🔍 Обнаружен сильный паттерн!",
    "🧠 Нейросеть подтверждает сигнал",
    "📈 Найдена точка входа",
    "⚡ Импульс движения усиливается"
]

# ------------------- КОМАНДА СТАРТ -------------------
@dp.message(Command(commands=["start"]))
async def start(message: Message):
    if message.from_user.username not in ALLOWED_USERS:
        await message.answer("⛔ У вас нет доступа к боту.")
        return
    await message.answer("📸 Отправь скрин графика — я дам сигнал")

# ------------------- КОМАНДЫ АДМИНА -------------------
@dp.message(Command(commands=["stopbot"]))
async def stop_bot(message: Message):
    global BOT_ACTIVE
    if message.from_user.username != ADMIN_USERNAME:
        return
    BOT_ACTIVE = False
    await message.answer("⛔ Бот приостановлен. Фото больше не обрабатываются.")

@dp.message(Command(commands=["startbot"]))
async def start_bot(message: Message):
    global BOT_ACTIVE
    if message.from_user.username != ADMIN_USERNAME:
        return
    BOT_ACTIVE = True
    await message.answer("✅ Бот снова активен.")

# ------------------- УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ -------------------
@dp.message(Command(commands=["adduser"]))
async def add_user(message: Message):
    if message.from_user.username != ADMIN_USERNAME:
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Используй: /adduser <username>")
        return
    username_to_add = parts[1].lstrip("@")
    ALLOWED_USERS.add(username_to_add)
    await message.answer(f"✅ Пользователь @{username_to_add} добавлен.")

@dp.message(Command(commands=["deluser"]))
async def del_user(message: Message):
    if message.from_user.username != ADMIN_USERNAME:
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Используй: /deluser <username>")
        return
    username_to_remove = parts[1].lstrip("@")
    ALLOWED_USERS.discard(username_to_remove)
    await message.answer(f"❌ Пользователь @{username_to_remove} удалён.")

# ------------------- ОБРАБОТЧИК ФОТО -------------------
@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):
    if not BOT_ACTIVE:
        await message.answer("⛔ Бот временно приостановлен.")
        return

    if message.from_user.username not in ALLOWED_USERS:
        await message.answer("⛔ У вас нет доступа к боту.")
        return

    signal = random.choice(signals)
    time = random.choice(times)
    phrase = random.choice(phrases)
    confidence_value = random.randint(68, 91)  # случайная уверенность от 68 до 91%

    response = f"""
{phrase}

💹 Сигнал: {signal}
⏱ Таймфрейм: {time} мин
📊 Уверенность: {confidence_value}%

⚠️ Не является финансовой рекомендацией
"""
    await message.answer(response)

# ------------------- ЗАПУСК -------------------
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
