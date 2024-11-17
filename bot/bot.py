from bestconfig import Config
from pyrogram import Client
from handlers import register_handlers
import argparse
from loguru import logger
from utils.database import Database


def get_run_args():
    parser = argparse.ArgumentParser(description="Запуск бота")
    parser.add_argument(
        "--prod",
        action="store_true",
        help="Запустить в продакшен-режиме",
    )
    args = parser.parse_args()
    return args


def get_config(prod: False) -> Config:
    logger.info(f"Start as {'prod' if prod else 'test'}")
    config_path = "config.yaml" if prod else "test_config.yaml"
    return Config(config_path, exclude_default=True)


def main():
    args = get_run_args()
    cfg = get_config(args.prod)
    cfg.insert(cfg.apis)
    db = Database(cfg.db_path)
    app = Client(
        cfg.bot_name,
        bot_token=cfg.bot_token,
        api_id=cfg.api_id,
        api_hash=cfg.api_hash,
    )
    register_handlers(app, cfg, db)
    app.run()


if __name__ == "__main__":
    main()
