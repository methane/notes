# https://github.com/hynek/structlog/pull/607

import structlog
import logging

# Use structlog's findCaller()
structlog.stdlib.LoggerFactory()

import logging
import sys, os

devnull = open(os.devnull, "w", encoding="utf-8")

logging.basicConfig(
    format="%(message)s",
    stream=devnull,
    level=logging.INFO,
)

logger = logging.getLogger("hello")
print(logger)

import timeit

def foo():
    logger.info("hello %s", "world")

N = 1000_000
x = timeit.timeit(foo, number=N)
print(f"{x*1000000/N:.3f}us")
