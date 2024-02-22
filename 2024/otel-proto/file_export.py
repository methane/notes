# $ rye run python file_export.py

# まずはメモリ上にトレースを生成する。
# https://opentelemetry.io/docs/languages/python/instrumentation/#acquire-tracer

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)


provider = TracerProvider()
exporter = InMemorySpanExporter()
processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)
# ConsoleSpanExporterは1spanずつprintするので、バッチ化するメリットがない.
provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

def do_work():
    with tracer.start_as_current_span("span-name") as span:
        # do some work that 'span' will track
        print("doing some work...")
        # When the 'with' block goes out of scope, 'span' is closed for you


for _ in range(10):
    do_work()

processor.force_flush()
spans = exporter.get_finished_spans()


# OpenTelemetryのFileExporter (experimental) フォーマットで出力してみる.
# https://opentelemetry.io/docs/specs/otel/protocol/file-exporter/

from opentelemetry.exporter.otlp.proto.common.trace_encoder import (
    encode_spans,
)
from google.protobuf.json_format import MessageToJson

# FileExporter format は json lines (jsonl) なので、改行を入れないで
# エンコードする必要がある.
json_spans = MessageToJson(encode_spans(spans), indent=None)
print(json_spans)
