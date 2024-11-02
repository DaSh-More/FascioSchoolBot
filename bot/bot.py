from bestconfig import Config
from pyrogram import Client, enums, filters

TEST_MODE = False

CONFIG_PATH = "test_confit.yaml" if TEST_MODE else "confit.yaml"

cfg = Config(CONFIG_PATH, exclude_default=True)
cfg.insert(cfg.apis)

app = Client(
    cfg.bot_name, bot_token=cfg.bot_token, api_id=cfg.api_id, api_hash=cfg.api_hash
)


@filters.create
async def from_admin(_, client, query):
    """
    Фильтр для проверки является ли пользователь отправивший сообщение администратором
    """
    chat_member = await client.get_chat_member(query.chat.id, query.from_user.id)
    return chat_member.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    )


@app.on_message(
    filters.command("all", prefixes=["/", "@"]) & filters.chat(cfg.chat_id) & from_admin
)
async def tag_all(client, message):
    """
    Тегнуть всех пользователей чата
    """    
    chat_id = message.chat.id
    tag_all_message = "".join(
        [
            f"<a href=tg://user?id={i.user.id}>'</a>"
            async for i in app.get_chat_members(chat_id)
        ]
    )
    await app.send_message(chat_id, tag_all_message)


def main():
    app.run()


if __name__ == "__main__":
    main()
