from bestconfig import Config
from pyrogram import Client
from handlers import register_handlers
import argparse
from loguru import logger


def get_config(prod: False) -> Config:
    logger.info(f"Start as {'prod' if prod else 'test'}")
    config_path = "config.yaml" if prod else "test_config.yaml"
    return Config(config_path, exclude_default=True)


def main():
    parser = argparse.ArgumentParser(description="Запуск бота")
    parser.add_argument(
        "--prod",
        action="store_true",
        help="Запустить в продакшен-режиме",
        default=False
    )
    args = parser.parse_args()
    print(args.prod)
    cfg = get_config(args.prod)
    cfg.insert(cfg.apis)
    app = Client(
        cfg.bot_name,
        bot_token=cfg.bot_token,
        api_id=cfg.api_id,
        api_hash=cfg.api_hash,
    )
    register_handlers(app, cfg)
    app.run()


if __name__ == "__main__":
    main()
