import socket

def create_message(username, message):
    usernamelen = len(username)
    return bytearray([usernamelen]) + username.encode('utf-8') + message.encode('utf-8')

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 9001)  # サーバーのアドレスとポート

    try:
        while True:
            username = input("Enter your username: ")
            message = input("Enter your message: ")
            data = create_message(username, message)
            client_socket.sendto(data, server_address)

            # レスポンスを受信
            data, _ = client_socket.recvfrom(4096)
            print("Received:", data.decode('utf-8'))

    except KeyboardInterrupt:
        print("Client exited.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
