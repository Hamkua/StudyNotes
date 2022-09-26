from socket import *
from tkinter import *
from _thread import *
from time import *
from collections import deque
from tkinter import simpledialog

def recieve_from_server(client_socket):
    # global entry
    while True:
        msg = client_socket.recv(1024)

        if len(msg) != 0:
            recieved_message = msg.decode('utf-8')
            print("기입창 내용 : ", entry.get())

            # 내가 전달한 메세지가 아니라면
            if entry.get() != recieved_message.split(" : ")[1]:
                if recieved_message == "check message":
                    pass
            # 내가 메시지를 전달했음이 확인되었으므로, entry의 문자열을 삭제한다.
            else:
                entry.delete(0, END)

            # 전체 메시지 갯수가 10개 이하인 경우
            if len(labels) < 10:
                label = Label(frame,text=msg,width=10, height=20)
                label.place(x=10, y=5 + (30 * len(labels) - 1), width=180, height=20)
                labels.append(label)

            # 메시지 갯수가 10개 이상인 경우, 가장 상단의 메시지는 없애고 새로운 메시지를 아래에 추가한다
            else:
                old_label = labels.popleft()
                print("old_label 삭제")
                print(labels)
                new_label = Label(frame,text=msg,width=10, height=20)
                
                labels.append(new_label)
                for i in range(len(labels)):
                    labels[i].place(x=10, y=5 + (30 * (i)), width=180, height=20)


                    
        else:
            pass
            # label.insert(0, msg.decode('utf-8'))


clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8080))



root = Tk()    # 메인 창인 Tk 객체의 인스턴스 생성 
root.title("20171064 함영권 - 채팅 프로그램")
root.geometry("200x340")
root.resizable(False, False)

frame = Frame(root, background='gray')
frame.place(x = 0, y = 0, width=200, height=300)

nickname = simpledialog.askstring(title="닉네임 입력", prompt="닉네임을 입력하세요")
clientSock.send(nickname.encode('utf-8'))

# 가장 앞단의 요소들을 차례로 삭제할 것이므로 큐를 구현한 deque 사용
labels = deque()

entry = Entry(root)
entry.place(x=0, y=300,width=150, height=30)


enter_btn = Button(root, text="Enter", command=lambda: clientSock.send(entry.get().encode('utf-8')))
enter_btn.place(x=150, y=300, width=50, height=30)


start_new_thread(recieve_from_server, (clientSock,))

root.mainloop()
