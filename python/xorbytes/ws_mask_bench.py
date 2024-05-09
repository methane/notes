import random
from tornado.util import _websocket_mask_python
from tornado.speedups import websocket_mask
import pyperf


def websocket_mask_int(mask: bytes, data: bytes) -> bytes:
    assert len(mask) == 4
    mask = bytearray(mask)
    mask *= (len(data) + 3) // 4
    del mask[len(data) :]
    assert len(mask) == len(data)
    return (int.from_bytes(mask) ^ int.from_bytes(data)).to_bytes(len(data))


mask = random.randbytes(4)
data = random.randbytes(100)

for i in range(15):
    assert _websocket_mask_python(mask, data) == websocket_mask(mask, data)
    assert websocket_mask_int(mask, data) == websocket_mask(mask, data)


runner = pyperf.Runner()
runner.bench_func("_websocket_mask_python", _websocket_mask_python, mask, data)
runner.bench_func("tornado.speedups", websocket_mask, mask, data)
runner.bench_func("websocket_mask_int", websocket_mask_int, mask, data)
