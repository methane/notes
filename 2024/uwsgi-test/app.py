import os
import threading


def application(env, start_response):
    pid = os.getpid()
    tid = threading.get_ident()
    start_response('200 OK', [('Content-Type','text/html')])
    return [f"{pid} {tid}".encode()]
