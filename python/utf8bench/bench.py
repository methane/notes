# import utf8bench.ext
# print(utf8bench.ext.__file__)
from utf8bench.ext import decode1, decode_duckdb
import pyperf

runner = pyperf.Runner()

short_ascii = b"hello" * 2
long_ascii = short_ascii * 100

short_utf8 = "こんにちは".encode() * 2
long_utf8 = short_utf8 * 100

short_mixed = short_ascii + short_utf8
long_mixed = long_ascii + long_utf8

assert short_utf8.decode() == decode1(short_utf8) == decode_duckdb(short_utf8)


def add_bench_func(name, arg):
    runner.bench_func(name + " with Py/C API", decode1, arg, inner_loops=1000)
    runner.bench_func(name + " with DuckDB decoder", decode_duckdb, arg, inner_loops=1000)


add_bench_func("short ascii", short_ascii)
add_bench_func("long ascii", long_ascii)
add_bench_func("short utf8", short_utf8)
add_bench_func("long utf8", long_utf8)
#add_bench_func("short mixed", short_mixed)
#add_bench_func("long mixed", long_mixed)
