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
async def connect(sid, _):
    async with sio.session(sid) as session:
        session["points_id"] = 0


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
    async with sio.session(sid) as session:
        session["points_id"] += 1
        points_id = session["points_id"]
    await sio.emit("new_graph", data={"id": points_id}, to=sid)
    for i in range(data.quantity):
        async with sio.session(sid) as session:
            if points_id != session["points_id"]:
                break
        y = data.random(min_y=data.min_y, max_y=data.max_y, prev=y)
        await sio.emit("new_point", data={"x": x, "y": y}, to=sid)
        await asyncio.sleep(data.sleep)
        x += dx


@sio.event
async def stop_generation(sid, _=None):
    async with sio.session(sid) as session:
        session["points_id"] += 1


# wrap with ASGI application
app = socketio.ASGIApp(sio, app)
