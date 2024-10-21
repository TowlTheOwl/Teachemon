import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("", 0))

address, port = s.getsockname()

print(address)

s.close()