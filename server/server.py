import socket
import sys
import threading
import time
from typing import List, Tuple, Dict
import json
from player import Player
import csv
import random

class Server:
    def __init__(self, IP, port):
        self.run = True
        print("Initializing...\r")

        print("Retrieving user data.")
        with open("data/data.txt", "r") as file:
            self.total_cards = int(file.readline().strip("\n").split(",")[2]) # number of total cards
        print(f"Number of total cards: {self.total_cards}.")

        print("Retrieving Teachemon data.")
        with open("data/TeachemonData - Teachemon.csv", 'r') as file:
            self.teachemon_data = []
            csvfile = csv.DictReader(file) # reads data file for teachemon
            for row in csvfile:
                self.teachemon_data.append(row)
        print("Complete.\r")
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
        sys.exit()
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
        player = None
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
                            self.battle_queue.add_to_queue(player, msg)
                        else:
                            raise Exception("Searching for match without logging in")
                    
                    elif msg == "login":
                        c.send("rusername,password".encode())
                        username, password = c.recv(1024).decode().split(",") # String in form "{username},{password}"
                        found = str(self.find_login(username, password))
                        if found == "1":
                            user = username
                            self.logged_in_clients[user] = c
                            player = Player(c, user)
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
                    
                    elif msg[0] == "x":
                        # it is a match message, relay onto server
                        player.queue.append(msg[1:])

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
        
    def handle_match(self, p1, p2):
        BattleHandler(self, p1, p2, self.teachemon_data)

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
        with open("data/data.txt", "r") as file:
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
        with open("data/data.txt", "a") as file:
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
        with open("data/data.txt", "r+") as file:
            data = file.readlines()
            for info in data:
                user, _, card = info.split(",")
                if user == username:
                    return card
        return ""

    def add_card(self, username:str, card_num:str):
        with open("data/data.txt", "r+") as file:
            data = file.readlines()
            for index in range(len(data)):
                user, pswd, card = data[index].split(",")
                if user == username:
                    card_list = self.card_to_list(card)
                    if card_num not in card_list:
                        card_list.append(int(card_num))
                    self.replace_line("data/data.txt", index, f"{user},{pswd},{self.list_to_card(card_list)}\n")
                    print(f"Replaced Line {index} with {user},{pswd},{self.list_to_card(card_list)}")
                    return

