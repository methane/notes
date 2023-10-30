import sys
import sqlite3


def enable_otel(sample_rate: float = 1.0):
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio
    from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor

    # ParentBasedTraceIdRatio: parentのsampleに従う。rootはratioでsamplingする。
    # リバースプロキシ等上流でサンプリングしていて、それに完全に従いたい場合は ParentBased(ALWAYS_OFF)
    # 上流でサンプリングをしてないので幾らかをドロップしたい場合は ParentBased() を使って、
    #   root と remote_parent_sampled に ParentBasedTraceIdRatio を指定する。
    sampler = ParentBasedTraceIdRatio(sample_rate)

    # Service name is required for most backends,
    # and although it's not necessary for console export,
    # it's good to set service name anyways.
    resource = Resource(attributes={SERVICE_NAME: "sqlite3-otel"})

    provider = TracerProvider(resource=resource, sampler=sampler)
    processor = BatchSpanProcessor(ConsoleSpanExporter(formatter=lambda s: s.to_json(indent=2)))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    SQLite3Instrumentor().instrument()


from opentelemetry import trace
tracer = trace.get_tracer("otel-sampling")


@tracer.start_as_current_span("test")
def test():
    # https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE lang(name, first_appeared)")

    # This is the named style used with executemany():
    data = (
        {"name": "C", "year": 1972},
        {"name": "Fortran", "year": 1957},
        {"name": "Python", "year": 1991},
        {"name": "Go", "year": 2009},
    )
    cur.executemany("INSERT INTO lang VALUES(:name, :year)", data)

    for _ in range(5):
        for y in [1972, 1957, 1991, 2009]:
            # This is the qmark style used in a SELECT query:
            params = (y,)
            cur.execute("SELECT * FROM lang WHERE first_appeared = ?", params)
            cur.fetchall()


rate = float(sys.argv[1])
N = int(sys.argv[2]) if len(sys.argv) > 2 else 10_000
# N = 100_000 # for profiling

print(f"{N = }, sampling {rate = }", file=sys.stderr)
enable_otel(rate)

for _ in range(N):
   test()
