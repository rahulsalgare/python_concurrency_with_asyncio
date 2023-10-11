import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# server_address = ('127.0.0.1', 8000)
server_address = ('192.168.1.9', 8000)
server_socket.bind(server_address)
server_socket.listen()

try:
    connection, client_address = server_socket.accept()
    print(f'I got connection from {client_address}')

    buffer = b''

    # \r\n will be the end data when we press enter from telnet.
    # this server assumes that the client is telnet
    # tcp is just a stream of bytes. data format is more of an application layer protocol like HTTP
    while buffer[-2:] != b'\r\n':
        data = connection.recv(2)
        if not data:
            break
        else:
            print('Got data', data)
            buffer = buffer + data

    print('all the data is', buffer)

    connection.sendall(buffer)

finally:
    server_socket.close()
