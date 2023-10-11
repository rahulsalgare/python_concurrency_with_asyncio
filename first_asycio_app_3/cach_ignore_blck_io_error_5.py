"""
we get BlockingIOerror because our server socket has
no connection yet and therefore no data to process

to handle this, just catch the exception, ignore it, and keep looping until we
have data

problem with this code:
This approach works, but it comes at a cost. The first is code quality. Catching
exceptions any time we might not yet have data will quickly get verbose and is poten-
tially error-prone. The second is a resource issue. If you run this on a laptop, you may
notice your fan starts to sound louder after a few seconds. This application will always
be using nearly 100% of our CPU’s processing power. This is because we
are constantly looping and getting exceptions as fast as we can inside our application,
leading to a workload that is CPU heavy.

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
        try:
            conn, client_address = server_socket.accept()

            # mark the client socket as non blocking
            conn.setblocking(False)

            print(f'I got connection from {client_address}')
            connections.append(conn)

        except BlockingIOError:
            pass

        for connection in connections:
            try:
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

            except BlockingIOError:
                pass

finally:
    server_socket.close()
