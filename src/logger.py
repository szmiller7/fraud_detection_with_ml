# set up logging configuration to track what happens during the programme execution

import logging 
import os
from datetime import datetime

# create variable with filename based on the current datetime
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# create logs dir and add enure that if the dir exists it won't raise an error
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

# create full path to the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# configure the logging system
logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO, 
)
