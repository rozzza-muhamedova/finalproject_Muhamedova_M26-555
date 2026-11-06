import logging
import os
from logging.handlers import RotatingFileHandler

os.makedirs("logs", exist_ok=True)

def setup_logging():
    """Настраивает систему логирования."""

    logger = logging.getLogger("valutatrade")
    
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger
    
    handler = RotatingFileHandler(
        "logs/actions.log",
        maxBytes=1024 * 1024, 
        backupCount=3,
        encoding="utf-8",
    )
    
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

logger = setup_logging()