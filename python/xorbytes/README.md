# xorbytes

```
$ rye run python xor_bytes.py
.....................
list: Mean +- std dev: 7.59 us +- 0.12 us
.....................
generator: Mean +- std dev: 10.1 us +- 0.3 us
.....................
int: Mean +- std dev: 685 ns +- 7 ns
```


# ws_mask_bench.py

```
$ rye run python ws_mask_bench.py
.....................
_websocket_mask_python: Mean +- std dev: 6.35 us +- 0.07 us
.....................
tornado.speedups: Mean +- std dev: 63.1 ns +- 0.6 ns
.....................
websocket_mask_int: Mean +- std dev: 581 ns +- 6 ns
```
