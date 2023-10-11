"""
Our first client will work fine and will echo messages back as we’d expect, but our second client won’t
get anything echoed back to it. This is due to the default blocking behavior of sockets.
The methods accept and recv block until they receive data
"""

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# server_address = ('127.0.0.1', 8000)
server_address = ('192.168.1.9', 8000)
server_socket.bind(server_address)
server_socket.listen()

connections = []

try:
    while True:
        conn, client_address = server_socket.accept()
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
            connection.sendall(buffer)

finally:
    server_socket.close()
