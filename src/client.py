import socket
import sys
import webbrowser

# Default port and format settings
PORT = 5050
FORMAT = 'utf-8'
BUFFER_SIZE = 1024


def send_request(command, file_path, host, port=PORT):
    # Resolve the host name to an IP address
    host = socket.gethostbyname(host)
    address = (host, port)

    # Create a socket and connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)

    if command == "client_get":
        # Send a GET request to the server
        request = f"GET /{file_path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        client.send(request.encode(FORMAT))

        # Receive the response from the server
        response = client.recv(BUFFER_SIZE).decode(FORMAT)
        if "\r\n\r\n" in response:
            headers, body = response.split("\r\n\r\n", 1)
            print(headers)

            local_file_path = file_path.split('/')[-1]
            print(f"Saving response to {local_file_path}")
            webbrowser.open(f'http://{host}:{port}/{local_file_path}')
        else:
            print("Invalid response received from the server.")
    elif command == "client_post":
        # Read the file content to be sent in the POST request
        with open(file_path, 'r') as file:
            body = file.read()

        # Send a POST request to the server
        request = f"POST /{file_path} HTTP/1.1\r\nHost: {host}\r\nContent-Length: {len(body)}\r\n\r\n{body}"
        client.send(request.encode(FORMAT))

        # Receive and print the response from the server
        response = client.recv(BUFFER_SIZE).decode(FORMAT)
        print(response)

    # Close the socket connection
    client.close()


def main(command_file):
    # Read commands from the input file
    with open(command_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 3:
                print(f"Invalid command: {line.strip()}")
                continue

            # Extract command, file path, host, and optional port
            command, file_path, host = parts[:3]
            port = int(parts[3]) if len(parts) == 4 else PORT

            # Send the request based on the command
            send_request(command, file_path, host, port)


if __name__ == "__main__":
    # Check if the input file is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python client.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)