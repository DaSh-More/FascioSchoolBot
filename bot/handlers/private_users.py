from bestconfig import Config
from pyrogram import Client

from utils.database import Database


def register_handlers_private_users(
    app: Client, config: Config, database: Database
): ...
