import pygame
import socket

class TypingBox:
    def __init__(self, pos:tuple, length, width, id) -> None:
        self.text = ""
        self.x = pos[0]
        self.y = pos[1]
        self.length = length
        self.width = width
        self.rect = pygame.Rect(self.x, self.y, length, width)
        self.rect.center = pos
        self.id = id
        self.valid_keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def update(self, events, arrow):
        if arrow == self.id:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    for key in self.valid_keys:
                        if len(self.text)<20 and event.key == pygame.key.key_code(key):
                            self.text += key.upper()
    def return_rect(self):
        return self.rect
    def return_text(self):
        return self.text
    def draw(self, screen, font:pygame.font.Font):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        text_render = font.render(self.text, True, (255, 255, 255))
        text_rect = text_render.get_rect(centery=self.y, left=self.x-self.length/2+10)
        screen.blit(text_render, text_rect)
    def reset(self):
        self.text = ""

def card_to_list(c):
    return [bool(int(e)) for e in list(c)]

def list_to_card(l):
    return "".join([str(int(e)) for e in l])

# def server_return(screen, login_return, font, page) -> str:
#     # Display a rectangle saying what went wrong
#     if page == "Login":
#         if login_return == "1":
#             return "Menu"
#         elif login_return == "-1":
#             display_box(screen, "NO MATCHING USERNAME", font, 3)
#         else:
#             display_box(screen, "INCORRECT PASSWORD", font, 3)
#         return "Login"
#     else:
#         if login_return == "1":
#             return "Menu"
#         elif login_return == "-1":
#             display_box(screen, "USERNAME TAKEN", font, 3)
#         else:
#             display_box(screen, "BLANK PASSWORD", font, 3)
#         return "Signup"

def display_box(screen:pygame.Surface, text, font:pygame.font.FontType, seconds):
    center_x, center_y = get_center()
    rect = pygame.Rect(0, 0, 800, 300)
    rect.center = (center_x, center_y)
    pygame.draw.rect(screen, (100, 100, 100), rect)
    text_disp = font.render(text, True, (255, 255, 255))
    text_rect = text_disp.get_rect(center=(center_x, center_y))
    screen.blit(text_disp, text_rect)
    pygame.display.flip()
    pygame.time.wait(seconds*1000)

def get_center():
    center_x = 500
    center_y = 300
    return center_x, center_y

# Handle Socket Connections
def check_received_data(received, expecting):
    if received != expecting:
        print(f"ERROR: received \"{received}\" when expecting \"{expecting}\"")
        raise Exception
    
# def handle_login(conn:socket.socket, login:bool, u: str, p: str) -> str:
#     """
#     Parameters:
#     login: True if logging in, False if creating login
#     u: username
#     p: password

#     Return:
#     -1: no matching username/username taken
#     0: incorrect password/blank password
#     1: match/created
#     """
#     check_received_data(conn.recv(1024).decode(), "Enter matching string: ")
#     if login:
#         conn.send("login".encode())
#     else:
#         conn.send("create login".encode())
#     check_received_data(conn.recv(1024).decode(), "Send login info")
#     conn.send(f"{u},{p}".encode())
#     received = conn.recv(1024).decode()
#     return received

def handle_server_connection(conn:socket.socket, running, messages, userdata):
    """
    userdata: [username, password, card: list]
    messages: [login return, signup return, queue status]
    """
    while running[0]:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                print("Connection closed by the server.")
                conn.close()
            print(f"Received: {msg}")
            if msg == "cc":
                # server is checking if we are still connected
                conn.send("1".encode())
            
            elif msg[0] == "r":
                # server is requesting data
                to_parse = msg[1:]
                to_parse = to_parse.split(",")
                to_send = ""
                for requested_info in to_parse:
                    if len(to_send) != 0:
                        to_send += ","
                    if requested_info == "username":
                        to_send += str(userdata[0])
                    elif requested_info == "password":
                        to_send += str(userdata[1])
                    else:
                        raise Exception(f"Unknown info requested by the server: {requested_info}")
                conn.send(to_send.encode())
                print(f"Sent: {to_send}")
            
            elif msg[0] == "s":
                # server is sending info
                info = msg[1:]
                if info[0] == "l":
                    # server responded to login request
                    messages[0] = info[1]
                elif info[0] == "s":
                    # server responded to signup request
                    messages[1] = info[1]
                elif info[0] == "m":
                    # server is sending match info
                    message = info[1:]
                    if message == "SEARCHING":
                        messages[2] = False
                    elif message == "MATCH":
                        messages[2] = True
                    elif message == "DC":
                        messages[3] = "DC"
                elif info[0] == "c":
                    # server sent card info
                    message = info[1:]
                    userdata[2][:] = [int(e) for e in message.split(",")]
            else:
                raise Exception(f"unexpected message, received {msg}")
        except Exception as e:
            if isinstance(e, ConnectionResetError) or isinstance(e, ConnectionAbortedError) or isinstance(e, OSError):
                print("SERVER CONNECTION IS CLOSED, TERMINATING")
                running[0] = False