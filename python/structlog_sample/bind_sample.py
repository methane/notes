import structlog
from structlog.processors import JSONRenderer

structlog.configure(processors=[JSONRenderer()])
logger = structlog.get_logger()

def hello():
    log = logger.bind(foo="bar")
    log.info("hello") # {"foo": "bar", "event": "hello"}

hello()
logger.info("goodby", arg="world") # {"arg": "world", "event": "goodby"}
