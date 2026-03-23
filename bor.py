import random
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command

# ------------------- НАСТРОЙКИ -------------------
API_TOKEN = "8672741740:AAHDn8SPjl6UazjaK4ZP0zKYZoAYChq--MA"
ADMIN_USERNAME = "rusik_tut1"

# ------------------- ИНИЦИАЛИЗАЦИЯ -------------------
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ------------------- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ -------------------
BOT_ACTIVE = True
ALLOWED_USERS = {ADMIN_USERNAME}

# ------------------- ДАННЫЕ ДЛЯ СИГНАЛОВ -------------------
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
durations = [1, 2, 3]  # минуты для бинарного опциона
candlestick_patterns = [
    "Доджи — неопределённость, возможный разворот",
    "Марубозу — сильный тренд без теней",
    "Падающая звезда — сигнал на разворот вниз",
    "Молот — сигнал на разворот вверх",
    "Пинбар — указывает на разворот или продолжение движения"
]

# ------------------- РАЗНЫЕ КОММЕНТАРИИ -------------------
entry_comments = [
    "Цена подошла к ключевой зоне сопротивления, крупные игроки активно продают, подтверждение на свечах.",
    "На рынке формируется структура падения, сигнал подтверждается динамикой объёма.",
    "Сигнал возникает после теста зоны ликвидности, свечной паттерн подтверждает направление.",
    "Цена отскочила от зоны спроса, наблюдается подтверждающий импульс продавцов.",
    "Резкий откат от уровня сопротивления подтверждает точку входа на снижение.",
    "Тестирование ключевого уровня и подтверждение свечным паттерном указывают на нисходящее движение."
]

# ------------------- КОМАНДЫ АДМИНА -------------------
@dp.message(Command(commands=["stopbot"]))
async def stop_bot(message: Message):
    global BOT_ACTIVE
    if message.from_user.username != ADMIN_USERNAME:
        return
    BOT_ACTIVE = False
    await message.answer("Бот приостановлен.")

@dp.message(Command(commands=["startbot"]))
async def start_bot(message: Message):
    global BOT_ACTIVE
    if message.from_user.username != ADMIN_USERNAME:
        return
    BOT_ACTIVE = True
    await message.answer("Бот снова активен.")

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
    await message.answer(f"Пользователь @{username_to_add} добавлен.")

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
    await message.answer(f"Пользователь @{username_to_remove} удалён.")

# ------------------- ОБРАБОТЧИК ФОТО -------------------
@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):
    if not BOT_ACTIVE:
        await message.answer("Бот временно приостановлен.")
        return
    if message.from_user.username not in ALLOWED_USERS:
        await message.answer("У вас нет доступа к боту.")
        return

    # Рандомная пауза 3-10 секунд
    wait_time = random.randint(3, 10)
    await message.answer(f"Анализируем график, подождите {wait_time} секунд...")
    await asyncio.sleep(wait_time)

    # Выбор сигнала и длительности бинарного опциона
    signal, signal_desc = random.choice(signals)
    duration = random.choice(durations)
    confidence_value = random.randint(*confidence_range)
    phrase = random.choice(phrases)

    # Smart Money PA текст
    smpa_text = (
        "Smart Money PA (1M таймфрейм):\n"
        "• Определяем зоны интереса крупных участников\n"
        "• Ищем подтверждающий импульс для входа"
    )

    # Выбираем 1 случайный свечной паттерн
    chosen_pattern = random.choice(candlestick_patterns)
    candlestick_text = f"Свечной паттерн:\n• {chosen_pattern}"

    # Выбираем случайный комментарий
    comment_text = random.choice(entry_comments)

    # Формируем финальный ответ
    response = (
        f"🎯 {phrase}\n\n"
        f"💹 Сигнал: {signal} на {duration} минут\n"
        f"📝 {signal_desc}\n"
        f"⏱ Таймфрейм анализа: 1M\n"
        f"📊 Уверенность: {confidence_value}%\n\n"
        f"{smpa_text}\n\n"
        f"{candlestick_text}\n\n"
        f"💡 Комментарий: {comment_text}\n\n"
        f"⚠️ Не является финансовой рекомендацией"
    )

    await message.answer(response, parse_mode="Markdown")

# ------------------- ЗАПУСК БОТА -------------------
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