class BattleHandler:
    def __init__(self, server:Server, p1:Player, p2:Player, teachemon_data:list):
        self.game_in_progress = True
        self.teachemon_data = teachemon_data
        self.server = server
        self.p1 = p1
        self.p2 = p2
        self.c1 = p1.conn
        self.c2 = p2.conn
        self.p1_msg = p1.queue
        self.p2_msg = p2.queue

        self.c1.send("rownedcards".encode())
        self.c2.send("rownedcards".encode())

        while (len(self.p1_msg) == 0 or len(self.p2_msg) == 0):
            pass
        self.p1_cards = json.loads(self.p1_msg[0])
        self.p2_cards = json.loads(self.p2_msg[0])
        self.p1_hps = [100, 100, 100, 100]
        self.p2_hps = [100, 100, 100, 100]
        self.all_hps = (self.p1_hps, self.p2_hps)
        self.p1_msg.clear()
        self.p2_msg.clear()

        print(f"Player 1 cards: {self.p1_cards}")
        print(f"Player 2 cards: {self.p2_cards}")
        self.curr_cards = [0, 0]


        self.c1.send("smMATCH1".encode())
        self.c2.send("smMATCH2".encode())

        self.send_info_to_both_players(f"smu{p1.username}'{p2.username}'{self.p1_cards}'{self.p2_cards}'{self.p1_hps}'{self.p2_hps}")

        threading.Thread(target=self.check_connected).start()
        self.wait_for_response("CONNECTED")
        time.sleep(3)



        # game loop begins
        while (self.game_in_progress and any(self.p1_hps) and any(self.p2_hps)):
            # check if current teachemon is dead
            dead = []
            if self.p1_hps[self.curr_cards[0]] == 0:
                # p1 playa ded
                dead.append(0)
            if self.p2_hps[self.curr_cards[1]] == 0:
                dead.append(1)
            if len(dead) != 0:
                print("Player Dead")
                self.send_info_to_both_players(f"smm1{json.dumps(dead)}'10")
                # let dead player swap
                self.wait_for_response_starts_with(dead, ("s",), ("n",), 10)
                p1_action = None
                if 0 in dead:
                    for i in range(len(self.p1_msg)):
                        if self.p1_msg[i][0] == "s":
                            p1_action = self.p1_msg[i]
                    self.p1_msg.clear()

                p2_action = None
                if 1 in dead:
                    for i in range(len(self.p2_msg)):
                        if self.p2_msg[i][0] == "s":
                            p2_action = self.p2_msg[i]
                    self.p2_msg.clear()
                actions = [p1_action, p2_action]

                swaps = [None, None]
                for i in range(2):
                    if i in dead:
                        action = actions[i]
                        if action is not None and action[0] == "s":
                            self.curr_cards[i] = int(action[1])
                            swaps[i] = action
                        else:
                            alive = []
                            for j in range(len(self.p1_hps)):
                                if self.all_hps[i][j] > 0:
                                    alive.append(j)
                            choice = random.choice(alive)
                            self.curr_cards[i] = choice
                            swaps[i] = f"s{choice}"
                
                self.send_info_to_both_players(f"smm2{json.dumps(swaps)}")
                self.wait_for_response("anicomp")
            else:
                print("No Players Dead")

            curr_cards_data = (self.teachemon_data[self.p1_cards[self.curr_cards[0]]], self.teachemon_data[self.p2_cards[self.curr_cards[1]]])
            # give 20 seconds to choose, tell users to pick a move
            self.send_info_to_both_players("smgmove10")
            self.wait_for_response_starts_with((0, 1), ("m", "i", "s"), ("n",), 12)# 2 second buffer to receive messages
            # receive messages
            possible_moves = ["m", "i", "s"]
            p1_action = None
            if self.p1_msg[0][0] in possible_moves:
                p1_action = self.p1_msg[0]
            self.p1_msg.clear()

            p2_action = None
            if self.p2_msg[0][0] in possible_moves:
                p2_action = self.p2_msg[0]
            self.p2_msg.clear()

            actions = (p1_action, p2_action)
            # handle actions
            """
            m = Move
            i = Item Use
            s = Swap
            """
            abilities = [None, None]
            items = [None, None]
            first_to_animate = -1
            for i in range(2):
                action = actions[i]
                if action is not None:
                    action_type = action[0]
                    move_num = action[1]
                    if action_type == "m":
                        abilities[i] = int(move_num)
                    elif action_type == "i":
                        items[i] = int(move_num)
                    elif action_type == "s":
                        self.curr_cards[i] = int(move_num)  # swap is immediate - swap before any abilities cast
                        first_to_animate = i
            
            # handle user actions
            # items are used immediately
            ########BLAVKLJBLKJKDJBLBJDK########
            
            # cast abilities
            first_to_cast = 0
            num_cast = 0
            if abilities[0] is not None and abilities[1] is not None:  # if both players cast
                first_to_cast = 0
                num_cast = 2
                user1speed = int(curr_cards_data[0][f"Move {abilities[0]+1} Speed"])
                user2speed = int(curr_cards_data[1][f"Move {abilities[1]+1} Speed"])
                if user1speed > user2speed:
                    first_to_cast = 1
                elif user1speed == user2speed:
                    # coin toss
                    first_to_cast = random.randint(0,1)
                
            elif abilities[1] is not None: # only user 2 casted
                first_to_cast = 1
                num_cast = 1
            elif abilities[0] is not None: # only user 1 casted
                first_to_cast = 0
                num_cast = 1
            if first_to_animate == -1:
                first_to_animate = first_to_cast
            
            i = 0
            print(f"Number of Casts: {num_cast}")
            print(abilities)

            print(f"P1 Queue: {self.p1_msg}")
            print(f"P2 Queue: {self.p2_msg}")
            while num_cast > 0:
                target_idx = (first_to_cast + i) % 2
                opp_idx = (first_to_cast + i + 1) % 2
                if self.all_hps[target_idx][self.curr_cards[target_idx]] != 0:
                    self.cast_ability(curr_cards_data[target_idx], int(abilities[target_idx]), self.curr_cards[opp_idx], self.all_hps[opp_idx])
                i += 1
                num_cast -= 1

            self.send_info_to_both_players(f"smm0{p1_action}'{p2_action}'{first_to_animate}'{self.p1_hps}'{self.p2_hps}") # send moves
            """
            user action 1, user action 2, first to cast, hp1, hp2
            """
            # wait for users to finish animation
            completed = self.wait_for_response("anicomp", 7) # client sends "xanicomp" (ANImation COMPlete)
            if not all(completed):
                if not completed[0]:
                    self.c2.send("smDC".encode())
                elif not completed[1]:
                    self.c1.send("smDC".encode())
        
        winner = -1
        # declare winner
        if (any(self.p1_hps)):
            winner = 0
        else:
            winner = 1
        self.send_info_to_both_players(f"smd{winner}")
    
    def cast_ability(self, card_data:dict, ability_idx:int, opp_curr_card: int, opp_hps:list):
        # cast the selected ability, calculate damage
        damage = int(card_data[f"Move {ability_idx + 1} Damage"])
        opp_hps[opp_curr_card] -= damage
        if opp_hps[opp_curr_card] < 0:
            opp_hps[opp_curr_card] = 0
        
    def send_info_to_both_players(self, message:str):
        self.c1.send(message.encode())
        self.c2.send(message.encode())
        print(f"Sent message to both players: {message}")
    
    def wait_for_response(self, response_key:str, max_time:int=10, delete:bool=True):
        responses = [0, 0]
        start_time = time.time()
        while not all(responses) and time.time() - start_time < max_time:
            if response_key in self.p1_msg:
                responses[0] = 1
                if delete:
                    self.p1_msg.remove(response_key)
            if response_key in self.p2_msg:
                responses[1] = 1
                if delete:
                    self.p2_msg.remove(response_key)
        
        return responses
        
    
    def wait_for_response_starts_with(self, targets:list, response_key:tuple, catch_key:tuple, max_time:int):
        responses = [1, 1]
        start_time = time.time()
        for target in targets:
            responses[target] = 0
        while not all(responses) and time.time() - start_time < max_time:
            if 0 in targets:
                for msg in self.p1_msg:
                    if msg[0] in response_key or msg[0] in catch_key:
                        responses[0] = 1
            if 1 in targets:
                for msg in self.p2_msg:
                    if msg[0] in response_key or msg[0] in catch_key:
                        responses[1] = 1
            time.sleep(1)
            

    def check_connected(self):
        while self.server.run and self.game_in_progress:
            if (self.c1 not in self.server.logged_in_clients.values()) or ("L" in self.p1_msg):
                self.c2.send("smDC".encode())
                self.game_in_progress = False
            if (self.c2 not in self.server.logged_in_clients.values()) or ("L" in self.p2_msg):
                self.c1.send("smDC".encode())
                self.game_in_progress = False

class BattleQueue:
    def __init__(self, server:Server):
        self.queue : List[Tuple[Player, str]] = []
        self.server = server
    
    def check_queue(self):
        for i in reversed(range(len(self.queue))):
            conn = self.queue[i][0].conn
            if conn not in self.server.logged_in_clients.values():
                self.queue.pop(i)
            
    def add_to_queue(self, player:Player, match_string:str):
        self.check_queue()
        print(self.queue)
        for i in range(len(self.queue)):
            if self.queue[i][1] == match_string:
                threading.Thread(target=self.server.handle_match, args=(player, self.queue[i][0])).start()
                self.queue.pop(i)
                return
        self.queue.append((player, match_string))
    
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
