import datetime
import logging
import sys
import structlog
import structlog.processors as _procs


_renderer = _procs.JSONRenderer()
#_renderer = _procs.LogfmtRenderer()

# JSONRendererにはkey_orderがないので自分でやる.
# ついでにEventRenamer("message")相当のこともやってしまう.
def _sort_keys(logger, name, event):
    new = {}
    new["timestamp"] = event.pop("timestamp")
    new["level"] = event.pop("level")
    new["message"] = event.pop("event")
    new.update(event)
    return new

structlog.configure(
    cache_logger_on_first_use=True, # for performance
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=[
        _procs.TimeStamper(fmt="iso", utc=True),
        _procs.add_log_level,
        _procs.format_exc_info,
        #_procs.EventRenamer("message"),  # _sort_keysの中でやる
        _sort_keys,
        # filename等は後ろに追加する
        _procs.CallsiteParameterAdder([
            _procs.CallsiteParameter.FILENAME,
            _procs.CallsiteParameter.LINENO,
            _procs.CallsiteParameter.FUNC_NAME,
        ]),
        _renderer,
    ],
    # 出力先をlogging.StreamHandlerと同じstderrに揃える.
    logger_factory=structlog.PrintLoggerFactory(sys.stderr),
)

# configure stdlib logging

# loggingのLoggerとstructlogを連結すると、LogRecordの生成コストがかかるので、それぞれが
# 独自に sys.stderr に書き込む形にする。
# structlogのDon't Integrateパターン
# https://www.structlog.org/en/stable/standard-library.html#dont-integrate

## Using jsonlogger
## structlogのドキュメントで紹介されていたのがこれ。structlogと別にインストールしないと
## いけないし、設定しないといけないのが面倒.

from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
#formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')

## Using structlog ProcessorFormatter
# jsonloggerではなくstructlog.stdlib.ProcessorFormetter を使うことでログのフォーマットを
# structlogに合わせやすくなる。
# logger.name は structlog には存在しないのでstdlib logger独自になる。

# event["_record"] から eventへの変換
# processorsの先頭か、foreign_pre_chainに使うこと
def _record_to_event(lg, name, ed):
    rec : logging.LogRecord = ed["_record"]
    ed["timestamp"] = datetime.datetime.utcfromtimestamp(rec.created).isoformat()+'Z'
    ed["logger"] = rec.name
    #ed["level"] = rec.levelname.lower()  # structlogに合わせてlowerで
    ed["level"] = structlog.stdlib.LEVEL_TO_NAME[rec.levelno]
    # CallsiteParameterAdderと同じキー名を使う。
    ed["filename"] = rec.filename
    ed["lineno"] = rec.lineno
    ed["func_name"] = rec.funcName
    return ed

formatter = structlog.stdlib.ProcessorFormatter(
    foreign_pre_chain = [_record_to_event],
    processors = [
        _procs.format_exc_info,
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        _sort_keys,
        _renderer,
    ]
)

root_logger = logging.getLogger()
logHandler = logging.StreamHandler()
logHandler.setFormatter(formatter)
root_logger.addHandler(logHandler)
root_logger.setLevel(logging.INFO)


# use structlog

# structlogにはlogger.nameがないので、独自に logger="logger name" をbind
# することで出力を揃える.
logger = structlog.stdlib.get_logger().bind(logger="structlog_logger")

def hello():
    log = logger.bind(foo="bar")
    log.warn("hello") # {"foo": "bar", "event": "hello"}

hello()
logger.info("goodby", arg="world") # {"arg": "world", "event": "goodby"}

# use stdlib logging

std_logger = logging.getLogger("stdlib_logger")
std_logger.info("hello, hello,")

def world():
    std_logger.warning("hello, from %s", "world")

world()
