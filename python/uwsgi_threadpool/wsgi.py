from concurrent.futures import ThreadPoolExecutor
import time


executor = ThreadPoolExecutor(max_workers=16)


def background(i):
    print(f"starting {i}")
    time.sleep(5)
    print(f"ending {i}")


counter = 0


def application(environ, start_response):
    global counter
    start_response("200 OK", [("Content-type", "text/plain; charset=utf-8")])
    count = counter
    counter += 1
    executor.submit(background, count)
    return [b"Hello, world"]
