import logging
import asyncio
import socket
from asyncio import AbstractEventLoop


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
        asyncio.create_task(echo(connection, loop))


async def main():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    await listen_for_connections(server_socket, asyncio.get_event_loop())


asyncio.run(main())
