from functions import *
import sys
import configparser
import logging
import time

logging.basicConfig(filename='logs/logs_' + time.strftime('%Y-%m-%d') + '.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

#load config file
config = configparser.ConfigParser()
config.read('config.ini')

#enter menu() at start
decision = 8

try:
	#main loop
	while True:
		#upload
	    if decision == 1:
	        upload(config)
	        decision = menu()
		#settings
	    elif decision == 7:
	        settings()
	        decision = menu()
	    elif decision == 8:
		#menu
	        decision = menu()
		#about
	    elif decision == 9:
	        about()
	        decision = menu()
		#exit
	    elif decision == 0:
	        sys.exit(0)

except Exception as err:
    logger.error(err)
