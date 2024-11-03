from pyrogram import Client, filters, types
from pyrogram.handlers import MessageHandler
from bestconfig import Config


async def start(client: Client, message: types.Message):
    """
    Обработчик команды start
    """
    await client.send_message(message.chat.id, "Привет!")


def register_handlers_private(app: Client, config: Config):
    app.add_handler(MessageHandler(start, filters.command("start")))
