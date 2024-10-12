import socket

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to a specific address and port
s.bind(('localhost', 0))

# Get the socket's address
address, port = s.getsockname()

# Check if the address is IPv4
if address.startswith('127.'):  # This is a simple check for localhost
    print("IPv4 address:", address)
else:
    print("Not an IPv4 address:", address)

# Close the socket
s.close()