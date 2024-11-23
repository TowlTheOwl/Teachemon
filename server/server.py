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
        self.server.listen()
        print("Listening...")
        self.battle_queue = self.BattleQueue(self)
        threading.Thread(target=self.main).start()

    def main(self):
        threading.Thread(target=self.repeat_queue_check).start()
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
    
    def repeat_queue_check(self):
        while self.run:
            self.battle_queue.check_queue()
            time.sleep(3)
    
    def handle_client(self, c: socket.socket):
        c.send("Enter matching string: ".encode())
        # client will send back a matching string
        matching_string = c.recv(1024).decode()
        print("Received:", matching_string)
        if matching_string == "match":
            c.send("SEARCHING".encode())
            
            self.battle_queue.add_to_queue(c, matching_string)
        elif matching_string == "login":
            c.send("Send login info".encode())
            username, password = c.recv(1024).decode().split(",") # String in form "{username},{password}"
            found = str(self.find_login(username, password))
            c.send(found.encode())
        elif matching_string == "create login":
            # -1 if blank password, 0 if username taken
            c.send("Send login info".encode())
            username, password = c.recv(1024).decode().split(",")
            if len(password) < 1:
                c.send("0".encode())
            else:
                if self.create_login(username, password):
                    c.send("1".encode())
                else:
                    c.send("-1".encode())
        elif matching_string == "add card":
            c.send("Enter card num".encode())
            # should receive an int corresponding to user's new card
            username, card_num = c.recv(1024).decode().split(",")
            self.add_card(username, card_num)
            c.send("Success".encode())
        elif matching_string == "get cards":
            c.send("Req:username".encode())
            username = c.recv(1024).decode()
            c.send(self.find_card(username))
    
    def handle_match(self, c1: socket.socket, c2: socket.socket):
        match = self.BattleHandler(c1, c2)

    def find_login(self, username: str, password: str="") -> int:
        """
        parameters:
        username and password of the user

        return:
        -1: no matching username
        0: incorrect password
        1: match
        """
        with open("data.txt", "r") as file:
            data = file.readlines()
            for info in data:
                info = info.split(",")
                if info[0] == username:
                    if info[1] == password:
                            return 1
                    return 0
            return -1

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
            p1.send("MATCH".encode())
            p2.send("MATCH".encode())

    class BattleQueue:
        def __init__(self, server):
            self.queue : List[Tuple[socket.socket, str]] = []
            self.server = server
        
        def check_queue(self):
            for i in reversed(range(len(self.queue))):
                conn = self.queue[i][0]
                try:
                    conn.send("Checking Connection".encode())
                    data = conn.recv(1024)  # Receive data from the socket
                    if not data:
                        print("Connection closed by the client.")
                        conn.close()
                        self.queue.pop(i)
                        
                except ConnectionResetError:
                    print("Connection forcibly closed by the client.")
                    conn.close()
                    self.queue.pop(i)
                
                except ConnectionAbortedError:
                    print("Connection forcibly closed by the client.")
                    conn.close()
                    self.queue.pop(i)
                
        def add_to_queue(self, conn:socket.socket, match_string:str):
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
