import asyncio


async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


async def main():
    long_task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(long_task, timeout=5)
        print('result', result)
    except asyncio.exceptions.TimeoutError:
        print('Got timeout, was task cancelled', long_task.cancelled())


asyncio.run(main())
