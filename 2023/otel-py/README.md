# otel-py

measure overhead of instrumentations.

## text output

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

real	0m1.075s
user	0m1.024s
sys	0m0.032s

# opentelemetry
$ time .venv/bin/python script.py

real	0m11.381s
user	0m11.210s
sys	0m0.268s

# ddtrace
$ time .venv/bin/python script.py

real	0m7.821s
user	0m7.208s
sys	0m0.590s
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

