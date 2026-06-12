import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = "8794038815:AAFQAvCckZeLIMiK9YSmL5_2GK5iDLq-0g0"
ADMIN_ID = 8000962980  # сюда вставь свой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Здравствуйте! Спасибо за то что хотите выложить новость в наш канал.\n"
        "Введите текст, голосовое сообщение, видеосообщения, фото либо видео."
    )

# Приём ЛЮБЫХ сообщений
@dp.message()
async def forward_to_admin(message: Message):
    # пересылаем тебе
    await bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

    # сохраняем ID пользователя (чтобы потом ответить)
    await bot.send_message(
        ADMIN_ID,
        f"ID пользователя: {message.chat.id}"
    )

# Ответ пользователю через reply
@dp.message(lambda msg: msg.reply_to_message is not None)
async def reply_to_user(message: Message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = message.reply_to_message.forward_from.id
            await bot.send_message(user_id, message.text)
        except:
            await message.answer("Не удалось ответить")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
