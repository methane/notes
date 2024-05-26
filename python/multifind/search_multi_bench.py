import pyperf


def oneliner1(p):
    subs = ('\\', '/')
    i = min((i for i in map(lambda x: p.find(x), subs) if i != -1), default=-1)
    return i


def oneliner2(p):
    subs = ('\\', '/')
    i = min([i for i in map(p.find, subs) if i != -1], default=-1)
    return i


def oneliner3(p):
    subs = ('\\', '/')
    i = min([i for s in subs if (i := p.find(s)) != -1], default=-1)
    return i


def test(f):
    assert f("/\\") == 0
    assert f("x/\\") == 1
    assert f("x\\/") == 1
    assert f("xx\\/") == 2
    assert f("x"*1000) == -1
    assert f("") == -1
    assert f("x"*1000+'/') == 1000


test(oneliner1)
test(oneliner2)
test(oneliner3)


runner = pyperf.Runner()
runner.bench_func('oneliner1', oneliner1, "x"*10000)
runner.bench_func('oneliner2', oneliner2, "x"*10000)
runner.bench_func('oneliner3', oneliner3, "x"*10000)
