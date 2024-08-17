import logging

from pydantic import BaseConfig


class GlobalConfig(BaseConfig):
    title: str = "TITLE"
    version: str = "1.0.0"
    description: str = "DESCRIPTION"
    log_format: str = "LOG_FORMAT"
    logging_level: int = logging.DEBUG


settings = GlobalConfig()
