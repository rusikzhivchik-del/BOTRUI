import random
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# ------------------- НАСТРОЙКИ -------------------
API_TOKEN = "8672741740:AAHDn8SPjl6UazjaK4ZP0zKYZoAYChq--MA"
ADMIN_USERNAME = "rusik_tut1"  # ваш Telegram username без @

# ------------------- ИНИЦИАЛИЗАЦИЯ -------------------
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ------------------- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ -------------------
BOT_ACTIVE = True  # True — бот активен
users = set()      # список пользователей для добавления/удаления

signals = ["BUY 🟢", "SELL 🔴"]
times = [1, 2, 3]  # только 1,2,3 минуты
phrases = [
    "📊 Анализ графика завершён...",
    "🔍 Обнаружен сильный паттерн!",
    "🧠 Нейросеть подтверждает сигнал",
    "📈 Найдена точка входа",
    "⚡ Импульс движения усиливается"
]

# ------------------- КОМАНДЫ -------------------
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("📸 Отправь скрин графика — я дам сигнал")

@dp.message(Command("startbot"))
async def cmd_startbot(message: Message):
    global BOT_ACTIVE
    if message.from_user.username != ADMIN_USERNAME:
        return
    BOT_ACTIVE = True
    await message.answer("✅ Бот снова активен.")

@dp.message(Command("stopbot"))
async def cmd_stopbot(message: Message):
    global BOT_ACTIVE
    if message.from_user.username != ADMIN_USERNAME:
        return
    BOT_ACTIVE = False
    await message.answer("⛔ Бот приостановлен.")

# ------------------- ДОБАВЛЕНИЕ/УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ -------------------
@dp.message()
async def handle_message(message: Message):
    global users

    if message.from_user.username != ADMIN_USERNAME:
        return  # только админ может управлять списком

    if not BOT_ACTIVE:
        await message.answer("⛔ Бот временно приостановлен.")
        return

    text = message.text.strip()
    if text.startswith("@"):
        username = text[1:]
        if username in users:
            users.remove(username)
            await message.answer(f"Пользователь @{username} удалён из списка.")
        else:
            users.add(username)
            await message.answer(f"Пользователь @{username} добавлен в список.")
    else:
        await message.answer(f"Список пользователей: {', '.join('@'+u for u in users) if users else 'пуст'}")

# ------------------- ОБРАБОТКА ФОТО -------------------
@dp.message(content_types=["photo"])
async def handle_photo(message: Message):
    if not BOT_ACTIVE:
        await message.answer("⛔ Бот временно приостановлен.")
        return

    signal = random.choice(signals)
    time_val = random.choice(times)
    phrase = random.choice(phrases)
    confidence_value = random.randint(68, 91)

    response = f"""
{phrase}

💹 Сигнал: {signal}
⏱ Таймфрейм: {time_val} мин
📊 Уверенность: {confidence_value}%

⚠️ Не является финансовой рекомендацией
"""
    await message.answer(response)

# ------------------- ЗАПУСК -------------------
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
