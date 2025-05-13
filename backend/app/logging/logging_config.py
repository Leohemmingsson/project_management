import logging
import sys

logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log")

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
