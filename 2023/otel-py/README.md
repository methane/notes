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

サンプリングレートを1/100にすることで、オーバーヘッドが約25秒から5秒へと1/5に減っている。

計装自体のオーバーヘッドがある程度大きいので、1/100サンプリングでもオーバーヘッドが1/100にならないことには注意する必要がある。
オーバーヘッドに関して言えば1/100だと絞りすぎで、1/10程度にしておいて、あとは転送量やログ保存料金を考えてtail based samplingと組み合わせるのがよさそう。


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

サンプリングよりもさらに高速になっている。spanは余計な情報がつくためで、数が多いイベントは開始・終了があってもスパンではなくイベントにした方がデータ量と速度両方に効果がありそう。

オーバーヘッドのほとんどは別スレッドで動いているファイルへのJSON出力。

## events + sampling

```
$ time python otel-events.py 0.1
sampling rate=0.1

real    0m2.806s
user    0m2.780s
sys     0m0.033s
```

すごい減った。やはりサンプリングレートは0.1で十分ぽい。

