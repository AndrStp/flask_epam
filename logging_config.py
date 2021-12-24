# logging_config = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters' : {
#         'default' : {
#             'format': '[%(asctime)s] ::%(levelname)s:: in %(name)s: %(module)s: %(message)s',
#             'datefmt': '%Y-%b-%d %H:%M:%S',
#         }
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'level': 'INFO',
#             'formatter': 'default',
#             'stream': 'ext://sys.stdout'
#         },
#         'file' : {
#             'class': 'logging.handlers.RotatingFileHandler',
#             'level': 'INFO',
#             'formatter': 'default',
#             'filename': 'logs/log.txt',
#             'maxBytes': 10485760,
#             'backupCount': 3,
#             'encoding': 'utf8'
#         }
#     },
#     'loggers': {
#         'werkzeug': {
#             'level': 'DEBUG',
#             'handlers': ['console', 'file'],
#         },
#         'root': {
#             'level': 'DEBUG',
#             'handlers': ['console', 'file']
#         }
#     }
# }

logging_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] ::%(levelname)s:: in %(name)s: %(pathname)s: %(funcName)s: %(message)s',
            'datefmt': '%Y-%b-%d %H:%M:%S',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': 'logs/log.txt',
            'maxBytes': 10485760,
            'backupCount': 3,
            'encoding': 'utf8',
        }
    },
    'loggers': {
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi', 'file']
        },
        'api': {
            
        }
    }
}