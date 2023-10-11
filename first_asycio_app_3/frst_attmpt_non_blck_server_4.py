"""
In this  we will get BlockingIOerror because our server socket has
no connection yet and therefore no data to process
"""

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
# server_address = ('192.168.1.9', 8000)
server_socket.bind(server_address)
server_socket.listen()

# mark the socket as nonblocking
# If the socket has data ready for processing, then we will get data
# returned as we would with a blocking socket. If not, the socket will instantly let us know it
# does not have any data ready, and we are free to move on to execute other code.
server_socket.setblocking(False)

connections = []

try:
    while True:
        conn, client_address = server_socket.accept()

        # mark the client socket as non blocking
        conn.setblocking(False)

        print(f'I got connection from {client_address}')
        connections.append(conn)

        for connection in connections:
            buffer = b''

            while buffer[-2:] != b'\r\n':

                # this blocks other connections to execute till it recieves the data from the current connection
                data = connection.recv(2)
                if not data:
                    break
                else:
                    buffer = buffer + data

            print('data is', buffer)
            connection.send(buffer)

finally:
    server_socket.close()
