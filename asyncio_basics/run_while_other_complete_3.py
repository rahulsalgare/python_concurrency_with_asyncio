import asyncio


async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


async def run_this_while_waiting():
    for i in range(2):
        await asyncio.sleep(1)
        print('doing this other task while waiting...')


async def main():
    import time
    s = time.time()

    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    third_delay = asyncio.create_task(delay(3))

    # If there were no tasks, then awaiting this coroutine function would have resulted in
    # executing the whole function first, before continuing the main function further
    await run_this_while_waiting()

    # await delay(3)
    # await delay(3)
    # await delay(3)

    await first_delay
    await second_delay
    await third_delay

    t = time.time() - s
    print('total execution time', t)


asyncio.run(main())
