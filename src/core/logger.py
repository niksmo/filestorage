logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(module)s: %(message)s'
        },
        'uvicorn_default_f': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': True,
        },
        'uvicorn_access_f': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': ('%(levelprefix)s %(client_addr)s - '
                    "'%(request_line)s' %(status_code)s"),
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': 'ext://sys.stdout'
        },
        'uvicorn_default_sh': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'uvicorn_default_f',
            'stream': 'ext://sys.stdout'
        },
        'uvicorn_access_sh': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'uvicorn_access_f',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'common': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'uvicorn.access': {
            'level': 'DEBUG',
            'handlers': ['uvicorn_access_sh'],
        },
        'uvicorn.error': {
            'level': 'DEBUG',
            'handlers': ['uvicorn_default_sh']
        }
    }
}
