"""
Exercise: run a task until future is set
"""
import asyncio
from asyncio import Future


async def run_till_future_set(future: Future):
    while not future.done():
        await asyncio.sleep(1)
        print('its not over yet, I must not give up')

    print(future.result())


async def set_future_value(future: Future):
    await asyncio.sleep(8)
    future.set_result('Its done, Mission Successful')


async def main():
    future = Future()
    task_1 = asyncio.create_task(run_till_future_set(future))
    task_2 = asyncio.create_task(set_future_value(future))

    await task_1
    await task_2


asyncio.run(main())
