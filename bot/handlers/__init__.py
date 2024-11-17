from bestconfig import Config
from pyrogram import Client

from utils.database import Database
from .group import register_handlers_group
from .private import register_handlers_private


def register_handlers(app: Client, config: Config, database: Database):
    register_handlers_group(app, config, database)
    register_handlers_private(app, config, database)
