import socket
import threading
import tools.helper as helper

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!q"
ACTIVES = {}
RUN = False

hp = helper.Helper(FORMAT)


def sendCmd(cmd, cli):
    cli.send(hp.utf8len(cmd))
    cli.send(cmd.encode(FORMAT))

def sendAll(cmd,all:list):
    for addr in all:
        sendCmd(cmd,addr)

def recv(conn, addr):
    print(f"\n[NEW CONNECTION] {addr[1]} connected.")
    while True:
        print("Client bridge")
        try:
            msg_len = conn.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg = conn.recv(int((msg_len))).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    print(f"\n[{addr[1]}] DISCONNECTED")
                    break
                else:
                    print(f"\n[{addr[1]}] {msg}")
        except socket.error as err:
            print(f"[ERROR]  {err}")
            break
    del ACTIVES[conn]
    conn.close()

def serverManager(isrun:bool):
    while True:
        print("ServerMan Running")
        try:
            cmd = input("cmd: > ")
            if cmd:
                if cmd == DISCONNECT_MESSAGE:
                    print("[CLOSING]  server will be closed ...")
                    # send message about server is down
                    sendAll(cmd,ACTIVES)
                    isrun = False
                    break
                elif cmd.split()[0] == "!c":
                    listClients()
                elif cmd.split()[0] == "sel":
                    listClients()
                    clct = 1
                    cmd = input(": > ")
                    for client in ACTIVES:
                        if int(cmd) == clct:
                            cmdToCli = str(input("send: "))
                            sendCmd(cmdToCli, client)
                        clct += 1
        except socket.error as err:
            print(f"[ERROR]  {err}")
            break

def listClients():
    ct = 1
    if len(ACTIVES) == 0:
        print("No Online Clients")
    else:
        print("-- ACTIVE CLIENTS --\n")
        for cl in ACTIVES:
            print(f"[{ct}]  {ACTIVES[cl][1]}")
            ct += 1
        print("\n-------------------- ")

def connexManager(sock:socket.socket,onlines:list,isrun:bool):
    while isrun:
        print("ConnexMan running...")
        conn, addr = sock.accept()
        onlines[conn] = addr
        recv(conn,addr,isrun)


def run(isrun:bool,onlines:list):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[STARTING] server is starting...")

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    isrun = True
    serverHandler = threading.Thread(target=serverManager,args=(isrun,), daemon=False)
    serverHandler.start()
    
    print("[HANDLING] server is able to commands")

    # connexHandler = threading.Thread(target=connexManager, args=(server,onlines,isrun),daemon=False)
    # connexHandler.start()

    while True:
        try:
            if not serverHandler.is_alive():
                print(f"\nhandler status: {serverHandler.is_alive()}")
                serverHandler.join()
                break
            else:
                print("\n[WAITING]  Server is waiting")
                
            conn, addr = server.accept()
            ACTIVES[conn] = addr

            clientHandler = threading.Thread(target=recv, args=(conn, addr), daemon=True)
            clientHandler.start()

            print(f"[ACTIVE CONNECTIONS]  {len(ACTIVES)}")
        except socket.error as msg:
            print("Error: " + msg)
            print("[ERROR]  server will be closed ...")
            break

if __name__ == "__main__":
    run(RUN,ACTIVES)
    input("> done")
