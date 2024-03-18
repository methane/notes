from time import sleep

from anyio import CapacityLimiter
from anyio.lowlevel import RunVar
from fastapi import FastAPI, Depends

app = FastAPI()

def f1():
    return 42

@app.get("/")
def ping(f=Depends(f1)) -> str:
    print("start ping")
    sleep(5)
    print("finish ping")
    return "pong!"

@app.on_event("startup")
def startup():
    print("startup")
    RunVar("_default_thread_limiter").set(CapacityLimiter(1))
