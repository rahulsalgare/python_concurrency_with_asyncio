import asyncio


async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


async def add_one(number: int) -> int:
    print(number + 1)


async def hello_world_message() -> str:
    await delay(1)
    print('Hello World!')


async def main() -> None:
    await hello_world_message()
    await add_one(1)


asyncio.run(main())
