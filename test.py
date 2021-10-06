import asyncio

from socketio import AsyncClient
from socketio.exceptions import ConnectionError

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
    await client.emit("generate_points", data={"quantity": 100}, callback=lambda: done.set_result(True))
    client.on("disconnect", handler=lambda: done.set_exception(ConnectionError))
    await done


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([test()]))

