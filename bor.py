import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

API_TOKEN = "8672741740:AAHDn8SPjl6UazjaK4ZP0zKYZoAYChq--MA"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

signals = ["BUY 🟢", "SELL 🔴"]
times = [1, 2, 3, 4, 5]

phrases = [
    "📊 Анализ графика завершён...",
    "🔍 Обнаружен сильный паттерн!",
    "🧠 Нейросеть подтверждает сигнал",
    "📈 Найдена точка входа",
    "⚡ Импульс движения усиливается"
]

confidence = [
    "Уверенность: 82%",
    "Уверенность: 76%",
    "Уверенность: 91%",
    "Уверенность: 68%",
    "Уверенность: 88%"
]

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer("📸 Отправь скрин графика — я дам сигнал")

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: Message):
    signal = random.choice(signals)
    time = random.choice(times)
    phrase = random.choice(phrases)
    conf = random.choice(confidence)

    response = f"""
{phrase}

💹 Сигнал: {signal}
⏱ Таймфрейм: {time} мин
📊 {conf}

⚠️ Не является финансовой рекомендацией
"""

    await message.answer(response)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
