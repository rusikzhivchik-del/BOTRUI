import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

# ------------------- НАСТРОЙКИ -------------------
API_TOKEN = "8672741740:AAHDn8SPjl6UazjaK4ZP0zKYZoAYChq--MA"
ADMIN_USERNAME = "rusik_tut1"  # твой Telegram username без @

# ------------------- ИНИЦИАЛИЗАЦИЯ -------------------
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ------------------- ГЛОБАЛЬНЫЙ ФЛАГ -------------------
BOT_ACTIVE = True  # True — бот активен, False — приостановлен

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
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer("📸 Отправь скрин графика — я дам сигнал")

# ------------------- КОМАНДЫ АДМИНА -------------------
@dp.message_handler(commands=['stopbot'])
async def stop_bot(message: Message):
    global BOT_ACTIVE
    if message.from_user.username != ADMIN_USERNAME:
        return
    BOT_ACTIVE = False
    await message.answer("⛔ Бот приостановлен. Фото больше не обрабатываются.")

@dp.message_handler(commands=['startbot'])
async def start_bot(message: Message):
    global BOT_ACTIVE
    if message.from_user.username != ADMIN_USERNAME:
        return
    BOT_ACTIVE = True
    await message.answer("✅ Бот снова активен.")

# ------------------- ОБРАБОТЧИК ФОТО -------------------
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: Message):
    if not BOT_ACTIVE:
        await message.answer("⛔ Бот временно приостановлен.")
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
    executor.start_polling(dp, skip_updates=True)
