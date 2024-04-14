import socket
import time

def parse_data(data):
    usernamelen = data[0]
    username = data[1:usernamelen+1].decode('utf-8')
    message = data[usernamelen+1:].decode('utf-8')
    return username, message

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = '0.0.0.0'
server_port = 9001
server_socket.bind((server_address, server_port))
clients = {}

# クライアントの最後の活動時刻を追跡
last_active = {}

print(f"Starting up on {server_address} port {server_port}")

while True:
    try:
        data, address = server_socket.recvfrom(4096)
        current_time = time.time()
        
        if address not in clients:
            clients[address] = True
            last_active[address] = current_time
            print(f"New client connected: {address}")
        
        # メッセージとユーザー名を解析
        username, message = parse_data(data)
        print(f"Received from {username}: {message}")
        
        # 他のクライアントにメッセージを送信
        for client_address in list(clients.keys()):
            if client_address != address:
                server_socket.sendto(data, client_address)

        # 更新クライアントの最後の活動時間
        last_active[address] = current_time

        # 30秒以上活動がないクライアントを切断
        inactive_clients = [addr for addr, last_time in last_active.items() if current_time - last_time > 30]
        for addr in inactive_clients:
            del clients[addr]
            del last_active[addr]
            print(f"Client timed out and disconnected: {addr}")

    except Exception as e:
        print(f"Error: {str(e)}")
