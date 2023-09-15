import logging

from core.config import app_config as config

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', ]
match config.api.log_level:
    case 'DEBUG':
        LOG_LEVEL = logging.DEBUG
    case 'INFO':
        LOG_LEVEL = logging.INFO
    case 'ERROR':
        LOG_LEVEL = logging.ERROR
    case 'CRITICAL':
        LOG_LEVEL = logging.CRITICAL
    case _:
        LOG_LEVEL = logging.WARNING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': LOG_LEVEL,
        },
        'uvicorn.error': {
            'level': LOG_LEVEL,
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
    'root': {
        'level': LOG_LEVEL,
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
