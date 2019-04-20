
"""Script for testing the performance of pickling/unpickling.

This will pickle/unpickle several real world-representative objects a few
thousand times. The methodology below was chosen for was chosen to be similar
to real-world scenarios which operate on single objects at a time. Note that if
we did something like

    pickle.dumps([dict(some_dict) for _ in xrange(10000)])

this isn't equivalent to dumping the dict 10000 times: pickle uses a
highly-efficient encoding for the n-1 following copies.
"""

from __future__ import division

import perf


def template(loops, n):
    range_it = range(loops)
    range_x = range(n)

    t0 = perf.perf_counter()

    for _ in range_it:
        set(range_x)

    return perf.perf_counter() - t0


def creation_int(loops, n):
    range_it = range(loops)
    range_x = range(n)

    t0 = perf.perf_counter()

    for _ in range_it:
        set(range_x)
        set(range_x)
        set(range_x)
        set(range_x)
        set(range_x)
        set(range_x)
        set(range_x)
        set(range_x)
        set(range_x)
        set(range_x)

    return perf.perf_counter() - t0


def creation_str(loops, n):
    L = [f"s{i}" for i in range(n)]
    range_it = range(loops)

    t0 = perf.perf_counter()

    for _ in range_it:
        set(L)
        set(L)
        set(L)
        set(L)
        set(L)
        set(L)
        set(L)
        set(L)
        set(L)
        set(L)

    return perf.perf_counter() - t0
    

def contains_int(loops, n):
    range_it = range(loops)
    s = set(range(n))

    t0 = perf.perf_counter()

    for _ in range_it:
        0 in s
        0 in s
        0 in s
        0 in s
        0 in s
        0 in s
        0 in s
        0 in s
        0 in s
        0 in s

    return perf.perf_counter() - t0



def contains_str(loops, n):
    range_it = range(loops)
    s = set(f"s{i}" for i in range(n))

    t0 = perf.perf_counter()

    for _ in range_it:
        "s0" in s
        "s0" in s
        "s0" in s
        "s0" in s
        "s0" in s
        "s0" in s
        "s0" in s
        "s0" in s
        "s0" in s
        "s0" in s

    return perf.perf_counter() - t0


def mishit(loops, n):
    range_it = range(loops)
    s = set(f"s{i}" for i in range(n))

    t0 = perf.perf_counter()

    for _ in range_it:
        "ss" in s
        "ss" in s
        "ss" in s
        "ss" in s
        "ss" in s
        "ss" in s
        "ss" in s
        "ss" in s
        "ss" in s
        "ss" in s

    return perf.perf_counter() - t0


def pop(loops, n):
    range_it = range(loops)
    s = set(f"s{i}" for i in range(n))

    t0 = perf.perf_counter()

    for _ in range_it:
        t = s.copy()
        for _ in range(n):
            t.pop()

    return perf.perf_counter() - t0


def remove_and_add(loops, n):
    range_it = range(loops)
    t = [f"s{i}" for i in range(n*2)]
    a = t[:n]
    b = t[n:]

    t0 = perf.perf_counter()

    for _ in range_it:
        s = set(a)
        for j, k in zip(a, b):
            s.remove(j)
            s.add(k)

    return perf.perf_counter() - t0


if __name__ == "__main__":
    runner = perf.Runner()
    runner.metadata['description'] = "microbench for set operations"

    ns = (5, 20, 100, 500)

    for n in ns:
        runner.bench_time_func(f"creation_int({n})", creation_int, n, inner_loops=10)

    for n in ns:
        runner.bench_time_func(f"creation_str({n})", creation_str, n, inner_loops=10)

    for n in ns:
        runner.bench_time_func(f"contains_int({n})",   contains_int, n, inner_loops=10)

    for n in ns:
        runner.bench_time_func(f"contains_str({n})",   contains_str, n, inner_loops=10)

    for n in ns:
        runner.bench_time_func(f"mishit({n})",   mishit, n, inner_loops=10)

    for n in ns:
        runner.bench_time_func(f"pop({n})", pop, n)

    for n in ns:
        runner.bench_time_func(f"remove_and_add({n})", pop, n)
