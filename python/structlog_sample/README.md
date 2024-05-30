# structlog-test

structlogの使い方を試す

json_sample.py -- structlogとstdlibのloggingの両方でフォーマットを揃えてJSONを出力してみる


## 2024/03/27 stdlibとの連携

https://github.com/hynek/structlog/commit/6959f1d55568f9a743309c6824be32ca48e90192

このパッチを適用済み

```
methane@skyland:~/notes/structlog-test (master =)$ .venv/bin/python stdlib_bench.py
CALLSITE=False N=100000
stdlib: 20145ns
stdlib+ProcessorFormatter: 35324ns
structlog+stdlib+ProcessorFormatter: 45063ns

methane@skyland:~/notes/structlog-test (master =)$ CALLSITE=1 .venv/bin/python stdlib_bench.py
CALLSITE=True N=100000
stdlib: 19964ns
stdlib+ProcessorFormatter: 52585ns
structlog+stdlib+ProcessorFormatter: 60687ns

methane@skyland:~/notes/structlog-test (master =)$ .venv/bin/python logformat_bench.py
CALLSITE=False ORJSON=False N=100000
stdlib: 16008ns
stdlib+ProcessorFormatter: 30076ns
stdlib+json_formatter: 26234ns
structlog: 11394ns

methane@skyland:~/notes/structlog-test (master =)$ CALLSITE=1 .venv/bin/python logformat_bench.py
CALLSITE=True ORJSON=False N=100000
stdlib: 16217ns
stdlib+ProcessorFormatter: 33315ns
stdlib+json_formatter: 25804ns
structlog: 19898ns

methane@skyland:~/notes/structlog-test (master =)$ CALLSITE=1 ORJSON=1 .venv/bin/python logformat_bench.py
CALLSITE=True ORJSON=True N=100000
stdlib: 15841ns
stdlib+ProcessorFormatter: 33806ns
stdlib+json_formatter: 25839ns
structlog: 15110ns
```
