#Import and Initialize PyGame and math
import pygame
pygame.init()
import math
import socket
from TypingBox import TypingBox

# Connect to server's IPv4 address
server = "localhost"
# Random open port
port = 5555

#Create display
ScreenWidth = 1000
ScreenHeight = 600
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
center_x = 500
center_y = 300
pygame.display.set_caption("Teachemon")
run = True

#Import Images
logo = pygame.image.load("Images/logo x4.png")
button_login = pygame.image.load("Images/login x5.png")
button_signup = pygame.image.load("Images/signup x5.png")
button_battle = pygame.image.load("Images/battle x5.png")
button_binder = pygame.image.load("Images/binder x5.png")
button_claim = pygame.image.load("Images/claim x5.png")
button_settings = pygame.image.load("Images/settings x5.png")
button_credits = pygame.image.load("Images/credits x5.png")
button_exit = pygame.image.load("Images/exit x5.png")
battle = pygame.image.load("Images/fight_scene.png")
pointer = pygame.image.load("Images/pointer x5.png")
search_glass = pygame.image.load("Images/Magnifying Glass.png")

#Define Variables
username = ""
password = ""
clock = pygame.time.Clock()
page = "Start"
pointer_on = True
pointer_x = 55
pointer_y = 257
circle_x = 0
circle_y = 0
username_box = TypingBox((center_x, 150), 800, 100, 1)
password_box = TypingBox((center_x, 350), 800, 100, 2)

# Font Setup
base_font = pygame.font.Font("teachemon.ttf", 30)

# LOGIN SCREEN VARIABLES
text_username = base_font.render("USERNAME", True, (0, 0, 0))
text_username_rect = text_username.get_rect(center=(center_x, 50))
text_password = base_font.render("PASSWORD", True, (0, 0, 0))
text_password_rect = text_password.get_rect(center=(center_x, 250))

text_login = base_font.render("LOGIN", True, (255, 255, 255), (66, 245, 152))
login_button_pos = (center_x, 450)
text_login_rect = text_login.get_rect(center=login_button_pos)
text_login_bg = text_login.get_rect(width=220, height=60, center=login_button_pos)
text_back = base_font.render("BACK", True, (0, 0, 0))
text_back_rect = text_back.get_rect(center=(center_x, 550))

text_signup = base_font.render("SIGN UP", True, (255, 255, 255), (66, 245, 152))
signup_button_pos = (center_x, 450)
text_signup_rect = text_signup.get_rect(center=signup_button_pos)
text_signup_bg = text_signup.get_rect(width=399, height=60, center=signup_button_pos)

# util
def card_to_list(c):
    return [bool(int(e)) for e in list(c)]

def list_to_card(l):
    return "".join([str(int(e)) for e in l])

#Define Screen drawing
def update_circle(radius):
    if circle_x >= radius:
        circle_y = math.sqrt((radius**2) - (circle_x**2))
def draw_start():
    screen.fill("grey")
    screen.blit(logo, (30,50))
    screen.blit(button_login, (100,262))
    screen.blit(button_signup, (100,332))
def draw_login(events, arrow_pos):
    screen.fill("grey")
    screen.blit(text_username, text_username_rect)
    screen.blit(text_password, text_password_rect)
    pygame.draw.rect(screen, (66, 245, 152), text_login_bg, border_radius=5)
    screen.blit(text_login, text_login_rect)
    screen.blit(text_back, text_back_rect)
    username_box.update(events, arrow_pos)
    password_box.update(events, arrow_pos)
    username_box.draw(screen, base_font)
    password_box.draw(screen, base_font)
def draw_signup(events, arrow_pos):
    screen.fill("grey")
    screen.blit(text_username, text_username_rect)
    screen.blit(text_password, text_password_rect)
    screen.blit(text_username, text_username_rect)
    screen.blit(text_password, text_password_rect)
    pygame.draw.rect(screen, (66, 245, 152), text_signup_bg, border_radius=5)
    screen.blit(text_signup, text_signup_rect)
    screen.blit(text_back, text_back_rect)
    username_box.update(events, arrow_pos)
    password_box.update(events, arrow_pos)
    username_box.draw(screen, base_font)
    password_box.draw(screen, base_font)
def draw_loading():
    screen.fill("darkgrey")
    screen.blit(search_glass, (500+circle_x,300+circle_y))
def draw_menu():
    screen.fill("grey")
    screen.blit(logo, (30,50))
    screen.blit(button_battle, (100,262))
    screen.blit(button_binder, (100,332))
    screen.blit(button_claim, (100,402))
    screen.blit(button_settings, (100,472))
