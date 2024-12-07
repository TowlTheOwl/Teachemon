import socket
import threading
import time
from typing import List, Tuple


class Server:
    def __init__(self, IP, port):
        self.run = True

        self.ip = IP
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        
        self.connected_clients = {}
        self.keys_to_remove = []
        self.server.listen()
        print("Listening...")
        self.battle_queue = BattleQueue(self)
        threading.Thread(target=self.main).start()

    def main(self):
        # threading.Thread(target=self.repeat_queue_check).start()
        while self.run:
            client, addr = self.server.accept()
            print("Connected to:", addr)
            # runs the function handle_client, which will handle a single client.
            # threading is needed to we can listen to multiple clients, while another is being handled.
            
            threading.Thread(target=self.handle_client, args=(client,)).start()
    
    def close(self):
        self.run = False
        closer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        closer.connect((self.ip, self.port))
        closer.recv(1024)
        closer.send(" ".encode())
        self.server.close()
        quit()
    
    # def check_clients(self):
    #     print(self.connected_clients)
    #     for username, conn in self.connected_clients.items():
    #         try:
    #             conn.send("cc".encode())
            
    #         except Exception as e:
    #             if isinstance(e, ConnectionResetError) or isinstance(e, ConnectionAbortedError) or isinstance(e, OSError):
    #                 print("Connection forcibly closed by the client.")
    #                 conn.close()
    #                 self.keys_to_remove.append(username)
        
    #     print(self.keys_to_remove)
    #     # remove disconnected clients
    #     if len(self.keys_to_remove) != 0:
    #         to_remove = self.keys_to_remove.copy()
    #         for key in to_remove:
    #             del self.connected_clients[key]
    #         self.keys_to_remove = [keys for keys in self.keys_to_remove if keys not in to_remove]
    
    # def repeat_queue_check(self):
    #     while self.run:
    #         self.check_clients()
    #         time.sleep(3)
    
    def handle_client(self, c: socket.socket):
        """
        Requesting Info
        send "rusername,password,etc"
        Sending Info
        send "sinfo"
        """
        client_connected = True
        user = None
        while self.run and client_connected:
            try:
                data = c.recv(1024)
                if not data:
                    print("Connection closed by the client.")
                    c.close()
                    self.keys_to_remove.append(username)
                    client_connected = False
                else:
                    msg = data.decode()
                    print("Received:", msg)

                    if msg == "match":
                        c.send("smSEARCHING".encode())
                        
                        if user is not None:
                            self.battle_queue.add_to_queue(c, msg)
                        else:
                            raise Exception("Searching for match without logging in")
                    
                    elif msg == "login":
                        c.send("rusername,password".encode())
                        username, password = c.recv(1024).decode().split(",") # String in form "{username},{password}"
                        found = str(self.find_login(username, password))
                        if found == "1":
                            user = username
                            self.connected_clients[user] = c
                        c.send(f"sl{found}".encode())
                        print(f"sent: sl{found}")

                    elif msg == "signup":
                        # 0 if blank password, 2 if username taken
                        c.send("rusername,password".encode())
                        username, password = c.recv(1024).decode().split(",")
                        if len(password) < 1:
                            to_send = 0
                        else:
                            if self.create_login(username, password):
                                to_send = 1
                                user = username
                                self.connected_clients[user] = c
                            else:
                                to_send = 2
                        c.send(f"ss{to_send}".encode())
                        print(f"sent: ss{to_send}")

                    elif msg == "add card":
                        c.send("Enter card num".encode())
                        # should receive an int corresponding to user's new card
                        username, card_num = c.recv(1024).decode().split(",")
                        self.add_card(username, card_num)
                        c.send("Success".encode())

                    elif msg == "get cards":
                        c.send("Req:username".encode())
                        username = c.recv(1024).decode()
                        c.send(self.find_card(username))
            
            except Exception as e:
                print(e)
                if isinstance(e, ConnectionResetError) or isinstance(e, ConnectionAbortedError) or isinstance(e, OSError):
                    print("Connection forcibly closed by the client.")
                    c.close()
                    client_connected = False
                    if user is not None:
                        del self.connected_clients[user]
                else:
                    raise e
        
    def handle_match(self, c1: socket.socket, c2: socket.socket):
        match = BattleHandler(c1, c2)

    def find_login(self, username: str, password: str="") -> int:
        """
        parameters:
        username and password of the user

        return:
        3: no matching username
        0: incorrect password
        1: match
        2: already logged in
        """
        with open("data.txt", "r") as file:
            data = file.readlines()
            for info in data:
                info = info.split(",")
                if info[0] == username:
                    if info[1] == password:
                        if username in self.connected_clients:
                            return 2
                        return 1
                    return 0
            return 3

    def create_login(self, username: str, password: str) -> bool:
        """
        return:
        false if username is taken & login not created
        true if login was created
        """
        if (self.find_login(username) == 0):
            return False
        with open("data.txt", "a") as file:
            file.write(f"\n{username},{password}," + "0"*59)
        return True

    def replace_line(file_name, line_num, text):
        lines = open(file_name, 'r').readlines()
        lines[line_num] = text
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()

    def card_to_list(self, c):
        return [bool(int(e)) for e in list(c)]

    def list_to_card(self, l):
        return "".join([str(int(e)) for e in l])

    def find_card(self, username):
        with open("data.txt", "r+") as file:
            data = file.readlines()
            for info in data:
                user, _, card = info.split(",")
                if user == username:
                    return card
        return ""

    def add_card(self, username:str, card_num:str):
        with open("data.txt", "r+") as file:
            data = file.readlines()
            for info in data:
                user, pswd, card = info.split(",")
                if user == username:
                    card_list = self.card_to_list(card)
                    card_list[card_num] = True
                    self.replace_line("data.txt", data.index(info), f"{user},{pswd},{self.list_to_card(card_list)}")
                    return

class BattleHandler:
    def __init__(self, p1:socket.socket, p2:socket.socket):
        self.p1 = p1
        self.p2 = p2
        p1.send("smMATCH".encode())
        p2.send("smMATCH".encode())

class BattleQueue:
    def __init__(self, server:Server):
        self.queue : List[Tuple[socket.socket, str]] = []
        self.server = server
    
    def check_queue(self):
        for i in reversed(range(len(self.queue))):
            conn = self.queue[i][0]
            if conn not in self.server.connected_clients.values():
                self.queue.pop(i)
            
    def add_to_queue(self, conn:socket.socket, match_string:str):
        self.check_queue()
        print(self.queue)
        for i in range(len(self.queue)):
            if self.queue[i][1] == match_string:
                threading.Thread(target=self.server.handle_match, args=(conn, self.queue[i][0])).start()
                self.queue.pop(i)
                return
        self.queue.append((conn, match_string))

if __name__ == "__main__":
    # Server's IPv4 address, port
    serverIP = "localhost"
    port = 5555

    serverObj = Server(serverIP, port)
    input()
    serverObj.close()
