import socket

# Connect to server's IPv4 address
server = "localhost"
# Random open port
port = 5555


while True:
    # AF_INET: internet address family for IPv4, SOCK_STREAM is socket type for TCP,
    # a protocol that will be used to transport messages in the network. 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server, port))
    # When connected to the server, should receive a messages 
    print(client.recv(1024).decode())
    inp = input("> ")
    # login, match, create login,
    if inp == "login" or inp == "create login":
        # send match string to tell the server what we want to do
        client.send(inp.encode())
        print(client.recv(1024).decode())
        username = input("Username: ")
        password = input("Password: ")
        client.send(f"{username},{password}".encode())
        print(client.recv(1024).decode())
    elif inp == "add card":
        client.send(inp.encode())
        print(client.recv(1024).decode())
        client.send(f"{input("Username: ")},{input("Card num: ")}".encode())
    elif inp == "quit":
        break
    else:
        print("Invalid")
    client.close()