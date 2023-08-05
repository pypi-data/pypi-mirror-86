from typing import Dict

__all__ = (
    "get_log_config",
    "JSON_FIELDS"
)

JSON_FIELDS = (
    "asctime", "message", "name", "created",
    "filename", "module", "funcName", "lineno",
    "msecs", "pathname", "process", "processName",
    "relativeCreated", "thread", "threadName", "levelname",
    "access",
)


def build_log_format(fields):
    return " ".join(f"%({f})s" for f in fields)


def get_log_config(fields=JSON_FIELDS) -> Dict:
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                "format": build_log_format(fields=fields),
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'json',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            'root': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'gunicorn.error': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
                'qualname': 'gunicorn.error'
            },
            'gunicorn': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
                'qualname': 'gunicorn'
            },
            'gunicorn.access': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
                'qualname': 'gunicorn.access'
            }
        }
    }
