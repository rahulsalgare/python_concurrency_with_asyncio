import logging
import asyncio, signal
import socket
from asyncio import AbstractEventLoop

echo_tasks = []


class GracefulShutdown(SystemExit):
    pass


def shutdown():
    raise GracefulShutdown()


async def echo(connection, loop):
    # Loop forever waiting for data from a client connection
    try:
        while data := await loop.sock_recv(connection, 1024):
            print('got the data', data)
            if data == b'boom\r\n':
                raise Exception("Unexpected Network Error")
            await loop.sock_sendall(connection, data)
    except Exception as e:
        logging.exception(e)

    finally:
        connection.close()


async def listen_for_connections(server_socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print('got connection from ', connection)
        # Because we need to handle multiple connections at the same time, creating a task for each
        # connection to read and write data makes sense. On every connection we get, we’ll cre-
        # ate a task to both read data from and write data to that connection.
        echo_task = asyncio.create_task(echo(connection, loop))
        echo_tasks.append(echo_task)


async def main():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)

    await listen_for_connections(server_socket, asyncio.get_event_loop())


async def close_echo_tasks(echo_tasks):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            # Timout error
            pass


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())
except GracefulShutdown:
    loop.run_until_complete(close_echo_tasks(echo_tasks))
