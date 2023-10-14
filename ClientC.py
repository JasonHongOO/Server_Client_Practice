import sys, struct, time, json, signal,random
import socket
import threading

running = True
def signal_handler(sig, frame):
    print("接收到Ctrl+C信號，正在停止服務器...")
    global running
    running = False

    # 執行清理操作，例如關閉套接字和停止線程
    send_thread.join()
    receive_thread.join()

    client_socket.close()
    sys.exit(0)

def receive_messages(client_socket):
    while running == True:
        try :
            message_length_data = client_socket.recv(4)
            if not message_length_data: break

            message_length = struct.unpack('!I', message_length_data)[0]
            data = client_socket.recv(message_length)
            print(data.decode('utf-8'))
            received_data = json.loads(data.decode('utf-8'))
            print(f"\n來自 {received_data['Sender_Name']} 的消息: {received_data['Msg']}")
        except socket.timeout:
            print("等待訊息超時 => 休息一下")
            time.sleep(1)

def send_message(client_socket, message):
    message_json = json.dumps(message)
    message_length = len(message_json)
    client_socket.send(struct.pack('!I', message_length))  # 發送消息長度
    client_socket.send(message_json.encode('utf-8'))  # 發送消息內容

def send_messages(client_socket):
    while running == True:
        message = {}
        message["Receiver_Name"] = []
        message["Receiver_Name"].append("A")
        message["Receiver_Name"].append(input("請發送訊息對象："))
        message["Msg"] = input("請輸入要發送的消息：")
        send_message(client_socket, message)
        time.sleep(1)

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345

    signal.signal(signal.SIGINT, signal_handler)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.settimeout(5)

    client_name = "C"
    client_socket.send(client_name.encode('utf-8'))  # 發送用戶名給服務器

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    while running:
        pass