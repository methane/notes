# otel-py

measure overhead of instrumentations.

```
model name      : Intel(R) Core(TM) i5-8279U CPU @ 2.40GHz
Python 3.11.6 (main, Oct  3 2023, 01:26:22) [Clang 17.0.1 ]
```


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

root trace を手動で追加した

N=1あたりのtraceの数は、root,create,insert,select*20で合計23個.

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

オーバーヘッドの変化を観察するために追試

```
$ bash bench.sh
N = 10000, sampling rate = 1.0

real    0m26.599s
user    0m26.564s
sys     0m0.209s

N = 10000, sampling rate = 0.5

real    0m17.505s
user    0m17.501s
sys     0m0.104s

N = 10000, sampling rate = 0.1

real    0m9.498s
user    0m9.457s
sys     0m0.064s

N = 10000, sampling rate = 0.05

real    0m8.366s
user    0m8.361s
sys     0m0.016s

N = 10000, sampling rate = 0.0

real    0m7.231s
user    0m7.194s
sys     0m0.036s
```

## events

sqlite3への自動計装を止めて、spanではなくeventでタイミングを記録してみる。

N=1あたり、root trace + 22 events

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

スクリプトを改良後取り直し

```
N = 10000, sampling rate = 1.0

real    0m5.648s
user    0m5.628s
sys     0m0.048s

N = 10000, sampling rate = 0.5

real    0m4.134s
user    0m4.126s
sys     0m0.024s

N = 10000, sampling rate = 0.1

real    0m2.853s
user    0m2.826s
sys     0m0.028s

N = 10000, sampling rate = 0.05

real    0m2.587s
user    0m2.571s
sys     0m0.016s

N = 10000, sampling rate = 0.0

real    0m2.477s
user    0m2.453s
sys     0m0.024s
```


## まとめ

まず、計測に使ったCPUが古いかつノートPC向けのものなので、今時のサーバーなら2倍は速いはず。

- トレースなしが約2秒
- 23万トレースで約27秒
- 1万トレース+22万イベントで約6秒

ざっくりと、1万トレース/秒、7~8万イベント/秒程度と見積もればいい。

1トレースあたりだと約0.1msなので、5~10ms以上かかるようなネットワーク経由のサービス呼び出し(redisなど)については自動計装に任せてしまって、気になるようであればhead based samplingを少しかける程度でいいだろう。

sqlite3のようなインメモリの操作の場合、1リクエストあたりのオーバーヘッドのバジェットをざっくりと考えて、自動計装で重い場合は手動trace,eventを実装していく。（重いループの外でtrace,中でeventなど）
例えばオーバーヘッドを10ms以下にしたいなら、トレースなら100個、イベントなら7~800個以下に抑える。
