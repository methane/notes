# https://www.structlog.org/en/stable/standard-library.html#rendering-using-structlog-based-formatters-within-logging
# structlogがlogging.Loggerを呼び出す形でログ出力するベンチマーク
# logformat_bench.py は output だけシェアする形なので、それに比べて
# どれだけ遅くなるかを調べる.

import datetime
import logging
import sys
import structlog
import structlog.processors as _procs
import timeit
import os

# ログにfunc_name, filename, linenoをつけるか
# 大幅に性能に影響するのでそれぞれでベンチ取る
CALLSITE = bool(os.environ.get("CALLSITE", 0))

N = 100_000
devnull = open(os.devnull, "w", encoding="utf-8")

if bool(os.environ.get("TEST")):  # 出力確認用
    N = 1
    devnull = sys.stderr

if CALLSITE:
    callsite_procs = [
        _procs.CallsiteParameterAdder(
            [
                _procs.CallsiteParameter.FILENAME,
                _procs.CallsiteParameter.LINENO,
                _procs.CallsiteParameter.FUNC_NAME,
            ]
        ),
    ]
else:
    callsite_procs = []

_renderer = _procs.JSONRenderer()


# JSONRendererにはkey_orderがないので自分でやる.
# ついでにEventRenamer("message")相当のこともやってしまう.
def _sort_keys(logger, name, event):
    new = {
        "timestamp": event["timestamp"],
        "level": event["level"],
        "message": event.pop("event"),
    }
    new.update(event)
    return new


structlog.configure(
    cache_logger_on_first_use=True,  # for performance
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=[
        _procs.TimeStamper(fmt="iso", utc=True),
        _procs.add_log_level,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)


# event["_record"] から eventへの変換
# structlog.stdlib.ProcessorFormatterがやってくれない部分をカバー
# processorsの先頭か、foreign_pre_chainに使うこと
def _record_to_event(lg, name, ed):
    rec: logging.LogRecord = ed["_record"]
    ed["timestamp"] = datetime.datetime.utcfromtimestamp(rec.created).isoformat() + "Z"
    ed["logger"] = rec.name
    # ed["level"] = rec.levelname.lower()  # structlogに合わせてlowerで
    ed["level"] = structlog.stdlib.LEVEL_TO_NAME[rec.levelno]
    # CallsiteParameterAdderが_recordからの変換に対応していたので以下は不要
    # ed["filename"] = rec.filename
    # ed["lineno"] = rec.lineno
    # ed["func_name"] = rec.funcName
    return ed


structlog_formatter = structlog.stdlib.ProcessorFormatter(
    # 1つのformatterをstructlogとstdlibで共有するときは、stdlibでだけ
    # 実行する処理はforeign_pre_chainに書く。
    # 別々に用意するときは分けなくて良い。
    foreign_pre_chain=[_record_to_event],
    processors=[
        # CallsiteParameterAdderは_recordからの情報取得に対応している
        _procs.format_exc_info,
        *callsite_procs,
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        _sort_keys,
        _renderer,
    ],
)

stdlib_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s:%(lineno)s %(funcName)s"
)
root_logger = logging.getLogger()
logHandler = logging.StreamHandler(devnull)
root_logger.addHandler(logHandler)
root_logger.setLevel(logging.INFO)

stdlib_logger = logging.getLogger("stdlib_logger")

# use structlog

# structlogにはlogger.nameがないので、独自に logger="logger name" をbind
# することで出力を揃える.
struct_logger = structlog.get_logger().bind(logger="struct_logger")


def hello(logger):
    logger.warning("hello")  # {"foo": "bar", "event": "hello"}
    logger.info("goodby %s", "world")  # {"arg": "world", "event": "goodby"}


def to_ns(t):
    return f"{int(x*1000_000_000/N)}ns"


print(f"{CALLSITE=} {N=}")

logHandler.setFormatter(stdlib_formatter)
x = timeit.timeit(lambda: hello(stdlib_logger), number=N)
print("stdlib:", to_ns(x))

logHandler.setFormatter(structlog_formatter)
x = timeit.timeit(lambda: hello(stdlib_logger), number=N)
print("stdlib+ProcessorFormatter:", to_ns(x))

x = timeit.timeit(lambda: hello(struct_logger), number=N)
print("structlog+stdlib+ProcessorFormatter:", to_ns(x))
