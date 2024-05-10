import random
from tornado.util import _websocket_mask_python
import itertools
import operator

try:
    from tornado.speedups import websocket_mask
except ImportError:
    websocket_mask = False
import pyperf


def websocket_mask_int(mask: bytes, data: bytes) -> bytes:
    assert len(mask) == 4
    mask = bytearray(mask)
    mask *= (len(data) + 3) // 4
    del mask[len(data) :]
    assert len(mask) == len(data)
    return (int.from_bytes(mask, "big") ^ int.from_bytes(data, "big")).to_bytes(
        len(data), "big"
    )


def mask_itertools(mask: bytes, data: bytes) -> bytes:
    return bytes(map(operator.xor, data, itertools.cycle(mask)))


mask = random.randbytes(4)
data = random.randbytes(100)

for i in range(15):
    if websocket_mask:
        assert _websocket_mask_python(mask, data) == websocket_mask(mask, data)
    assert websocket_mask_int(mask, data) == _websocket_mask_python(mask, data)
    assert mask_itertools(mask, data) == _websocket_mask_python(mask, data)


runner = pyperf.Runner()
runner.bench_func("_websocket_mask_python", _websocket_mask_python, mask, data)
if websocket_mask:
    runner.bench_func("tornado.speedups", websocket_mask, mask, data)
runner.bench_func("websocket_mask_int", websocket_mask_int, mask, data)
runner.bench_func("mask_itertools", mask_itertools, mask, data)
