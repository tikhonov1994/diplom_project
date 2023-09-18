import logging

from core.config import app_config as config

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', ]
if config.log_level == 'DEBUG':
    LOG_LEVEL = logging.DEBUG
elif config.log_level == 'INFO':
    LOG_LEVEL = logging.INFO
elif config.log_level == 'ERROR':
    LOG_LEVEL = logging.ERROR
elif config.log_level == 'CRITICAL':
    LOG_LEVEL = logging.CRITICAL

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
