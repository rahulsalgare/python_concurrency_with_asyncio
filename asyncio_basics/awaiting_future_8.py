import asyncio
from asyncio import Future


def make_request():
    future = Future()

    # Create a task to asynchronously set the value of the future.
    asyncio.create_task(set_future_value(future))
    return future


async def set_future_value(future):
    # Wait 1 second before setting the value of the future.
    await asyncio.sleep(1)
    future.set_result(42)


async def main():
    future = make_request()
    print('is future done', future.done())

    # Pause main until the future’s value is set.
    value = await future

    print('is future done', future.done())
    print('value', value)


asyncio.run(main())
