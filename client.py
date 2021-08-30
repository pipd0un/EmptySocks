import socket
import tools.helper as helper
import threading

HEADER = 128
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!q"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

hp = helper.Helper(FORMAT)


def send(msg:str,sock:socket.socket):
    sock.send(hp.utf8len(msg))
    sock.send(msg.encode(FORMAT))

def getResponse(sock:socket.socket):
    while True:
        try:
            msg_len = int(sock.recv(HEADER).decode(FORMAT))
            if msg_len:
                msg = sock.recv(msg_len).decode(FORMAT)
                if msg == "!q":
                    print("\n[CLOSING]  Server is down")
                    break
                else:
                    print("Server: "+msg)
        except socket.error as err:
            print(f"[ERROR]  {err}")
            break

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    connexHandler = threading.Thread(target=getResponse, args=(client,),daemon=True)
    connexHandler.start()
    while True:
        try:
            msg = str(input("> "))
            send(msg,client)
            if msg == DISCONNECT_MESSAGE:
                connexHandler.join()
                break
        except socket.error as err:
            print(f"[ERROR]  {err}")
            connexHandler.join()
            break

if __name__ == "__main__":
    connect()
    input("> done")


