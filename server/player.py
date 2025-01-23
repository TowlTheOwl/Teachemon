import socket

class Player:
    def __init__(self, conn:socket.socket, username:str):
        self.conn = conn
        self.queue = []
        self.username = username