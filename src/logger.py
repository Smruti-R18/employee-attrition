import os
import logging
from datetime import datetime

LOG_FILE_NAME = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_dir = os.path.join(os.getcwd(),"logs")
os.makedirs(log_dir,exist_ok=True)
LOG_FILE_PATH = os.path.join(log_dir,LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format=" [ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)