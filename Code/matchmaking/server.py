import socket
import threading

# Server's IPv4 address, port
serverIP = "127.0.0.1"
port = 5555
# See client.py for AF_INET and SOCK_STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serverIP, port))

server.listen()
print("Listening...")

# list of client in match queue
queue = []

def find_login(username: str, password: str) -> int:
    """
    parameters:
    username and password of the user

    return:
    -1: no matching username
    0: incorrect password
    1: match
    """
    with open("data.txt", "r") as file:
        data = file.readlines()[1:]
        for info in data:
            info = info.split(", ")
            if info[0] == username:
                if info[1] == password:
                        return 1
                return 0
        return -1

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
        pass
        # to be implemented



while True:
    client, addr = server.accept()
    print("Connected to:", addr)
    # runs the function handle_client, which will handle a single client.
    # threading is needed to we can listen to multiple clients, while another is being handled.
    threading.Thread(target=handle_client, args=(client,)).start()