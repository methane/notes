import pyperf
import random
import operator


def xor_bytes_list(a, b):
    return bytes([(aa ^ bb) for (aa, bb) in zip(a, b, strict=True)])


def xor_bytes_generator(a, b):
    return bytes((aa ^ bb) for (aa, bb) in zip(a, b, strict=True))


def xor_bytes_operator(a, b):
    return bytes(map(operator.xor, a, b))


def xor_bytes_via_int(a, b):
    if len(a) != len(b):
        raise ValueError(f"a and b must have same length; {len(a)=} {len(b)=}")
    aa = int.from_bytes(a, "big")
    bb = int.from_bytes(b, "big")
    return (aa ^ bb).to_bytes(len(a), "big")


xa = bytes([*range(256)])
xb = random.randbytes(256)

expected = xor_bytes_list(xa, xb)
assert expected == xor_bytes_generator(xa, xb)
assert expected == xor_bytes_operator(xa, xb)
assert expected == xor_bytes_via_int(xa, xb)

runner = pyperf.Runner()
runner.bench_func("list", xor_bytes_list, xa, xb)
runner.bench_func("generator", xor_bytes_generator, xa, xb)
runner.bench_func("operator", xor_bytes_operator, xa, xb)
runner.bench_func("int", xor_bytes_via_int, xa, xb)
