import pyperf
import dictbench

runner = pyperf.Runner()
for size in (1, 5, 10, 25, 100, 500, 1000):
    runner.bench_time_func('dict-{:,}'.format(size), dictbench.bench_new, size)
