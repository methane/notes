import sys
import os
import io
import traceback
import json
import pathlib
import minitraceback
import sqlalchemy

import sub

try:
    import py.code
except ImportError:
    py = None


def f1():
    try:
        return f2(10)
    except:
        return f2(10)


def f2(n):
    if n:
        f2(n - 1)
    else:
        return sub.c(f3)


def f3():
    return pathlib.Path("./foo").relative_to(pathlib.Path("./bar"))


_DEFAULT_MAXFILENAMELEN = 30


def format_tb_short(tb, *, maxfilenamelen=None, limit=None) -> list[str]:
    cwd = os.getcwd()
    if maxfilenamelen is None:
        maxfilenamelen = _DEFAULT_MAXFILENAMELEN
    lines = ["Traceback (most recent call first):\n"]

    tbs = [*traceback.walk_tb(tb)]
    tbs.reverse()
    if limit is not None:
        del tbs[limit:]

    for f, lineno in tbs:
        c = f.f_code
        filename = c.co_filename
        try:
            filename = str(pathlib.Path(filename).relative_to(cwd, walk_up=False))
        except ValueError:
            pass
        filename = filename[-maxfilenamelen:]
        lines.append(f"  {filename}:{lineno} {c.co_name}\n")

    return lines


def format_exception_short(exc: BaseException, *, maxfilenamelen=None, limit=None) -> str:
    lines = traceback.format_exception_only(exc)
    lines += format_tb_short(
        exc.__traceback__, maxfilenamelen=maxfilenamelen, limit=limit
    )
    return "".join(lines)


def main():
    try:
        engine = sqlalchemy.create_engine("sqlite:////bin/hoge.db")
        conn = engine.connect()
        #f1()
    except Exception as e:
        tb = e.__traceback__

        print("# stdlib traceback")
        s = "".join(traceback.format_exception(e, chain=True))
        print(s)

        if py:
            print("# py.code traceback")
            exc_info = py.code.ExceptionInfo()
            print(f"traceback:\n{exc_info.getrepr(showlocals=False, style='short')}")
            print()

        print("# minitrace")
        print("\n".join(minitraceback.format_exception(e)))

        print("\n# minitrace in json")
        frames = minitraceback.extract_tb(tb)
        print('"exception":', minitraceback.format_exception_only(e))
        print('"stacktrace":', json.dumps(minitraceback.format_frames(frames)))


main()
