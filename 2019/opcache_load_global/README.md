# OPCache for LOAD_GLOBAL

## micro benchmark

```
$ master/python -m perf timeit -s 'def foo(): int; str; bytes; float; int; str; bytes; float' -- 'foo()'
.....................
Mean +- std dev: 213 ns +- 5 ns

$ opcache/python -m perf timeit -s 'def foo(): int; str; bytes; float; int; str; bytes; float' -- 'foo()'
.....................
Mean +- std dev: 120 ns +- 2 ns
```

## performance

master: 9d062d690b768252204992fc6ab7c3873a87442d
opcache_load_global: 7f3fc85d375f294b61155035409fcdf6035d1d10

```
$ ./cpython/python -m perf compare_to master.json opcache_load_global.json -G  --min-speed=2
Slower (2):
- pickle: 19.1 us +- 0.2 us -> 19.7 us +- 0.8 us: 1.03x slower (+3%)
- unpickle_list: 8.66 us +- 0.04 us -> 8.85 us +- 0.06 us: 1.02x slower (+2%)

Faster (23):
- scimark_lu: 424 ms +- 22 ms -> 384 ms +- 4 ms: 1.10x faster (-9%)
- regex_compile: 359 ms +- 4 ms -> 330 ms +- 1 ms: 1.09x faster (-8%)
- django_template: 250 ms +- 3 ms -> 231 ms +- 2 ms: 1.08x faster (-8%)
- unpickle_pure_python: 802 us +- 12 us -> 754 us +- 9 us: 1.06x faster (-6%)
- pickle_pure_python: 1.04 ms +- 0.01 ms -> 991 us +- 15 us: 1.05x faster (-5%)
- hexiom: 20.8 ms +- 0.2 ms -> 19.8 ms +- 0.1 ms: 1.05x faster (-5%)
- logging_simple: 18.4 us +- 0.2 us -> 17.6 us +- 0.2 us: 1.05x faster (-4%)
- sympy_expand: 774 ms +- 5 ms -> 741 ms +- 3 ms: 1.04x faster (-4%)
- json_dumps: 28.1 ms +- 0.2 ms -> 27.0 ms +- 0.2 ms: 1.04x faster (-4%)
- logging_format: 20.4 us +- 0.2 us -> 19.6 us +- 0.3 us: 1.04x faster (-4%)
- richards: 147 ms +- 2 ms -> 141 ms +- 1 ms: 1.04x faster (-4%)
- meteor_contest: 189 ms +- 1 ms -> 182 ms +- 1 ms: 1.04x faster (-4%)
- xml_etree_iterparse: 226 ms +- 2 ms -> 217 ms +- 2 ms: 1.04x faster (-4%)
- sympy_str: 358 ms +- 3 ms -> 345 ms +- 4 ms: 1.04x faster (-4%)
- sqlalchemy_imperative: 44.0 ms +- 1.2 ms -> 42.4 ms +- 1.2 ms: 1.04x faster (-4%)
- sympy_sum: 167 ms +- 1 ms -> 161 ms +- 1 ms: 1.04x faster (-4%)
- nqueens: 217 ms +- 1 ms -> 211 ms +- 1 ms: 1.03x faster (-3%)
- fannkuch: 1.09 sec +- 0.01 sec -> 1.07 sec +- 0.00 sec: 1.03x faster (-3%)
- raytrace: 1.11 sec +- 0.02 sec -> 1.08 sec +- 0.01 sec: 1.03x faster (-3%)
- dulwich_log: 122 ms +- 1 ms -> 119 ms +- 1 ms: 1.03x faster (-3%)
- logging_silent: 419 ns +- 5 ns -> 410 ns +- 5 ns: 1.02x faster (-2%)
- sympy_integrate: 33.5 ms +- 0.1 ms -> 32.8 ms +- 0.2 ms: 1.02x faster (-2%)
- pathlib: 40.8 ms +- 0.4 ms -> 40.0 ms +- 0.5 ms: 1.02x faster (-2%)

Benchmark hidden because not significant (32): 2to3, chaos, crypto_pyaes, deltablue, float, go, html5lib, json_loads, mako, nbody, pickle_dict, pickle_list, pidigits, python_startup, python_startup_no_site, regex_dna, regex_effbot, regex_v8, scimark_fft, scimark_monte_carlo, scimark_sor, scimark_sparse_mat_mult, spectral_norm, sqlalchemy_declarative, sqlite_synth, telco, tornado_http, unpack_sequence, unpickle, xml_etree_parse, xml_etree_generate, xml_etree_process
```
