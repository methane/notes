from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

fd = open("foo.txt", "w")
tracer_provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter(out=fd))
tracer_provider.add_span_processor(processor)
