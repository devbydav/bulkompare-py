import logging.config
import logging.handlers

LEVEL = logging.DEBUG


config = {
    "disable_existing_loggers": False,
    "version": 1,
    "formatters": {
        "stream": {
            "format": "%(levelname)s - %(message)s  (%(name)s.%(funcName)s)"
        },
    },
    "handlers": {
        "stream": {
            'formatter': 'stream',
            'class': 'logging.StreamHandler',
        },
    },
    "loggers": {
        "": {
            "handlers": ["stream"],
            "level": LEVEL
        },
    },
}

logging.config.dictConfig(config)
