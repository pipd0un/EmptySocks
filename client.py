import socket
import threading
import tools.helper as helper

hp = helper.Helper(helper._FORMAT)

class Client:
    def __init__(self,SERVER:str,PORT:int):
        self._CSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ADDR = (SERVER,PORT)
        self._PORT = PORT
        self._SERVER = SERVER
        self._RUN = False
        self._Threads = []
        self._shutReq = False

    def __loadThreads(self):
        recvTh = threading.Thread(target=self.__recvResponse,name="recvTh",daemon=True)
        sendTh = threading.Thread(target=self.__sendResponse,name="sendTh",daemon=False)

        self._Threads.append(recvTh)
        self._Threads.append(sendTh)

    def __runThreads(self):
        for t in self._Threads:
            t.start()
            
    def __send(self,cmd:str):
        self._CSOCK.send(hp.utf8len(cmd))
        self._CSOCK.send(cmd.encode(helper._FORMAT))

    def __recvResponse(self):
        while self._RUN:
            try:
                msg_len = self._CSOCK.recv(helper._HEADER).decode(helper._FORMAT)
                if msg_len:
                    msg = self._CSOCK.recv(int(msg_len)).decode(helper._FORMAT)
                    if msg == f"{helper._DISC}":
                        print("\n[CLOSING]  Server is down")
                        self.__send("!q")
                        self._shutReq = True
                    else:
                        print(f"Server: {msg}")
            except socket.error as err:
                print(f"[ERROR-1]  {err}")
                self._shutReq = True
                #break 

    def __sendResponse(self):
        while self._RUN:
            try:
                msg = str(input("> "))
                if not self._shutReq:
                    self.__send(msg)
                    if msg == helper._DISC:
                        print("[CLOSE]  DISCONNECTED")
                        self._shutReq = True
            except socket.error as err:
                print(f"[ERROR-2]  {err}")
                self._shutReq = True
                break

    def connect(self):
        self._RUN = True
        self._CSOCK.connect(self._ADDR)
        print(f"[CONNEXD] Server is listening on {self._SERVER}")
        self.__loadThreads()
        print("[READY]  Client is ready for processes ! ")
        self.__runThreads()

if __name__ == "__main__":
    cli = Client(socket.gethostbyname(socket.gethostname()),5050)
    cli.connect()
        