import socket
import threading
import time

# Server's IPv4 address, port
serverIP = "localhost"
port = 5555
# See client.py for AF_INET and SOCK_STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serverIP, port))

server.listen()
print("Listening...")

# list of client in match queue
queue = []

def find_login(username: str, password: str="") -> int:
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

def create_login(username: str, password: str) -> bool:
    """
    return:
    false if username is taken & login not created
    true if login was created
    """
    if (find_login(username) == 0):
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

def card_to_list(c):
    return [bool(int(e)) for e in list(c)]

def list_to_card(l):
    return "".join([str(int(e)) for e in l])

def find_card(username):
    with open("data.txt", "r+") as file:
        data = file.readlines()
        for info in data:
            user, _, card = info.split(",")
            if user == username:
                return card
    return ""

def add_card(username:str, card_num:str):
    with open("data.txt", "r+") as file:
        data = file.readlines()
        for info in data:
            user, pswd, card = info.split(",")
            if user == username:
                card_list = card_to_list(card)
                card_list[card_num] = True
                replace_line("data.txt", data.index(info), f"{user},{pswd},{list_to_card(card_list)}")
                return

def handle_match(c1: socket.socket, c2: socket.socket):
    c1.send("MATCH".encode())
    c2.send("MATCH".encode())
    c1_name = c1.recv(1024).decode()

def handle_client(c: socket.socket):
    c.send("Enter matching string: ".encode())
    # client will send back a matching string
    matching_string = c.recv(1024).decode()
    print("Received:", matching_string)
    if matching_string == "match":
        # for now, matching string is just match - later can be modified for different gamemodes

        # finds another player in the queue, starts a game
        # if not found, add player to the queue
        found_match = False
        for i in range(len(queue)):
            if queue[i][1] == matching_string:
                threading.Thread(target=handle_match, args=(c, queue[i][0])).start()
                found_match = True
                del queue[i]
        
        if not found_match:
            queue.append((c, matching_string))
    elif matching_string == "login":
        c.send("Send login info".encode())
        username, password = c.recv(1024).decode().split(",") # String in form "{username},{password}"
        found = str(find_login(username, password))
        c.send(found.encode())
    elif matching_string == "create login":
        # -1 if blank password, 0 if username taken
        c.send("Send login info".encode())
        username, password = c.recv(1024).decode().split(",")
        if len(password) < 1:
            c.send("0".encode())
        else:
            if create_login(username, password):
                c.send("1".encode())
            else:
                c.send("-1".encode())
    elif matching_string == "add card":
        c.send("Enter card num".encode())
        # should receive an int corresponding to user's new card
        username, card_num = c.recv(1024).decode().split(",")
        add_card(username, card_num)
        c.send("Success".encode())
    elif matching_string == "get cards":
        c.send("Req:username".encode())
        username = c.recv(1024).decode()
        c.send(find_card(username))

def main(server:socket.socket):
    while True:
        client, addr = server.accept()
        print("Connected to:", addr)
        # runs the function handle_client, which will handle a single client.
        # threading is needed to we can listen to multiple clients, while another is being handled.
        threading.Thread(target=handle_client, args=(client,)).start()
        
threading.Thread(target=main, args=(server,)).start()
input()
server.close()