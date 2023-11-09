import sys
import json
import logging
import datetime
import loguru
from logging.config import dictConfig
from typing import cast
from types import FrameType
import stackprinter
import logstash

from core.config import app_config
from schemas.logs import BaseJsonLogSchema

LEVEL_TO_NAME = {
    logging.CRITICAL: 'Critical',
    logging.ERROR: 'Error',
    logging.WARNING: 'Warning',
    logging.INFO: 'Information',
    logging.DEBUG: 'Debug',
    logging.NOTSET: 'Trace',
}


class ConsoleLogger(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = loguru.logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)
        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1
        loguru.logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class JSONLogFormatter(logging.Formatter):
    """
    Custom class-formatter for writing logs to json
    """

    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        """
        Formatting LogRecord to json

        :param record: logging.LogRecord
        :return: json string
        """
        log_object: dict = self._format_log_object(record)
        return json.dumps(log_object, ensure_ascii=False)

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict:
        now = (
            datetime.
            datetime.
            fromtimestamp(record.created).
            astimezone().
            replace(microsecond=0).
            isoformat()
        )
        message = record.getMessage()
        duration = (
            record.duration
            if hasattr(record, 'duration')
            else int(record.msecs)
        )

        json_log_fields = BaseJsonLogSchema(
            thread=record.process,
            timestamp=now,
            level_name=LEVEL_TO_NAME[record.levelno],
            message=message,
            source_log=record.name,
            duration=duration,
            app_name=app_config.api.project_name,
            app_version=app_config.api.version,
        )

        if hasattr(record, 'props'):
            json_log_fields.props = record.props

        if record.exc_info:
            json_log_fields.exceptions = (
                # default library traceback
                # traceback.format_exception(*record.exc_info)

                # stackprinter gets all debug information
                # https://github.com/cknd/stackprinter/blob/master/stackprinter/__init__.py#L28-L137
                stackprinter.format(
                    record.exc_info,
                    suppressed_paths=[
                        r"lib/python.*/site-packages/starlette.*",
                    ],
                    add_summary=False,
                ).split('\n')
            )

        elif record.exc_text:
            json_log_fields.exceptions = record.exc_text

        # Pydantic to dict
        json_log_object = json_log_fields.model_dump(
            exclude_unset=True,
            by_alias=True,
        )
        # getting additional fields
        if hasattr(record, 'request_json_fields'):
            json_log_object.update(record.request_json_fields)

        return json_log_object


def handlers():
    handler_list = ['json']

    return handler_list


LOG_HANDLER = handlers()
LOGGING_LEVEL = logging.DEBUG if app_config.debug else logging.INFO

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': JSONLogFormatter,
        },
    },
    'handlers': {
        'json': {
            'formatter': 'json',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
        'intercept': {
            '()': ConsoleLogger,
        }
    },
    'loggers': {
        'main': {
            'handlers': LOG_HANDLER,
            'level': LOGGING_LEVEL,
            'propagate': False,
        },
        'uvicorn': {
            'handlers': LOG_HANDLER,
            'level': 'INFO',
            'propagate': False,
        },
        'uvicorn.access': {
            'handlers': LOG_HANDLER,
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# dictConfig(LOG_CONFIG)
logger = logging.getLogger('main')

if app_config.export_logs:
    logstash_handler = logstash.LogstashHandler(app_config.logstash.host,
                                                app_config.api.logstash_port,
                                                version=1)
    logger.addHandler(logstash_handler)
