import pyperf
import random


def xor_bytes_list(a, b):
    return bytes([(aa ^ bb) for (aa, bb) in zip(a, b, strict=True)])


def xor_bytes_generator(a, b):
    return bytes((aa ^ bb) for (aa, bb) in zip(a, b, strict=True))


def xor_bytes_via_int(a, b):
    if len(a) != len(b):
        return ValueError(f"a and b must have same length; {len(a)=} {len(b)=}")
    aa = int.from_bytes(a)
    bb = int.from_bytes(b)
    return (aa ^ bb).to_bytes(len(a))


xa = bytes([*range(256)])
xb = random.randbytes(256)

assert (
    xor_bytes_list(xa, xb) == xor_bytes_generator(xa, xb) == xor_bytes_via_int(xa, xb)
)

runner = pyperf.Runner()
runner.bench_func("list", xor_bytes_list, xa, xb)
runner.bench_func("generator", xor_bytes_generator, xa, xb)
runner.bench_func("int", xor_bytes_via_int, xa, xb)
