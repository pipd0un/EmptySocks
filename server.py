import socket
import tools.helper as helper
import threading
import time

hp = helper.Helper(helper._FORMAT)

class Server:
  
    def __init__(self,SERVER:str,PORT:int):
        
        self._PORT = PORT
        self._SERVER = SERVER
        self._ADDR = (SERVER,PORT)
        self._SSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._RUN = False
        self._ACTIVES = {}
        self._Threads = []
        self._shutReq = False

    def __send(self,cmd:str,ct:int):
        print("[ ! ]  Send Response triggered !")
        conn =1
        for sock in self._ACTIVES:
            if ct == conn:
                print(f"[SOCKET_NAME]  {conn}")
                sock.send(hp.utf8len(cmd))
                sock.send(cmd.encode(helper._FORMAT))
                print("[SENT]  Message has sent ")
                break
            conn+=1

    def __sendAll(self,cmd:str):
        for online in self._ACTIVES:
            online.send(hp.utf8len(cmd)),
            online.send(cmd.encode(helper._FORMAT))
            
    def __listClients(self):
        ct = 1
        print("-- ACTIVE CLIENTS --\n")
        for cl in self._ACTIVES:
            print(f"[{ct}]  {self._ACTIVES[cl][1]}")
            ct += 1
        print("\n-------------------- ")
        return len(self._ACTIVES)

    def __close_server(self):
        while True:
            if self._shutReq:
                print("[ ! ]  All clients warned. ")
                self.__sendAll(helper._DISC)
                time.sleep(2)
                for cli in self._ACTIVES:
                    cli.close()
                self._ACTIVES.clear()
                if not self._ACTIVES:
                    print("\n[ALL KILLED]")
                    self._shutReq = False
                #break

    def __connexMan(self):
        while self._RUN:
            try:
                conn, addr = self._SSOCK.accept()
                self._ACTIVES[conn] = addr
                print(f"\n[NEW CONNECTION] {addr[1]} connected.")
            except socket.error as err:
                print(f"[ERROR-1]  {err}")
                print("[CLOSING]")

            clientHandler = threading.Thread(target=self.__clientBridge__,args=(conn,addr),daemon=True)
            clientHandler.start()

    def __clientBridge__(self,conn:socket.socket,addr):
        
        while not self._shutReq:
            try:
                msg_len = conn.recv(helper._HEADER).decode(helper._FORMAT)
                if msg_len:
                    msg = conn.recv(int((msg_len))).decode(helper._FORMAT)
                    if msg == helper._DISC:
                        print(f"\n[{addr[1]}] DISCONNECTED")
                        conn.close()
                        del self._ACTIVES[conn]
                        break
                    else:
                        print(f"\n[{addr[1]}] {msg}")
            except socket.error as err:
                print(f"[ERROR-2]  {err}")
                break
        
        

    def __sendResponse(self):
        while self._RUN:
            try:
                cmd = input("cmd: > ")
                if cmd:
                    if cmd == helper._DISC:
                        print("[CLOSING]  server will be closed ...")
                        self._shutReq = True
                        time.sleep(2)
                    elif cmd.split()[0] == "!c":
                        self.__listClients()
                    elif cmd.split()[0] == "!a":
                        cmd = input("send: ")
                        self.__sendAll(cmd)
                    elif cmd.split()[0] == "sel":
                        if self.__listClients():
                            ct = int(input(": > "))
                            cmd = input("send: ")
                            self.__send(cmd,ct)
                        else:
                            print("\n[ ! ]  No Online Client Exist")
            except socket.error as err:
                print(f"[ERROR-3]  {err}")
                self._shutReq = True
                break

    def run(self):
        self._SSOCK.bind(self._ADDR)
        print("[STARTING] server is starting...")
        self._SSOCK.listen()
        print(f"[LISTENING] Server is listening on {self._SERVER}")
        self._RUN = True
        sendTh = threading.Thread(target=self.__sendResponse,daemon=False)
        sendTh.start()
        print("[READY] server is able to commands")
        connexTh = threading.Thread(target=self.__connexMan,daemon=True)
        connexTh.start()
        
        threading.Thread(target=self.__close_server,daemon=False).start()

if __name__ == "__main__":

    s = Server(socket.gethostbyname(socket.gethostname()),5050)
    s.run()
    #input("Done")
