import asyncio
from random import uniform
import socketio
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# create a Socket.IO server
sio = socketio.AsyncServer(engineio_logger=True, async_mode='asgi')


@sio.event
async def generate_numbers(sid, data=None):
    defaults = {"quantity": 10, "min": 1, "max": 6, "sleep": 0.5}
    data = {**defaults, **data} if type(data) is dict else defaults
    for number in range(data["quantity"]):
        await sio.emit("new_number", data=uniform(data["min"], data["max"]), to=sid)
        await asyncio.sleep(data["sleep"])


@sio.event
async def generate_points(sid, data=None):
    defaults = {"quantity": 11, "min_x": 0, "max_x": 10, "min_y": 1, "max_y": 6, "sleep": 0.5}
    data = {**defaults, **data} if type(data) is dict else defaults
    x = data["min_x"]
    dx = (data["max_x"] - data["min_x"]) / (data["quantity"] - 1)
    for i in range(data["quantity"]):
        await sio.emit("new_point", data={"x": x, "y": uniform(data["min_y"], data["max_y"])}, to=sid)
        await asyncio.sleep(data["sleep"])
        x += dx


# wrap with ASGI application
app = socketio.ASGIApp(sio, app)
