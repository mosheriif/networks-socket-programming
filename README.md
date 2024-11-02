
# Socket Programming Assignment

## Overview

This project is part of the (CSE334) Computer Networks course. The project contains the implementation of a simple web server and client application, and provides hands-on experience with UNIX socket programming, focusing on HTTP request handling, multi-threaded server architecture, and basic client-server communication in Python.

## Project Structure

The assignment has been divided into three main parts:
1. **Multi-threaded Web Server**
2. **HTTP Web Client**
3. **HTTP/1.1 Persistent Connections (Advanced)**

### 1. Multi-threaded Web Server

The web server accepts incoming client connections and handles HTTP `GET` and `POST` requests:
- **GET Requests**: Retrieve the requested file if available and return a `200 OK` response. If the file is not found, return `404 Not Found`.
- **POST Requests**: Acknowledge the request with an `OK` message and receive file data from the client.

#### Running the Server
```bash
python my_server.py <port_number>
```

### 2. HTTP Web Client

The web client reads and processes commands from an input file, handling both `GET` and `POST` commands:
- **GET Command**: Fetches a file from the server.
- **POST Command**: Sends a file to the server.

#### Running the Client
```bash
python my_client.py <server_ip> <port_number>
```
Note: The `<port_number>` is optional and defaults to port 80 if unspecified.

### 3. HTTP/1.1 Support

The server supports persistent connections and pipelining of requests, allowing reuse of a single connection for multiple requests. The connection timeout is dynamic based on the server’s workload.

## Bonus Features
- **Browser Compatibility**: The server can be tested using a real web browser.
- **Performance Evaluation**: Includes an analysis of server performance under varying client loads, with a chart illustrating the relationship between response time and the number of requests.

## Resources
- [Beej’s Guide to Network Programming](https://beej.us/guide/bgnet/)
- **Computer Networking: A Top-Down Approach, 8th Edition**
