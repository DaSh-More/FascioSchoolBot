from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import Message


@filters.create
async def private_message(_, __, message: Message) -> bool:
    """
    Фильтр для проверки является ли пользователь отправивший сообщение администратором
    """
    return message.chat.type == ChatType.PRIVATE


@filters.create
async def from_group_admin(_, client, message):
    """
    Фильтр для проверки является ли пользователь отправивший сообщение администратором текущей группы
    """
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    return chat_member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    )


def from_admin(database):
    @filters.create
    async def filter_from_admin(_, client: Client, message: Message):
        user = await database.get_user(user_id=message.from_user.id)
        if not user:
            return False
        return user[2] == "admin"

    return filter_from_admin
