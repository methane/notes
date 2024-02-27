# $ rye run python file_export.py

# まずはメモリ上にトレースを生成する。
# https://opentelemetry.io/docs/languages/python/instrumentation/#acquire-tracer

import sys

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
# provider.add_span_processor(
#     SimpleSpanProcessor(ConsoleSpanExporter())
# )

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

def do_work():
    with tracer.start_as_current_span("span-name") as span:
        # do some work that 'span' will track
        # print("doing some work...")
        pass
        # When the 'with' block goes out of scope, 'span' is closed for you

N = 10  # sizeとtimingを測るときは100を使った
for _ in range(N):
    do_work()

processor.force_flush()
spans = exporter.get_finished_spans()


# OpenTelemetryのFileExporter (experimental) フォーマットで出力してみる.
# https://opentelemetry.io/docs/specs/otel/protocol/file-exporter/

from opentelemetry.exporter.otlp.proto.common.trace_encoder import (
    encode_spans,
)
from opentelemetry.exporter.otlp.proto.common._internal.trace_encoder import (
    _encode_span
)
from google.protobuf import json_format

## spanをjsonにしてpb messageに戻すまで
# FileExporter format は json lines (jsonl) なので、改行を入れないで
# エンコードする必要がある.
# from opentelemetry.proto.trace.v1.trace_pb2 import Span as PB2SPan

# print(f"{spans[0]=}")
# encoded_span = _encode_span(spans[0])
# print(f"{encoded_span=}")
# json_span = json_format.MessageToJson(encoded_span, indent=None)
# print(f"{json_span=}")
# json_spans2 = json_format.Parse(json_span, PB2SPan())
# print(f"{json_spans2=}")

## spanをpb2, json化
encoded_spans = encode_spans(spans)
# File Exporrt format は json lines なのでindent=Noneで1行にする
json_spans = json_format.MessageToJson(encoded_spans, indent=None)
print("json output:", json_spans)


## compare timing
# import timeit
# timing_json = timeit.timeit(lambda: json_format.MessageToJson(encode_spans(spans)), number=1000)
# timing_pb2  = timeit.timeit(lambda: encode_spans(spans).SerializeToString(), number=1000)
# print(f"{timing_json=}, {timing_pb2=}")
## timing_json=1.6855301250470802, timing_pb2=0.6994002499850467

## compare size
# pb2_spans = encode_spans(spans).SerializeToString()
# print(f"{len(json_spans)=} vs {len(pb2_spans)=}")
## len(json_spans)=22202 vs len(pb2_spans)=6472

## FileExporter formatを取り込んで、別のExporterから出力してみる。

from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest as PB2ExportTraceServiceRequest,
)
request = json_format.Parse(json_spans, PB2ExportTraceServiceRequest())
from google.protobuf import text_format
print("protobuf(text):")
text_format.PrintMessage(request, sys.stdout))
