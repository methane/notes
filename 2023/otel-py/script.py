import sqlite3


def enable_ddtrace():
    from ddtrace import tracer, patch
    from ddtrace.internal.writer import LogWriter

    tracer.configure(writer=LogWriter(open("./ddtrace.out", "w", encoding="utf-8")))
    patch(sqlite3=True)


def enable_otel():
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource

    # Service name is required for most backends,
    # and although it's not necessary for console export,
    # it's good to set service name anyways.
    resource = Resource(attributes={SERVICE_NAME: "sqlite3-otel"})

    provider = TracerProvider(resource=resource)
    out = open("./otel.out", "w", encoding="utf-8")
    processor = BatchSpanProcessor(ConsoleSpanExporter(out=out))
    # processor = BatchSpanProcessor(ConsoleSpanExporter())  # to stdout
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor

    SQLite3Instrumentor().instrument(tracer_provider=provider)

    # tracer = trace.get_tracer("sqlite3-test")
    # with tracer.start_as_current_span("test()"):
    #    test()


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


enable_ddtrace()
enable_otel()

test()

# for _ in range(10000):
#    test()
