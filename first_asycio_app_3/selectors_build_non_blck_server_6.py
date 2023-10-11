"""
Using the event notification system of operating system to listen to the events on sockets

python has library 'selector' to utilize event notification system
"""
import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple

selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()

# register our socket on Selector for the read event
selector.register(server_socket, selectors.EVENT_READ)

print(dir(server_socket))

while True:
    # Create a selector that will timeout after 1 second
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

    # when timeout happens
    if len(events) == 0:
        print('no events, wating a bit more')

    for event, _ in events:
        # get the socket on which the event happened
        event_socket = event.fileobj

        # If the event happened on the server socket, that means someone attempting to connect, initiate handshake
        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print('got a connection from', connection)

            # register the client's socket with selector for the read event
            # TODO: shouldn't it be EVENT_WRITE, since client will 'write' on his own socket to send it to server ?
            selector.register(connection, selectors.EVENT_READ)

        else:
            data = event_socket.recv(1024)
            print(f'data recieved from {event_socket.getpeername()}: {data}')
            event_socket.send(data)
