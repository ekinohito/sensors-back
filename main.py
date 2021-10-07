import asyncio

from pydantic import ValidationError
import socketio
from fastapi import FastAPI

from model import NumbersQuery, PointsQuery

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# create a Socket.IO server
sio = socketio.AsyncServer(engineio_logger=True, async_mode='asgi', cors_allowed_origins='*')


@sio.event
async def generate_numbers(sid, data=None):
    try:
        data = NumbersQuery(**data) if type(data) is dict else NumbersQuery()
    except ValidationError:
        return
    y = (data.min_y + data.max_y) / 2
    for number in range(data.quantity):
        y = data.random(min_y=data.min_y, max_y=data.max_y, prev=y)
        await sio.emit("new_number", data=y, to=sid)
        await asyncio.sleep(data.sleep)


@sio.event
async def generate_points(sid, data=None):
    try:
        data = PointsQuery(**data) if type(data) is dict else PointsQuery()
    except ValidationError:
        return
    x = data.min_x
    dx = (data.max_x - data.min_x) / (data.quantity - 1)
    y = (data.min_y + data.max_y) / 2
    for i in range(data.quantity):
        y = data.random(min_y=data.min_y, max_y=data.max_y, prev=y)
        await sio.emit("new_point", data={"x": x, "y": y}, to=sid)
        await asyncio.sleep(data.sleep)
        x += dx


# wrap with ASGI application
app = socketio.ASGIApp(sio, app)
