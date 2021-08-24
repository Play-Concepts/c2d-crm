from __future__ import annotations

import logging
import os
import sys

import loguru
from loguru import logger
from loguru._defaults import LOGURU_FORMAT

from app.application import application
from app.core.global_config import config as app_config

LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        print(record.name)
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# [UTCtimestamp][Severity][Method][ReponseCode][ResponseTime][Category][Component][HashedIP]
# [Request Id][namespace][free-form body as json]
def format_record(record: dict) -> str:
    def process_ip(ip_address: str) -> str:
        ip, *_ = ip_address.split(":")
        return ip if app_config.IP_LOGGING else ""

    message = "[{time:YYYY-MM-DDTHH:mm:ss.SSS}Z][{level}]------[{name}]"
    if record["name"] == "uvicorn.lifespan.on":
        message = "[{time:YYYY-MM-DDTHH:mm:ss.SSS}Z][{level}]in here{message}"

    return message


def setup_logging():
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    # logger.configure(
    #    handlers=[
    #        {
    #            "sink": sys.stdout,
    #            "serialize": JSON_LOGS,
    #            "format": format_record
    #        },
    #    ],
    #    extra={
    #        "request_id": ""
    #    }
    # )
    logger.remove()
    logger.add(sys.stdout, format=format_record, serialize=JSON_LOGS)


setup_logging()

app = application
