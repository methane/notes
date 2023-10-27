import sys
import sqlite3


def enable_otel(sample_rate: float = 1.0):
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
    from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor

    # 1/100 sampling
    sampler = TraceIdRatioBased(sample_rate)

    # Service name is required for most backends,
    # and although it's not necessary for console export,
    # it's good to set service name anyways.
    resource = Resource(attributes={SERVICE_NAME: "sqlite3-otel"})

    provider = TracerProvider(resource=resource, sampler=sampler)
    out = open("./otel-sampled.out", "w", encoding="utf-8")
    # processor = BatchSpanProcessor(ConsoleSpanExporter())  # to stdout
    processor = BatchSpanProcessor(ConsoleSpanExporter(out=out, formatter=lambda s: s.to_json(indent=2)))
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


# enable_ddtrace()
rate = float(sys.argv[1])
print(f"sampling {rate=}")
enable_otel(rate)

# test()

for _ in range(10000):
   test()
