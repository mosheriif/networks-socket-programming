import socket
import threading
from request_commands import *

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())     # gets the ip address instead of being hardcoded
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def parser(request):
    request_line = request.splitlines()[0]
    command, path, _ = request_line.split()
    return command, path

def handle_client(connection, address, thread_count):
    try:
        print(f"[NEW CONNECTION] {address} connected.")
        connected = True
        while connected:
            timeout = 10 / (thread_count + 1)
            connection.settimeout(timeout)

            message = connection.recv(1024).decode(FORMAT) # (blocking line) waits to receive a message
            if not message:
                break

            headers, body = message.split("\r\n\r\n", 1)
            print(f"Received request:\n{headers}")

            command, path = parser(headers)
            path = path.lstrip('/')

            if command == "GET":
                get(path, connection)
            elif command == "POST":
                post(body, connection)
            connection.send(b'\r\n')
            print(f"[{address}] {message}")

    except socket.timeout:
        pass
    finally:
        connection.close()

def start():
    active = []
    server.listen()

    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()   # (blocking line) waits for a new connection to the server, storing the ip address and port in "address", and stores information in "connection" so we can send data back and forth
        thread_count = len(active)
        thread = threading.Thread(target=handle_client, args=(connection, address, thread_count))
        active.append(thread)

        active = [t for t in active if t.is_alive()]
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

start()