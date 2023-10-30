import sys
import sqlite3


def enable_otel(sample_rate:float = 1.0):
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio

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


from opentelemetry import trace
tracer = trace.get_tracer("otel-event-sampling")


@tracer.start_as_current_span("test")
def test():
    # デコレータではなくwith文を使えばspanは取得できるが、引数で引き回すのは非現実的なのでAPIで取得する。
    current_span = trace.get_current_span()

    # https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries
    con = sqlite3.connect(":memory:")
    # NOTE: sqlite3はcon.exuecute()を実装しているが、ddtraceはこれに対応しているものの
    # otelはこれに対応していない。con.cursor()してcur.execute()を使うべき。
    cur = con.cursor()
    cur.execute("CREATE TABLE lang(name, first_appeared)")
    current_span.add_event("created long table")

    # This is the named style used with executemany():
    data = (
        {"name": "C", "year": 1972},
        {"name": "Fortran", "year": 1957},
        {"name": "Python", "year": 1991},
        {"name": "Go", "year": 2009},
    )
    cur.executemany("INSERT INTO lang VALUES(:name, :year)", data)
    current_span.add_event("finished batch insert into long table")

    for _ in range(5):
        for y in [1972, 1957, 1991, 2009]:
            # This is the qmark style used in a SELECT query:
            params = (y,)
            cur.execute("SELECT * FROM lang WHERE first_appeared = ?", params)
            rows = cur.fetchall()
            current_span.add_event(f"selected {len(rows)} rows")


rate = float(sys.argv[1])
N = int(sys.argv[2]) if len(sys.argv) > 2 else 10_000
# N = 100_000 # for profiling

print(f"{N = }, sampling {rate = }", file=sys.stderr)
enable_otel(rate)

for _ in range(N):
   test()
