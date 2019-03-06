Change set implementation to compact & ordered, similar to dict.

https://mail.python.org/pipermail/python-dev/2019-February/156466.html

## Benchmark

[code](./bm_set.py)

Result:

```
$ ./python -m perf compare_to set_master.json set_oset.json -G --min-speed=3
Slower (16):
- creation_int(100): 1.78 us +- 0.02 us -> 2.14 us +- 0.05 us: 1.20x slower (+20%)
- creation_int(20): 581 ns +- 4 ns -> 691 ns +- 5 ns: 1.19x slower (+19%)
- creation_int(500): 10.5 us +- 0.2 us -> 11.8 us +- 0.1 us: 1.13x slower (+13%)
- mishit(500): 16.9 ns +- 0.6 ns -> 18.6 ns +- 1.7 ns: 1.10x slower (+10%)
- contains_str(500): 30.1 ns +- 0.8 ns -> 32.4 ns +- 0.9 ns: 1.08x slower (+8%)
- contains_int(20): 18.0 ns +- 0.2 ns -> 19.4 ns +- 0.2 ns: 1.08x slower (+8%)
- mishit(5): 16.5 ns +- 0.4 ns -> 17.8 ns +- 0.6 ns: 1.08x slower (+8%)
- contains_int(5): 18.1 ns +- 0.4 ns -> 19.5 ns +- 0.3 ns: 1.07x slower (+7%)
- contains_int(100): 18.1 ns +- 0.3 ns -> 19.4 ns +- 0.2 ns: 1.07x slower (+7%)
- creation_int(5): 293 ns +- 2 ns -> 314 ns +- 2 ns: 1.07x slower (+7%)
- mishit(100): 16.5 ns +- 0.3 ns -> 17.6 ns +- 0.6 ns: 1.07x slower (+7%)
- contains_str(100): 29.7 ns +- 0.2 ns -> 31.6 ns +- 0.2 ns: 1.06x slower (+6%)
- contains_int(500): 18.8 ns +- 0.1 ns -> 20.0 ns +- 0.2 ns: 1.06x slower (+6%)
- mishit(20): 16.8 ns +- 0.7 ns -> 17.8 ns +- 1.0 ns: 1.06x slower (+6%)
- contains_str(20): 29.9 ns +- 0.7 ns -> 31.7 ns +- 0.6 ns: 1.06x slower (+6%)
- contains_str(5): 29.8 ns +- 0.4 ns -> 31.3 ns +- 0.5 ns: 1.05x slower (+5%)

Faster (8):
- creation_str(500): 11.4 us +- 1.3 us -> 9.49 us +- 0.17 us: 1.20x faster (-17%)
- pop(500): 33.3 us +- 1.7 us -> 28.4 us +- 0.3 us: 1.18x faster (-15%)
- remove_and_add(500): 32.8 us +- 2.0 us -> 28.6 us +- 0.4 us: 1.15x faster (-13%)
- pop(100): 5.82 us +- 0.10 us -> 5.27 us +- 0.09 us: 1.10x faster (-9%)
- remove_and_add(100): 5.85 us +- 0.07 us -> 5.30 us +- 0.09 us: 1.10x faster (-9%)
- creation_str(100): 2.10 us +- 0.09 us -> 1.98 us +- 0.04 us: 1.06x faster (-6%)
- remove_and_add(20): 1.57 us +- 0.03 us -> 1.49 us +- 0.02 us: 1.05x faster (-5%)
- pop(20): 1.56 us +- 0.03 us -> 1.48 us +- 0.02 us: 1.05x faster (-5%)
```
