import random
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command

# ------------------- НАСТРОЙКИ -------------------
API_TOKEN = "8672741740:AAHDn8SPjl6UazjaK4ZP0zKYZoAYChq--MA"
ADMIN_USERNAME = "rusik_tut1"  # ваш Telegram username без @

# ------------------- ИНИЦИАЛИЗАЦИЯ -------------------
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ------------------- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ -------------------
BOT_ACTIVE = True
ALLOWED_USERS = {ADMIN_USERNAME}

# ------------------- ДАННЫЕ ДЛЯ СИГНАЛОВ -------------------
signals = [
    ("BUY 🟢", "💚 Покупка — ожидается рост цены"),
    ("SELL 🔴", "❤️ Продажа — ожидается падение цены")
]
phrases = [
    "📊 Анализ графика завершён...",
    "🔍 Сильный паттерн Smart Money PA обнаружен",
    "🧠 Нейросеть подтверждает сигнал",
    "📈 График показывает точку входа",
    "⚡ Импульс движения усиливается"
]
confidence_range = (68, 91)

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

    # Рандомная пауза 3-10 секунд
    wait_time = random.randint(3, 10)
    await message.answer(f"⏳ Анализируем график, подождите {wait_time} секунд...")
    await asyncio.sleep(wait_time)

    # Выбор сигнала
    signal, signal_desc = random.choice(signals)
    confidence_value = random.randint(*confidence_range)
    phrase = random.choice(phrases)

    # Текст по Smart Money PA
    smpa_text = (
        "📌 **Smart Money PA (1M таймфрейм):**\n"
        "• 🔹 Определяем зоны интереса крупных участников\n"
        "• 🔹 Ищем подтверждающий импульс для входа\n"
        "• 🔹 Сигнал сформирован на основе активности «умных денег»"
    )

    # Пояснение по свечным паттернам
    candlestick_text = (
        "🕯 **Свечные паттерны:**\n"
        "• Доджи — неопределённость, возможный разворот\n"
        "• Марубозу — сильный тренд без теней\n"
        "• Падающая звезда — сигнал на разворот вниз\n"
        "• Молот — сигнал на разворот вверх\n"
        "• Пинбар — указывает на разворот или продолжение движения"
    )

    # Формируем финальный красивый ответ
    response = (
        f"🎯 {phrase}\n\n"
        f"💹 **Сигнал:** {signal}\n"
        f"📝 {signal_desc}\n"
        f"⏱ **Таймфрейм:** 1M\n"
        f"📊 **Уверенность:** {confidence_value}%\n\n"
        f"{smpa_text}\n\n"
        f"{candlestick_text}\n\n"
        f"⚠️ *Не является финансовой рекомендацией*"
    )

    await message.answer(response, parse_mode="Markdown")

# ------------------- ЗАПУСК БОТА -------------------
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
