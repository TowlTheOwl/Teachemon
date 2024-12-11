import socket
import threading
import time
from typing import List, Tuple, Dict


class Server:
    def __init__(self, IP, port):
        self.run = True

        with open("data.txt", "r") as file:
            self.total_cards = int(file.readline().strip("\n").split(",")[2]) # number of total cards

        self.ip = IP
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        
        self.logged_in_clients: Dict[str, socket.socket] = {}
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
        closer.close()
        for user in self.logged_in_clients:
            self.logged_in_clients[user].close()
        self.server.close()
        quit()
    
    # def check_clients(self):
    #     print(self.logged_in_clients)
    #     for username, conn in self.logged_in_clients.items():
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
    #             del self.logged_in_clients[key]
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
                            self.logged_in_clients[user] = c
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
                                self.logged_in_clients[user] = c
                            else:
                                to_send = 2
                        c.send(f"ss{to_send}".encode())
                        print(f"sent: ss{to_send}")

                    elif msg == "exit queue":
                        print("Attempting to remove from queue")
                        if user is not None: # check user is logged in
                            if self.battle_queue.remove_from_queue(c):
                                print(f"Removed {c.getsockname()} from queue")
                            else:
                                print(f"Could not remove {c.getsockname()} from queue")

                    elif msg == "get cards":
                        if user is None:
                            print("NOT LOGGED IN BUT GET CARDS CALLED????")
                        else:
                            data = self.find_card(user)
                            if data != "":
                                c.send(f"sc{','.join([str(e) for e in self.card_to_list(data)])}".encode())
                                print(f"Sent sc{','.join([str(e) for e in self.card_to_list(data)])}")
                            else:
                                print("USERNAME NOT FOUND WHEN SEARCHING FOR CARDS")
                    
                    elif msg[0] == "a":
                        self.add_card(user, msg[1:])
                            
            
            except Exception as e:
                print(e)
                if isinstance(e, ConnectionResetError) or isinstance(e, ConnectionAbortedError) or isinstance(e, OSError):
                    print("Connection forcibly closed by the client.")
                    c.close()
                    client_connected = False
                    if user is not None:
                        del self.logged_in_clients[user]
                else:
                    raise e
        
    def handle_match(self, c1: socket.socket, c2: socket.socket):
        match = BattleHandler(self, c1, c2)

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
                        if username in self.logged_in_clients:
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

    def replace_line(self, file_name, line_num, text):
        lines = open(file_name, 'r').readlines()
        lines[line_num] = text
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()

    def card_to_list(self, c):
        return [i+1 for i in range(len(c)) if c[i] == "1"]

    def list_to_card(self, l):
        return "".join(["1" if i+1 in l else "0" for i in range(self.total_cards)])

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
            for index in range(len(data)):
                user, pswd, card = data[index].split(",")
                if user == username:
                    card_list = self.card_to_list(card)
                    if card_num not in card_list:
                        card_list.append(int(card_num))
                    self.replace_line("data.txt", index, f"{user},{pswd},{self.list_to_card(card_list)}\n")
                    print(f"Replaced Line {index} with {user},{pswd},{self.list_to_card(card_list)}")
                    return

class BattleHandler:
    def __init__(self, server:Server, p1:socket.socket, p2:socket.socket):
        self.game_in_progress = True
        self.server = server
        self.p1 = p1
        self.p2 = p2
        p1.send("smMATCH".encode())
        p2.send("smMATCH".encode())

        threading.Thread(target=self.check_connected).start()
    
    def check_connected(self):
        while self.server.run and self.game_in_progress:
            if self.p1 not in self.server.logged_in_clients.values():
                self.p2.send("smDC".encode())
                self.game_in_progress = False
            if self.p2 not in self.server.logged_in_clients.values():
                self.p1.send("smDC".encode())
                self.game_in_progress = False

class BattleQueue:
    def __init__(self, server:Server):
        self.queue : List[Tuple[socket.socket, str]] = []
        self.server = server
    
    def check_queue(self):
        for i in reversed(range(len(self.queue))):
            conn = self.queue[i][0]
            if conn not in self.server.logged_in_clients.values():
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
    
    def remove_from_queue(self, conn: socket.socket):
        """
        return True if connection was in queue and was removed
        return False if connection was not in queue; not removed
        """
        for i in range(len(self.queue)):
            if self.queue[i][0] == conn:
                self.queue.pop(i)
                return True
        return False

if __name__ == "__main__":
    # Server's IPv4 address, port
    serverIP = "localhost"
    port = 5555

    serverObj = Server(serverIP, port)
    input()
    serverObj.close()
