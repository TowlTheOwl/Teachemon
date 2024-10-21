import socket
import threading

# Server's IPv4 address, port
serverIP = "10.53.108.20"
port = 8005
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
        file.write(f"{username},{password},")
    return True

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def add_card(username:str, card_num:str):
    with open("data.txt", "r+") as file:
        data = file.readlines()
        for info in data:
            user, pswd, card = info.split(",")
            if user == username:
                if len(card) == 0:
                    replace_line("data.txt", data.index(info), info + f"{card_num}")
                else:
                    replace_line("data.txt", data.index(info), info + f":{card_num}")
                return

def handle_match(c1: socket.socket, c2: socket.socket):
    c1.send("MATCH".encode())
    c2.send("MATCH".encode())
    c1_name = c1.recv(1024).decode()

def handle_client(c: socket.socket):
    c.send("Enter matching string: ".encode())
    # client will send back a matching string
    matching_string = client.recv(1024).decode()
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
        username, password = client.recv(1024).decode().split(",") # String in form "{username},{password}"
        found = find_login(username, password)
        if found == 1:
            c.send("Logged In".encode())
        elif found == 0:
            c.send("Incorrect password".encode())
        else:
            c.send("Incorrect username".encode())
    elif matching_string == "create login":
        c.send("Send login info".encode())
        username, password = client.recv(1024).decode().split(",")
        if len(password) < 1:
            c.send("Please type password".encode())
        else:
            created = create_login(username, password)
            if created:
                c.send("Account created".encode())
            else:
                c.send("Username taken".encode())
    elif matching_string == "add card":
        c.send("Enter card num".encode())
        # should receive an int corresponding to user's new card
        username, card_num = client.recv(1024).decode().split(",")
        add_card(username, card_num)

while True:
    client, addr = server.accept()
    print("Connected to:", addr)
    # runs the function handle_client, which will handle a single client.
    # threading is needed to we can listen to multiple clients, while another is being handled.
    threading.Thread(target=handle_client, args=(client,)).start()