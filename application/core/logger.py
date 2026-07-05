import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory
LOG_DIR = "logs"
LOG_FILE = "app.log"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)


def setup_logger():
    logger = logging.getLogger("rag_app")
    logger.setLevel(logging.INFO)

    # Avoid duplicate logs
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        LOG_PATH,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logger()