import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler


# Trivial LevelSpecificFormatter for better bug hunting
class LevelSpecificFormatter(logging.StreamHandler):
    def __init__(self, stream=sys.stdout):
        super().__init__(stream)

    def emit(self, record):
        if record.levelno == logging.DEBUG:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        elif record.levelno == logging.INFO:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        elif record.levelno == logging.WARNING:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s():%(lineno)d - %(levelname)s - %(message)s')
        elif record.levelno == logging.ERROR:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s():%(lineno)d - %(levelname)s - %(message)s')
        elif record.levelno == logging.CRITICAL:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s():%(lineno)d - %(levelname)s - %(message)s')
        else:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.setFormatter(formatter)
        super().emit(record)

def get_custom_logger(name:str, log_dir:str=None, format:str="short", level:int=logging.DEBUG) -> logging.Logger:
    """
        Define a custom logger that writes to file if log_dir is not None.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # handler = logging.StreamHandler(stream=sys.stdout)
    # if format == "short":
    #     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # else:
    #     formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    handler = LevelSpecificFormatter()
    logger.addHandler(handler)


    # Define settings for file output
    if (log_dir is not None):
        if os.path.exists(log_dir) == False:
            os.makedirs(
                os.path.abspath(
                    os.path.join(os.path.basename(__file__), os.pardir, log_dir)    
                )
            )
        # Define logs that change daily
        file_handler = TimedRotatingFileHandler(
            os.path.join(log_dir, f"application.log"),
            when="MIDNIGHT",
            backupCount=10,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger