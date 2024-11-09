import os

def get(path, connection):
    if os.path.isfile(path):
        with open(path, 'rb') as file:
            content = file.read()

        if path.endswith('.html'):
            content_type = 'text/html'
        elif path.endswith('.txt'):
            content_type = 'text/plain'
        elif path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            content_type = 'image/' + path.split('.')[-1]
        else:
            content_type = 'application/octet-stream'

        # Send HTTP response header and content
        response_header = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n'
        connection.sendall(response_header.encode('utf-8') + content)
    else:
        # File not found, send 404 response
        error_message = "<h1>404 Not Found</h1><p>The requested resource was not found on this server.</p>"
        response = f"HTTP/1.1 404 Not Found\r\nContent-Length: {len(error_message)}\r\n\r\n{error_message}"
        connection.send(response.encode('utf-8'))

def post(body, connection):
    print(f"POST data:\n{body}")
                
    # Respond with 200 OK and wait for file content in body
    response = 'HTTP/1.1 200 OK\r\n\r\nPOST request received'
    connection.send(response.encode('utf-8'))