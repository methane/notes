## pyperformance

### empty-dict2 vs empty-dict 3

* emptydict2-opt.json: [empty-dict2](https://github.com/python/cpython/pull/12307) 06fdf74a2a
* emptydict3-opt.json: [empty-dict3](https://github.com/python/cpython/pull/12308) 815cf79847

lto: on, pgo: on

```
$ python -m perf compare_to emptydict2-opt.json emptydict3-opt.json -G --min-speed=1
Slower (8):
- regex_dna: 418 ms +- 1 ms -> 432 ms +- 6 ms: 1.03x slower (+3%)
- scimark_sor: 433 ms +- 4 ms -> 445 ms +- 4 ms: 1.03x slower (+3%)
- logging_simple: 15.5 us +- 0.1 us -> 15.8 us +- 0.2 us: 1.02x slower (+2%)
- logging_silent: 328 ns +- 7 ns -> 333 ns +- 8 ns: 1.01x slower (+1%)
- scimark_monte_carlo: 203 ms +- 2 ms -> 206 ms +- 1 ms: 1.01x slower (+1%)
- float: 185 ms +- 2 ms -> 187 ms +- 2 ms: 1.01x slower (+1%)
- sqlalchemy_imperative: 38.7 ms +- 0.8 ms -> 39.1 ms +- 1.3 ms: 1.01x slower (+1%)
- scimark_sparse_mat_mult: 13.6 ms +- 0.3 ms -> 13.7 ms +- 0.2 ms: 1.01x slower (+1%)

Faster (8):
- unpickle: 24.0 us +- 2.0 us -> 23.2 us +- 0.8 us: 1.04x faster (-4%)
- json_loads: 45.0 us +- 1.3 us -> 44.1 us +- 0.3 us: 1.02x faster (-2%)
- spectral_norm: 298 ms +- 3 ms -> 292 ms +- 2 ms: 1.02x faster (-2%)
- scimark_fft: 857 ms +- 8 ms -> 842 ms +- 5 ms: 1.02x faster (-2%)
- django_template: 205 ms +- 3 ms -> 201 ms +- 1 ms: 1.02x faster (-2%)
- unpack_sequence: 102 ns +- 2 ns -> 101 ns +- 1 ns: 1.01x faster (-1%)
- crypto_pyaes: 193 ms +- 1 ms -> 191 ms +- 1 ms: 1.01x faster (-1%)
- pickle_list: 6.83 us +- 0.14 us -> 6.75 us +- 0.06 us: 1.01x faster (-1%)
```

No significant performance different.

### before vs empty-dict2

before-opt is commit right before f2a186712b, which reduces size of empty dict.

* before-opt.josn: [master](https://github.com/python/cpython/commit/fc06a192fd) fc06a192fd
* emptydict2-opt.json: [empty-dict2](https://github.com/python/cpython/pull/12307) 06fdf74a2a

lto: on, pgo: on

```
ltf:re_to before-opt.json emptydict2-opt.json -G --min-speed=1
Slower (12):
- json_loads: 43.8 us +- 1.9 us -> 45.0 us +- 1.3 us: 1.03x slower (+3%)
- pickle_dict: 45.1 us +- 0.1 us -> 46.1 us +- 0.5 us: 1.02x slower (+2%)
- regex_v8: 62.1 ms +- 0.1 ms -> 63.5 ms +- 0.5 ms: 1.02x slower (+2%)
- django_template: 201 ms +- 2 ms -> 205 ms +- 3 ms: 1.02x slower (+2%)
- pickle_pure_python: 815 us +- 5 us -> 830 us +- 11 us: 1.02x slower (+2%)
- unpickle_list: 7.69 us +- 0.02 us -> 7.82 us +- 0.08 us: 1.02x slower (+2%)
- crypto_pyaes: 190 ms +- 1 ms -> 193 ms +- 1 ms: 1.02x slower (+2%)
- pathlib: 32.7 ms +- 0.3 ms -> 33.2 ms +- 0.3 ms: 1.01x slower (+1%)
- raytrace: 827 ms +- 5 ms -> 838 ms +- 7 ms: 1.01x slower (+1%)
- dulwich_log: 103 ms +- 1 ms -> 104 ms +- 1 ms: 1.01x slower (+1%)
- sqlalchemy_declarative: 231 ms +- 2 ms -> 234 ms +- 2 ms: 1.01x slower (+1%)
- sympy_expand: 631 ms +- 5 ms -> 638 ms +- 5 ms: 1.01x slower (+1%)

Faster (8):
- logging_silent: 345 ns +- 6 ns -> 328 ns +- 7 ns: 1.05x faster (-5%)
- regex_dna: 436 ms +- 6 ms -> 418 ms +- 1 ms: 1.04x faster (-4%)
- pidigits: 220 ms +- 0 ms -> 216 ms +- 0 ms: 1.02x faster (-2%)
- regex_effbot: 9.04 ms +- 0.05 ms -> 8.92 ms +- 0.07 ms: 1.01x faster (-1%)
- scimark_monte_carlo: 206 ms +- 3 ms -> 203 ms +- 2 ms: 1.01x faster (-1%)
- fannkuch: 917 ms +- 3 ms -> 906 ms +- 3 ms: 1.01x faster (-1%)
- scimark_sparse_mat_mult: 13.7 ms +- 0.3 ms -> 13.6 ms +- 0.3 ms: 1.01x faster (-1%)
- logging_simple: 15.7 us +- 0.2 us -> 15.5 us +- 0.1 us: 1.01x faster (-1%)

Benchmark hidden because not significant (37)
```

## micro benchmarks


* before: before reducing empty dict siae. [master](https://github.com/python/cpython/commit/fc06a192fd) fc06a192fd
* cpython: [empty-dict2](https://github.com/python/cpython/pull/12307) 06fdf74a2a
* empty-dict3: [empty-dict3](https://github.com/python/cpython/pull/12308) 815cf79847

### before vs empty-dict2

```
$ alias compare='./cpython/python.opt -m perf timeit --compare-to ./before/python.opt --python-names before:empty-dict2'

$ compare --duplicate 100 '{}'
before: ..................... 24.3 ns +- 0.6 ns
empty-dict2: ..................... 10.9 ns +- 0.2 ns

Mean +- std dev: [before] 24.3 ns +- 0.6 ns -> [empty-dict2] 10.9 ns +- 0.2 ns: 2.22x faster (-55%)

$ compare --duplicate 100 '{"a":1}'
before: ..................... 48.8 ns +- 0.3 ns
empty-dict2: ..................... 52.1 ns +- 0.5 ns

Mean +- std dev: [before] 48.8 ns +- 0.3 ns -> [empty-dict2] 52.1 ns +- 0.5 ns: 1.07x slower (+7%)

$ compare --duplicate 100 '{"a":1, "b":2}'
before: ..................... 79.8 ns +- 0.9 ns
empty-dict2: ..................... 84.3 ns +- 1.3 ns

Mean +- std dev: [before] 79.8 ns +- 0.9 ns -> [empty-dict2] 84.3 ns +- 1.3 ns: 1.06x slower (+6%)

$ compare --duplicate 100 'd={};d["a"]=1'
before: ..................... 56.3 ns +- 0.8 ns
empty-dict2: ..................... 52.3 ns +- 0.5 ns

Mean +- std dev: [before] 56.3 ns +- 0.8 ns -> [empty-dict2] 52.3 ns +- 0.5 ns: 1.08x faster (-7%)

$ compare --duplicate 100 'd={};d["a"]=1;d["b"]=2'
before: ..................... 104 ns +- 3 ns
empty-dict2: ..................... 101 ns +- 2 ns

Mean +- std dev: [before] 104 ns +- 3 ns -> [empty-dict2] 101 ns +- 2 ns: 1.03x faster (-3%)

$ compare -s 'd={"a":1}' --duplicate 100 '"a" in d'
before: ..................... 14.5 ns +- 0.3 ns
empty-dict2: ..................... 14.5 ns +- 0.3 ns

Mean +- std dev: [before] 14.5 ns +- 0.3 ns -> [empty-dict2] 14.5 ns +- 0.3 ns: 1.00x faster (-0%)
Not significant!

$ compare -s 'd={}' --duplicate 100 '"a" not in d'
before: ..................... 14.4 ns +- 0.1 ns
empty-dict2: ..................... 14.4 ns +- 0.1 ns

Mean +- std dev: [before] 14.4 ns +- 0.1 ns -> [empty-dict2] 14.4 ns +- 0.1 ns: 1.00x faster (-0%)
Not significant!

$ compare -s 'def foo(x, **kw): pass' -- 'foo(4)'
before: ..................... 83.6 ns +- 1.7 ns
empty-dict2: ..................... 67.6 ns +- 1.8 ns

Mean +- std dev: [before] 83.6 ns +- 1.7 ns -> [empty-dict2] 67.6 ns +- 1.8 ns: 1.24x faster (-19%)
```

### empty-dict2 vs empty-dict3

```
lias compare='./empty-dict3/python.opt -m perf timeit --compare-to ./cpython/python.opt --python-names empty-dict2:empty-dict3'

$ compare --duplicate 100 '{}'
empty-dict2: ..................... 11.1 ns +- 0.4 ns
empty-dict3: ..................... 9.71 ns +- 0.19 ns

Mean +- std dev: [empty-dict2] 11.1 ns +- 0.4 ns -> [empty-dict3] 9.71 ns +- 0.19 ns: 1.14x faster (-12%)

$ compare --duplicate 100 '{"a":1}'
empty-dict2: ..................... 52.2 ns +- 0.6 ns
empty-dict3: ..................... 51.5 ns +- 0.4 ns

Mean +- std dev: [empty-dict2] 52.2 ns +- 0.6 ns -> [empty-dict3] 51.5 ns +- 0.4 ns: 1.01x faster (-1%)

$ compare --duplicate 100 '{"a":1, "b":2}'
empty-dict2: ..................... 84.7 ns +- 1.6 ns
empty-dict3: ..................... 82.7 ns +- 1.1 ns

Mean +- std dev: [empty-dict2] 84.7 ns +- 1.6 ns -> [empty-dict3] 82.7 ns +- 1.1 ns: 1.02x faster (-2%)

$ compare --duplicate 100 'd={};d["a"]=1'
empty-dict2: ..................... 52.7 ns +- 1.7 ns
empty-dict3: ..................... 49.7 ns +- 0.3 ns

Mean +- std dev: [empty-dict2] 52.7 ns +- 1.7 ns -> [empty-dict3] 49.7 ns +- 0.3 ns: 1.06x faster (-6%)

$ compare --duplicate 100 'd={};d["a"]=1;d["b"]=2'
empty-dict2: ..................... 102 ns +- 3 ns
empty-dict3: ..................... 99.3 ns +- 1.3 ns

Mean +- std dev: [empty-dict2] 102 ns +- 3 ns -> [empty-dict3] 99.3 ns +- 1.3 ns: 1.03x faster (-2%)

$ compare -s 'd={"a":1}' --duplicate 100 '"a" in d'
empty-dict2: ..................... 14.7 ns +- 1.1 ns
empty-dict3: ..................... 14.7 ns +- 0.1 ns

Mean +- std dev: [empty-dict2] 14.7 ns +- 1.1 ns -> [empty-dict3] 14.7 ns +- 0.1 ns: 1.00x faster (-0%)
Not significant!

$ compare -s 'd={}' --duplicate 100 '"a" not in d'
empty-dict2: ..................... 14.4 ns +- 0.2 ns
empty-dict3: ..................... 10.6 ns +- 0.2 ns

Mean +- std dev: [empty-dict2] 14.4 ns +- 0.2 ns -> [empty-dict3] 10.6 ns +- 0.2 ns: 1.36x faster (-26%)

$ compare -s 'def foo(x, **kw): pass' -- 'foo(4)'
empty-dict2: ..................... 68.7 ns +- 2.4 ns
empty-dict3: ..................... 66.8 ns +- 1.1 ns

Mean +- std dev: [empty-dict2] 68.7 ns +- 2.4 ns -> [empty-dict3] 66.8 ns +- 1.1 ns: 1.03x faster (-3%)
```
