import structlog
from structlog.processors import JSONRenderer

structlog.configure(processors=[JSONRenderer()])
logger = structlog.get_logger()

def hello():
    lg = structlog.get_context(logger)
    lg["foo"] = "bar"
    logger.info("hello") # {"foo": "bar", "event": "hello"}

hello()
logger.info("goodby", arg="world") # {"foo": "bar", "arg": "world", "event": "goodby"}
