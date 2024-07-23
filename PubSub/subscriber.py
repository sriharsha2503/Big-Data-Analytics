import socket

def subscriber(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Subscriber: Connected to broker.")
        try:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Subscriber: Received message: {message}")
        finally:
            print("Subscriber: Disconnected from broker.")

if __name__ == "__main__":
    subscriber('localhost', 5556)

