from bestconfig import Config
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from utils.database import Database
from utils.filters import private_message, from_admin


def get_stat_handler(config: Config, database: Database) -> MessageHandler:
    async def get_state(client: Client, message: Message):
        """
        Получить статистику по ботам
        """
        all_users = await database.get_all_users()
        all_user_count = len(all_users)
        runned_user_count = len([u for u in all_users if u[3] == "runned"])
        admin_user_count = len([u for u in all_users if u[2] == "admin"])
        stat_text = f"""Всего пользователей: {all_user_count}
У которых запущен бот: {runned_user_count}
Из них администраторы: {admin_user_count}
        """

        await client.send_message(message.from_user.id, stat_text)

    # TODO проверить на админа
    return MessageHandler(
        get_state,
        filters.command("stat") & private_message & from_admin(database),
    )


def register_handlers_private_admins(app: Client, config: Config, database: Database):
    app.add_handler(get_stat_handler(config, database))
