import asyncio


async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


async def main():
    long_task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(asyncio.shield(long_task), 3)
        print('try result', result)
    except asyncio.exceptions.TimeoutError:
        print('Task not finished, it will finish soon')
        result = await long_task
        print('exc result', result)


asyncio.run(main())
