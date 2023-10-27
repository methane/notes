# otel-py

measure overhead of instrumentations.

## text output

ddtraceとotelをテキスト出力モードにして、計装時のオーバーヘッドを計測してみる。
軽装対象はsqlite3


```py
# see script.py ...

#enable_ddtrace()
#enable_otel()

for _ in range(10000):
    test()
```

output:

```
# no instrument
$ time .venv/bin/python script.py

real    0m1.825s
user    0m1.809s
sys     0m0.016s

# opentelemetry

real    0m27.088s
user    0m26.912s
sys     0m0.617s

# ddtrace

real    0m25.780s
user    0m24.402s
sys     0m1.177s
```

## head based smaplign

head based sampling でオーバーヘッドを削減できるかを試してみた。

./otel-sampling.py  -- ソース
./otel-sampled.out  -- 出力
./otel-sampling-profile.svg -- py-spyで取得したプロファイル結果

```
$ time python otel-sampling.py 0.01
sampling rate=0.01

real    0m7.097s
user    0m7.085s
sys     0m0.016s

$ wc -l otel-sampled.out
62934 otel-sampled.out
```

少し減ったけど、1/100にサンプリングした割にオーバーヘッドは半分にもなっていない。
これだけしか効果がないなら tail based sampling だけでいいのでは。


## events

sqlite3への自動計装を止めて、spanではなくeventでタイミングを記録してみる。

./otel-events.py  -- ソース
./otel-events.out  -- 出力
./otel-events-prof.svg -- py-spyで取得したプロファイル結果

```
$ time python otel-events.py

real    0m6.132s
user    0m6.139s
sys     0m0.140s
```

まだ遅いが、1/100サンプリングよりは速くなった。



