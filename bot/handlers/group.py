from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from bestconfig import Config

from utils.database import Database
from utils.filters import from_group_admin


def tag_all(config: Config):
    """
    Тегнуть всех пользователей чата
    """

    async def tag_all_wrap(client, message):
        chat_id = message.chat.id
        tag_all_message = "".join(
            [
                f"<a href=tg://user?id={i.user.id}>'</a>"
                async for i in client.get_chat_members(chat_id)
            ]
        )
        await client.send_message(chat_id, tag_all_message)

    tag_all_ = MessageHandler(
        tag_all_wrap,
        filters.command("all", prefixes=["/", "@"])
        & filters.chat(config.chat_id)
        & from_group_admin,
    )

    return tag_all_


def register_handlers_group(app: Client, config: Config, database: Database):
    # app.add_handler(tag_all(config))
    ...
