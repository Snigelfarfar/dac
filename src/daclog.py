#!/usr/bin/python2.7
import logging, sys
from logging import config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)-8s: %(module)s/%(funcName)s/%(lineno)d %(message)s'
            },
        'basic': {
            'format': '%(asctime)s %(message)s',
	    'datefmt': '%b %d %T'
            },
        },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'basic',
            },
        'sys-logger6': {
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'facility': "local6",
            'formatter': 'verbose',
            },
        },
    'loggers': {
        'dac-logger': {
            'handlers': ['sys-logger6','stdout'],
            'level': logging.DEBUG,
            'propagate': True,
            },
        }
    }

class DacLog(logging.StreamHandler):
    def __init__(self):
	logging.StreamHandler.__init__(self)
	self.config = config.dictConfig(LOGGING)

#EXAMPLE:
#from src.daclog import DacLog
#DacLog()
#log = logging.getLogger("dac-logger")
#log.info("WEHOooo")


#This works
#config.dictConfig(LOGGING)

#logger = logging.getLogger("dac-logger")
#
#logger.debug("Debug")
#logger.info("Info")
#logger.warn("Warn")
#logger.error("Error")
#logger.critical("Critical")
