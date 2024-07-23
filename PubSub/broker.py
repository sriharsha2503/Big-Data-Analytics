import socket
import threading

subscribers = []

def handle_subscriber(conn, addr):
    print(f"Subscriber connected: {addr}")
    subscribers.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
    finally:
        subscribers.remove(conn)
        conn.close()
        print(f"Subscriber disconnected: {addr}")

def handle_publisher(conn, addr):
    print(f"Publisher connected: {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Broker: Received message: {message}")
            for subscriber in subscribers:
                subscriber.sendall(data)

def accept_connections(sock, handler):
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handler, args=(conn, addr)).start()

def broker(publisher_port, subscriber_port):
    pub_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sub_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        pub_sock.bind(('localhost', publisher_port))
        sub_sock.bind(('localhost', subscriber_port))
        pub_sock.listen()
        sub_sock.listen()
        print("Broker: Listening for publishers on port", publisher_port)
        print("Broker: Listening for subscribers on port", subscriber_port)

        threading.Thread(target=accept_connections, args=(pub_sock, handle_publisher)).start()
        threading.Thread(target=accept_connections, args=(sub_sock, handle_subscriber)).start()
        
        # Keep the main thread running to maintain the socket bindings
        while True:
            pass

    finally:
        pub_sock.close()
        sub_sock.close()

if __name__ == "__main__":
    broker(5555, 5556)

