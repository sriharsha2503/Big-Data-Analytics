import socket

def publisher(broker_host, broker_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((broker_host, broker_port))
        print("Publisher: Type your messages below. Type 'exit' to quit.")
        while True:
            message = input()
            if message.lower() == 'exit':
                break
            s.sendall(message.encode('utf-8'))
            print(f"Publisher: Sent message: {message}")

if __name__ == "__main__":
    publisher('localhost', 5555)