def draw_battle():
    screen.blit(battle, (0,0))
def draw_binder():
    screen.fill("grey")
def draw_claim():
    screen.fill("grey")
    screen.blit(button_exit, (785,555))
def draw_settings():
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

# Handle Socket Connections
def check_received_data(received, expecting):
    if received != expecting:
        print(f"ERROR: received \"{received}\" when expecting \"{expecting}\"")
        raise Exception
def handle_login(login:bool, u: str, p: str) -> str:
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

def display_box(screen:pygame.Surface, text, font:pygame.font.FontType, seconds):
    rect = pygame.Rect(0, 0, 800, 300)
    rect.center = (center_x, center_y)
    pygame.draw.rect(screen, (100, 100, 100), rect)
    text_disp = font.render(text, True, (255, 255, 255))
    text_rect = text_disp.get_rect(center=(center_x, center_y))
    screen.blit(text_disp, text_rect)
    pygame.display.flip()
    pygame.time.wait(seconds*1000)

pointer_pos = 1

#Run Program
while run:
    key_pressed = False
    clock.tick(24)
    #Sense for events like Quit and Key presses
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN: 
            key_pressed = True
            keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if page == "Start":
                if pointer_y != 327:
                    pointer_y += 70
            elif page == "Menu":
                if pointer_y != 467:
                    pointer_y += 70
            elif page == "Settings":
                if pointer_y != 177:
                    pointer_y += 70
            elif page == "Login" or page == "Signup":
                if pointer_pos < 4:
                    pointer_pos += 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if page == "Start":
                if pointer_y != 257:
                    pointer_y -= 70
            elif page == "Menu":
                if pointer_y != 257:
                    pointer_y -= 70
            elif page == "Settings":
                if pointer_y != 107:
                    pointer_y -= 70
            elif page == "Login" or "Signup":
                if pointer_pos > 1:
                    pointer_pos -= 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if page == "Start":
                if pointer_y == 257:
                    page = "Login"
                elif pointer_y == 327:
                    page = "Signup"
                pointer_pos = 1
                pointer_x = 55
                pointer_y = 150
            elif page == "Menu":
                if pointer_y == 257:
                    page = "Battle"
                elif pointer_y == 327:
                    page = "Binder"
                elif pointer_y == 397:
                    page = "Claim"
                    pointer_x = 740
                    pointer_y = 550
                elif pointer_y == 467:
                    page = "Settings"
                    pointer_x = 270
                    pointer_y = 107
            elif page == "Claim":
                if pointer_x == 740:
                    page = "Menu"
                    pointer_x = 55
                    pointer_y = 397
            elif page == "Settings":
                if pointer_y == 107:
                    print("credits")
                elif pointer_y == 177:
                    page = "Menu"
                    pointer_x = 55
                    pointer_y = 467
            elif page == "Login" or page == "Signup":
                if pointer_pos == 3:
                    if page == "Login":
                        login_return = handle_login(True, username_box.return_text(), password_box.return_text())
                    else:
                        login_return = handle_login(False, username_box.return_text(), password_box.return_text())
                    page = server_return(screen, login_return, base_font, page)
                    if page == "Menu":
                        pointer_x = 55
                        pointer_y = 257
                if pointer_pos == 4:
                    page = "Start"
                    pointer_x = 55
                    pointer_y = 257
                    username_box.reset()
                    password_box.reset()

    if page == "Start":
        pointer_on = True
        draw_start()
    elif page == "Login":
        pointer_on = True
        if pointer_pos < 3:
            pointer_y = pointer_pos * 200 - 50 - 22
        else:
            pointer_y = 400-50-22 + (pointer_pos-2)*100
        draw_login(events, pointer_pos)
    elif page == "Signup":
        pointer_on = True
        if pointer_pos < 3:
            pointer_y = pointer_pos * 200 - 50 - 22
        else:
            pointer_y = 400-50-22 + (pointer_pos-2)*100
        draw_signup(events, pointer_pos)
    elif page == "Menu":
        pointer_on = True
        draw_menu()
    elif page == "Loading":
        pointer_on = False
        draw_loading()
    elif page == "Battle":
        draw_battle()
    elif page == "Binder":
        pointer_on = False
        draw_binder()
    elif page == "Claim":
        pointer_on = True
        draw_claim()
    elif page == "Settings":
        pointer_on = True
        draw_settings()
    if pointer_on:
        screen.blit(pointer, (pointer_x, pointer_y))
    pygame.display.update()

pygame.quit()