import logging

from pydantic import BaseConfig


class GlobalConfig(BaseConfig):
    title: str = "TITLE"
    version: str = "1.0.0"
    description: str = "DESCRIPTION"
    log_format: str = "LOG_FORMAT"

    title: str
    version: str = "1.0.0"
    description: str
    openapi_prefix: str = ""
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    api_prefix: str = "/api"
    debug: bool

    grpc_responder: str = "0.0.0.0"

    logging_level: int = logging.DEBUG


settings = GlobalConfig()
