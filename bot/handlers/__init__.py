from pyrogram import Client
from bestconfig import Config

from .group import register_handlers_group
from .private import register_handlers_private


def register_handlers(app: Client, config: Config):
    register_handlers_group(app, config)
    register_handlers_private(app, config)