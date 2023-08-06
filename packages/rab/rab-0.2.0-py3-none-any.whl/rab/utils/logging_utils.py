"""Logging Utilities

This module defines default logging configurations and methods for sending
logging messages directly to stderr.
"""
# Standard Libraries
import sys
import logging
import logging.config

LOGGING_LINE_FORMAT = "{asctime} {levelname} {name} lineno:{lineno}: {message}"
LOGGING_DATETIME_FORMAT = "[%Y-%m-%d %H:%M:%S]"
LOGGING_STYLE = "{"


def _configure_rab_loggers(root_module_name: str):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_formatter": False,
            "formatters": {
                "rab_formatter": {
                    "format": LOGGING_LINE_FORMAT,
                    "datefmt": LOGGING_DATETIME_FORMAT,
                    "style": LOGGING_STYLE,
                }
            },
            # Handler can output any 'format' to any 'target', e.g. output
            # a log to a structlog service
            "handlers": {
                "rab_handler": {
                    "level": "INFO",
                    "formatter": "rab_formatter",
                    "class": "logging.StreamHandler",
                    "stream": sys.stderr,
                }
            },
            "loggers": {
                root_module_name: {
                    "handlers": ["rab_handler"],
                    "level": "INFO",
                    "propagate": False,
                }
            },
        }
    )


def eprint(*args, **kwargs):
    """prints to stderr"""
    print(*args, file=sys.stderr, **kwargs)
