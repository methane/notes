# otel-proto

PythonでOpenTelemetryのプロトコルを触ってみる。
protobuf や protobuf json へのエンコード、デコードはできるが、
そこから ReadableSpan 等にするには otel のライブラリが用意している
encode系の関数の逆変換をする関数を自前で実装しないといけないことがわかった。

エンコード速度は、pb2がjsonの2倍以上速く、エンコード後のサイズは1/3以下になった。

トレースには同じ情報が大量に含まれるので、Batch化しておくと圧縮がかなり効く。
圧縮後のサイズはjsonもpb2も大きく変わらない。
