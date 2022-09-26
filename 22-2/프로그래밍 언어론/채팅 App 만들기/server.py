
from socket import *
from time import sleep
from multiprocessing import Process
from _thread import *

# def coroutin():
#     global server_socket
#     print(server_socket)
#     connected_socket, addr = server_socket.accept()
#     user_dict[addr] = connected_socket
#     print(str(addr),'에서 접속이 확인되었습니다.')

# class Server:
#     serverSocket = socket(AF_INET, SOCK_STREAM)    # 서버의 소켓 생성 AF_INET = IPv4 의미
#     user_dict = dict()
    

#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, "_instance"):         
#             cls._instance = super().__new__(cls)
            
#         return cls

#     def __init__(self):
#         cls = type(self)
#         if not hasattr(cls, "_init"):
#             # print("adwnlkanlwdanldwanldwalndwanldwanlkdwanlndklwandlawk")
#             cls.serverSocket.bind(("127.0.0.1", 8080)) 
#             cls.serverSocket.listen()
#             cls._init = True


# def connect_to_client(server_socket):
#     while True:
#         # print(self.serverSocket)
#         print("wadnbnnwaldnwla")
            
#         client_socket, addr = server_socket.accept()
#         nickname = client_socket.recv(1024).decode('utf-8')
#         print(nickname,'님이 접속하였습니다.')



class User:
    def __init__(self, addr, name):
        self.addr = addr
        self.name = name


def recieve_from_client(sock):
    while True:
        
        msg = sock.recv(1024)
        # print(msg.decode('utf-8'))
        
        if len(msg) != 0:
            name = user_dict[sock].name
            print(name, '으로부터 받은 데이터 : ', msg.decode('utf-8'))
        else:
            msg = "check message".encode('utf-8')

        send_to_client(name, msg)
        sleep(1)
        
def send_to_client(nickname, message):
    # print("메시지 보낸다")
    print(nickname)
    print(type(nickname))
    print(message)
    print(type(message))
    message = nickname + " : " + message.decode('utf-8')
    client_sockets = user_dict.copy().keys()
    print(client_sockets)
    for client_socket in client_sockets:
        
        # print(user_dict[client_socket], "에게 보낼 예정")
        # client_socket.send(message.decode('utf-8'))
        try:
            # print(user_dict[client_socket].name, "한테 보냄")
            client_socket.send(message.encode('utf-8'))

        except Exception as e:
            print(e)
            if client_socket in user_dict:
                del user_dict[client_socket]


server_socket = socket(AF_INET, SOCK_STREAM)    # 서버의 소켓 생성 AF_INET = IPv4 의미
server_socket.bind(("", 8080)) 
server_socket.listen()

user_dict = dict()

while True:

    connected_socket, addr = server_socket.accept()    # accept() 가 실행될때까지 대기하게 됨

    print(connected_socket, addr)
    print()
    if connected_socket not in user_dict:
        nickname = connected_socket.recv(1024).decode('utf-8')
        user_dict[connected_socket] = User(addr, nickname)
        print(str(addr),'에서 접속이 확인되었습니다.', nickname)
    else:
        nickname = user_dict[connected_socket]

# 서버 측 프로세스를 두개 이상 생성할 수 없어, 멀티 프로세싱을 사용하지 않고 멀티 스레딩을 사용합니다
# p = Process(target=recieve_from_client, args=(connected_socket,))
# p.start()
    start_new_thread(recieve_from_client, (connected_socket,))
    




    


