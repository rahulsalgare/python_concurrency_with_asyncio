import asyncio
from asyncio import CancelledError


async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


async def main():
    long_task = asyncio.create_task(delay(10))
    seconds_passed = 0

    while not long_task.done():
        print('Task not finished, checking again in second')
        await asyncio.sleep(1)
        seconds_passed += 1
        if seconds_passed == 5:
            long_task.cancel()

    try:
        await long_task

    except CancelledError:
        print("Task was cancelled")


asyncio.run(main())
