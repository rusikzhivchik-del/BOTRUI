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
    "Рынок демонстрирует восходящий импульс, пробивая важный уровень сопротивления. Покупатели начинают контролировать ситуацию.",
    "Цена отскочила от уровня поддержки, и индикаторы подтверждают начало восходящего тренда.",
    "Сильный рост объёмов указывает на усиление покупателей, что даёт основание для открытия длинной позиции.",
    "Покупатели уверенно держат цену выше критичного уровня, что сигнализирует о росте до ближайшего сопротивления.",
    "Цена укрепляется выше скользящих средних, что указывает на рост и укрепление бычьего тренда."
]

sell_text = [
    "Рынок уходит вниз, пробивая важную поддержку. Продавцы усиливают давление.",
    "Цена отскакивает от сопротивления, сигнализируя о потенциальном развороте вниз.",
    "Объём продаж нарастает, что указывает на силу продавцов и начало медвежьего тренда.",
    "Рынок не смог удержаться выше уровня, что подтверждает слабость быков и развитие нисходящего движения.",
    "Цена закрепляется ниже ключевых уровней, что подтверждает возможность дальнейшего снижения."
]

confidence = ["78%", "82%", "91%", "69%", "88%"]

smart_money_text = [
    "Цена тестирует ключевые уровни, где крупные игроки (институциональные трейдеры) могут начинать свои позиции. Следи за объёмами!",
    "Объём торговли значительно возрос, что может указывать на манипуляции крупными игроками. Внимание на возможные сильные движения.",
    "Снижение объёмов вблизи ключевых уровней может свидетельствовать о том, что крупные игроки начинают закрывать позиции.",
    "Цена откатывает на низкие уровни, что может быть признаком того, что крупные игроки готовятся к движению вверх.",
    "Крупные игроки удерживают цену в узком диапазоне, возможно, готовясь к сильному прорыву. Обращай внимание на изменения объёмов."
]

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
    analysis = random.choice(buy_text) if "BUY" in signal else random.choice(sell_text)
    smart_analysis = random.choice(smart_money_text)

    text = f"""
<b>{phrase}</b>

💹 <i>Сигнал:</i> {signal}
⏱ <i>Анализ:</i> 1 минута
⏲ <i>Сделка:</i> {duration} мин
📊 <i>Уверенность:</i> {conf}

🕯 <i>Паттерн:</i> {pattern}

🔎 <i>Анализ:</i>
{analysis}

<i>{smart_analysis}</i>

⚠️ <i>Не является финансовой рекомендацией</i>
"""

    await message.answer(text, parse_mode="HTML")

# ------------------- ЗАПУСК -------------------

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
