from bestconfig import Config
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from utils.database import Database
from utils.filters import private_message
from .private_admins import register_handlers_private_admins
from .private_users import register_handlers_private_users


def start_handler(config: Config, database: Database):
    async def start(client: Client, message: Message):
        """
        Обработчик запуска бота
        """
        res = await database.add_user(message.from_user.id, message.from_user.username)
        if res == "user added":
            await client.send_message(message.chat.id, "Привет!")
        else:
            await database.set_user_state(message.from_user.id, "runned")
            await client.send_message(message.chat.id, "С возвращением!")

    return MessageHandler(start, filters.command("start") & private_message)


def stop_handler(config: Config, database: Database):
    async def stop(client: Client, message: Message):
        """
        Обработчик остановки бота
        """
        # Пытаемся добавить пользователя в базу
        # Внутри все равно будет проверка на наличие пользователя
        # Но если его нет, надо его добавить
        await database.add_user(message.from_user.id, message.from_user.username)
        # Останавливаем пользователя
        await database.set_user_state(message.from_user.id, "stopped")

    return MessageHandler(stop, filters.command("stop") & private_message)


def register_handlers_private(app: Client, config: Config, database: Database):
    app.add_handler(start_handler(config, database))
    app.add_handler(stop_handler(config, database))

    register_handlers_private_users(app, config, database)
    register_handlers_private_admins(app, config, database)
