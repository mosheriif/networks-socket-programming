import socket
import sys
import time
import webbrowser

FORMAT = 'utf-8'
BUFFER_SIZE = 1024

def connect_to_server(commands, host, port):
    # Resolve the host name to an IP address
    host = socket.gethostbyname(host)
    address = (host, port)

    # Create a socket and connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)

    # Send the commands to the server
    for command in commands:
        send_request(client, command[0], command[1], host)
    # Close the socket connection
    client.close()

def send_request(client, command, file_path, host):
    if command == "client_get":
        # Send a GET request to the server
        request = f"GET /{file_path} HTTP/1.1\r\nHost: {host}\r\nConnection: keep-alive\r\n\r\n"
        client.send(request.encode(FORMAT))

        # Receive the response from the server
        response = client.recv(BUFFER_SIZE).decode(FORMAT)
        if "\r\n\r\n" in response:
            headers, body = response.split("\r\n\r\n", 1)
            print(headers)

            local_file_path = file_path.split('/')[-1]
            print(f"Saving response to {local_file_path}")
            # webbrowser.open(f'http://{host}:{port}/{local_file_path}')
        else:
            print("Invalid response received from the server.")
    elif command == "client_post":
        # Read the file content to be sent in the POST request
        with open(file_path, 'r') as file:
            body = file.read()

        # Send a POST request to the server
        request = f"POST /{file_path} HTTP/1.1\r\nHost: {host}\r\nContent-Length: {len(body)}\r\nConnection: keep-alive\r\n\r\n{body}"
        client.send(request.encode(FORMAT))

        # Receive and print the response from the server
        response = client.recv(BUFFER_SIZE).decode(FORMAT)
        print(response)

def main(command_file, host, port):
    commands = []
    with open(command_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 3:
                print(f"Invalid command: {line.strip()}")
                continue
            # Append the command to the list of commands
            commands.append(parts[0:2])
    # Connect to the server with the commands
    connect_to_server(commands, host, port)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: ./my_client <server_ip> <port_number> <input_file>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port_number = int(sys.argv[2])
    input_file = sys.argv[3]
    main(input_file, server_ip, port_number)