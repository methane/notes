import structlog

structlog.configure(
    processors=[
        #tracer_injection,
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

def foo():
    1/0

try:
    foo()
except:
    logger.error("Does not print the exception")
    logger.exception("Prints the exception")
    logger.info("Also prints exception", exc_info=True)
