import logging

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              ('[%(asctime)s %(levelname)-7s %(hostname)s(%(name)s) '
               '<%(process)d> %(filename)s:%(lineno)d] %(message)s')
        }
    },
    handlers = {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': logging.DEBUG,
            'stream': 'ext://sys.stderr',
        }
    },
    filters = {
        'hostname': {
            '()': 'ext://filters.HostnameFilter'
        }
    },
    loggers = {
        '': {
            'handlers': ['console'],
            'level': logging.DEBUG,
            'filters': ['hostname'],
        }
    }
)
