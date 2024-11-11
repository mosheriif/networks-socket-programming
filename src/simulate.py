import time
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

def fetch_url(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    return end_time - start_time

def main():
    ip = socket.gethostbyname(socket.gethostname())
    port = 5050
    url = f"http://{ip}:{port}/index.html"
    num_requests_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    num_clients = 100
    response_times = []

    for num_requests in num_requests_list:
        with ThreadPoolExecutor(max_workers=num_clients) as executor:
            times = list(executor.map(fetch_url, [url] * num_requests))
        average_response_time = sum(times) / len(times)
        response_times.append(average_response_time)
        print(f"Number of requests: {num_requests}, Average response time: {average_response_time} seconds")

    plt.plot(num_requests_list, response_times, marker='o')
    plt.xlabel('Number of Requests')
    plt.ylabel('Average Response Time (seconds)')
    plt.title('Server Performance')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()