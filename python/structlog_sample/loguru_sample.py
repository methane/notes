from loguru import logger
import sys

logger.add(sys.stdout, serialize=True)
logger.info("hello, {user}", user="methane", age=40)
