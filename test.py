import asyncio

from socketio import AsyncClient
from socketio.exceptions import ConnectionError
from matplotlib import pyplot as plt

client = AsyncClient()


@client.event
def new_number(data=None):
    print(f'New number! {data}')


@client.event
def new_point(data=None):
    print(f'New point! {data}')


async def test():
    await client.connect('http://localhost:8000')
    done = asyncio.Future()
    await client.emit("generate_points",
                      data={"quantity": 30, "sleep": 0},
                      callback=lambda: done.set_result(True))
    client.on("disconnect", handler=lambda: done.set_exception(ConnectionError))
    data = []
    client.on("new_point", handler=lambda point: data.append(point))
    await done
    plt.plot([point["x"] for point in data], [point["y"] for point in data])
    plt.show()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([test()]))

