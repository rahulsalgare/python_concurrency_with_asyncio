import asyncio


async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


async def without_task():
    import time

    s = time.time()

    sleep_for_three = await delay(3)
    sleep_again = await delay(3)
    sleep_more = await delay(3)

    total_time = time.time() - s
    print('total time without using create tasks is ', total_time)


async def main() -> None:
    """
    Using create_tasks
    :return:
    """
    import time

    s = time.time()

    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_more = asyncio.create_task(delay(3))

    await sleep_for_three
    await sleep_again
    await sleep_more

    total_time = time.time() - s
    print('total time using create tasks is ', total_time)

asyncio.run(without_task())
print('\n', '*' * 50, '\n')
asyncio.run(main())
