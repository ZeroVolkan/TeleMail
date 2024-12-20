from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from setting import get_setting
from database import Database
from gmail import get_last_email_sender, auth


setting = get_setting()
bot = Bot(setting["telegram"]["token"])
dp = Dispatcher()


@dp.message(Command("register"))
async def cmd_start(message: types.Message):
    """
    Обработка команды /register: Создает пользователя в базе данных, если его еще нет.
    """
    db = Database()
    try:
        user = db.get(message.chat.id)
        if user:
            await message.answer("Вы уже зарегистрированы.")
        else:
            db.create_user(message.chat.id)
            await message.answer("Привет! Вы успешно зарегистрированы.")
    except Exception as e:
        await message.answer("Произошла ошибка при регистрации.")
        print(f"Error in /start: {e}")
    finally:
        db.close()


@dp.message(Command("auth"))
async def cmd_auth(message: types.Message):
    """
    Обработка команды /auth: Инициирует процесс аутентификации пользователя через Google.
    """
    db = Database()
    try:
        user = db.get(message.chat.id)

        if user and user.get("auth_token"):
            await message.answer("Вы уже аутентифицированы.")
            return

        await message.answer("Инициализируем процесс аутентификации...")
        creds = await auth(message.chat.id)  # Получаем токен через OAuth
        db.users.update_one(
            {"chat_id": message.chat.id},
            {"$set": {"auth_token": creds}},
            upsert=True
        )
        await message.answer("Аутентификация завершена! Теперь вы можете использовать команды.")
    except Exception as e:
        await message.answer("Произошла ошибка при аутентификации.")
        print(f"Error in /auth: {e}")
    finally:
        db.close()


@dp.message(Command("last"))
async def cmd_last_email(message: types.Message):
    """
    Обработка команды /last_email: Получает информацию о последнем отправителе email из Gmail.
    """
    db = Database()
    try:
        # Получение токена из базы данных
        user = db.get(message.chat.id)

        if user and user.get("auth_token"):
            creds = user["auth_token"]
            last_sender = get_last_email_sender(creds)
            await message.answer(last_sender)
        else:
            await message.answer("Вы не аутентифицированы. Пожалуйста, используйте команду /auth.")
    except Exception as e:
        await message.answer("Произошла ошибка.")
        print(f"Error in /last_email: {e}")
    finally:
        db.close()


async def send_message(chat_id: int, text: str):
    await bot.send_message(chat_id, text)


async def telegram_loop():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(telegram_loop())
