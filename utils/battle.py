import math
import pygame
import socket

def update_circle(circle_x, circle_y, circle_angle, circle_start: bool, radius) -> tuple:
    """
    Update circle values for magnifying glass
    """
    if circle_start:
        circle_x = radius
        circle_start = False
    circle_x = math.sin(circle_angle) * radius
    circle_y = math.cos(circle_angle) * radius
    circle_angle += 0.05
    if circle_angle == 360:
        circle_angle = 0
    return (circle_x, circle_y, circle_angle, circle_start)

def draw_claim(screen, button_exit, dispenser, font, coins, gacha):
    screen.fill("grey")
    screen.blit(button_exit, (785,555))
    screen.blit(dispenser, (200,10))
    screen.blit(font.render(str(coins), True, (0, 0, 0)), (25, 5))
    screen.blit(font.render(str(gacha), True, (0, 0, 0)), (480, 250))

def draw_rotating_lever(screen, new_lever, rect):
    screen.blit(new_lever, rect)

def draw_settings(screen, button_credits, button_exit):
    screen.fill("grey")
    screen.blit(button_credits, (315,112))
    screen.blit(button_exit, (398,182))

def server_return(screen, login_return, font, page) -> str:
    # Display a rectangle saying what went wrong
    if page == "Login":
        if login_return == "1":
            return "Menu"
        elif login_return == "-1":
            display_box(screen, "NO MATCHING USERNAME", font, 3)
        else:
            display_box(screen, "INCORRECT PASSWORD", font, 3)
        return "Login"
    else:
        if login_return == "1":
            return "Menu"
        elif login_return == "-1":
            display_box(screen, "USERNAME TAKEN", font, 3)
        else:
            display_box(screen, "BLANK PASSWORD", font, 3)
        return "Signup"

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
    
def handle_login(server, port, login:bool, u: str, p: str) -> str:
    """
    Parameters:
    login: True if logging in, False if creating login
    u: username
    p: password

    Return:
    -1: no matching username/username taken
    0: incorrect password/blank password
    1: match/created
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server, port))
        check_received_data(client.recv(1024).decode(), "Enter matching string: ")
        if login:
            client.send("login".encode())
        else:
            client.send("create login".encode())
        check_received_data(client.recv(1024).decode(), "Send login info")
        client.send(f"{u},{p}".encode())
        received = client.recv(1024).decode()
    return received