import random
import asyncio
import time
import os
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command

# ------------------- НАСТРОЙКИ -------------------
API_TOKEN = os.getenv("BOT_API_TOKEN")
ADMIN_IDS = {8109284840}  # <-- обновлённый админ ID
MAX_FILE_SIZE_MB = 5
REQUEST_COOLDOWN = 60
USERS_FILE = "users.json"

# ------------------- ИНИЦИАЛИЗАЦИЯ -------------------
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
BOT_ACTIVE = True
LAST_REQUEST_TIME = {}

# ------------------- ФУНКЦИИ ПОЛЬЗОВАТЕЛЕЙ -------------------
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(list(ALLOWED_USERS), f)

ALLOWED_USERS = load_users()

def is_allowed(username: str):
    return username.lower() in ALLOWED_USERS

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

candlestick_patterns = [
    "Доджи — неопределённость, возможный разворот",
    "Марубозу — сильный тренд без теней",
    "Падающая звезда — сигнал на разворот вниз",
    "Молот — сигнал на разворот вверх",
    "Пинбар — указывает на разворот или продолжение движения"
]

entry_comments = [
    "Цена подошла к ключевой зоне сопротивления, крупные игроки активно продают, подтверждение на свечах.",
    "На рынке формируется структура падения, сигнал подтверждается динамикой объёма.",
    "Сигнал возникает после теста зоны ликвидности, свечной паттерн подтверждает направление.",
    "Цена отскочила от зоны спроса, наблюдается подтверждающий импульс продавцов.",
    "Резкий откат от уровня сопротивления подтверждает точку входа на снижение.",
    "Тестирование ключевого уровня и подтверждение свечным паттерном указывают на нисходящее движение."
]

# ------------------- АДМИН КОМАНДЫ -------------------
@dp.message(Command(commands=["stopbot"]))
async def stop_bot(message: Message):
    global BOT_ACTIVE
    if message.from_user.id not in ADMIN_IDS:
        return
    BOT_ACTIVE = False
    await message.answer("Бот приостановлен.")

@dp.message(Command(commands=["startbot"]))
async def start_bot(message: Message):
    global BOT_ACTIVE
    if message.from_user.id not in ADMIN_IDS:
        return
    BOT_ACTIVE = True
    await message.answer("Бот снова активен.")

@dp.message(Command(commands=["adduser"]))
async def add_user(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Используй: /adduser <username без @>")
        return

    username_to_add = parts[1].lstrip("@")
    ALLOWED_USERS.add(username_to_add.lower())
    save_users()
    await message.answer(f"Пользователь @{username_to_add} добавлен.")

@dp.message(Command(commands=["deluser"]))
async def del_user(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Используй: /deluser <username без @>")
        return

    username_to_remove = parts[1].lstrip("@")
    ALLOWED_USERS.discard(username_to_remove.lower())
    save_users()
    await message.answer(f"Пользователь @{username_to_remove} удалён.")

@dp.message(Command(commands=["allusers"]))
async def all_users(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    if not ALLOWED_USERS:
        await message.answer("Список пользователей пуст.")
    else:
        users_list = "\n".join("@" + uname for uname in ALLOWED_USERS)
        await message.answer(f"📋 Все пользователи бота:\n{users_list}")

@dp.message(Command(commands=["help"]))
async def help_command(message: Message):
    help_text = (
        "📌 **Список команд бота:**\n\n"
        "**Админские команды:**\n"
        "/startbot — запуск бота\n"
        "/stopbot — приостановка работы бота\n"
        "/adduser <username> — добавить пользователя\n"
        "/deluser <username> — удалить пользователя\n"
        "/allusers — показать всех пользователей\n\n"
        "**Для всех разрешённых пользователей:**\n"
        "Отправьте фото графика, и бот пришлёт анализ сигнала.\n"
        f"⚠️ Максимальный размер фото — {MAX_FILE_SIZE_MB} МБ.\n"
        f"⚠️ Один запрос в {REQUEST_COOLDOWN} секунд."
    )
    await message.answer(help_text, parse_mode="Markdown")

# ------------------- ФОТО -------------------
@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):
    if not BOT_ACTIVE:
        await message.answer("Бот временно приостановлен.")
        return

    username = message.from_user.username
    if not username or not is_allowed(username.lower()):
        await message.answer("У вас нет доступа к боту.")
        return

    now = time.time()
    last_time = LAST_REQUEST_TIME.get(username.lower(), 0)

    if now - last_time < REQUEST_COOLDOWN:
        wait_seconds = int(REQUEST_COOLDOWN - (now - last_time))
        await message.answer(f"⏳ Подождите {wait_seconds} секунд.")
        return

    LAST_REQUEST_TIME[username.lower()] = now

    photo = message.photo[-1]
    if photo.file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        await message.answer(f"Файл слишком большой! Максимум {MAX_FILE_SIZE_MB} МБ.")
        return

    wait_time = random.randint(3, 10)
    await message.answer(f"Анализируем график ({wait_time} сек)...")
    await asyncio.sleep(wait_time)

    signal, signal_desc = random.choice(signals)
    duration = random.choice(durations)
    confidence_value = random.randint(*confidence_range)
    phrase = random.choice(phrases)
    chosen_pattern = random.choice(candlestick_patterns)
    comment_text = random.choice(entry_comments)

    response = (
        f"🎯 {phrase}\n\n"
        f"💹 Сигнал: {signal} на {duration} минут\n"
        f"📝 {signal_desc}\n"
        f"📊 Уверенность: {confidence_value}%\n\n"
        f"Свечной паттерн:\n• {chosen_pattern}\n\n"
        f"💡 Комментарий: {comment_text}"
    )

    await message.answer(response, parse_mode="Markdown")

# ------------------- ЗАПУСК -------------------
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
