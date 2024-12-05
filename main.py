#Import and Initialize PyGame and math
import pygame
pygame.init()
import math
import socket
import random
from utils.utils import *
from utils.battle import *
from utils.draw import *
import threading

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

#Import Images
logo = pygame.image.load("Images/logo x4.png")
button_login = pygame.image.load("Images/login x5.png")
button_signup = pygame.image.load("Images/signup x5.png")
button_battle = pygame.image.load("Images/battle x5.png")
button_binder = pygame.image.load("Images/binder x5.png")
button_claim = pygame.image.load("Images/claim x5.png")
button_settings = pygame.image.load("Images/settings x5.png")
button_credits = pygame.image.load("Images/credits x5.png")
button_singleplayer = pygame.image.load("Images/singleplayer x5.png")
player_placeholder = pygame.image.load("Images/Test char.png")
enemy_placeholder = pygame.image.load("Images/Test opp.png")
button_multiplayer = pygame.image.load("Images/multiplayer x5.png")
button_exit = pygame.image.load("Images/exit x5.png")
battle_main = pygame.image.load("Images/battle_main.png")
battle_00 = pygame.image.load("Images/battle_00.png")
pointer = pygame.image.load("Images/pointer x5.png")
search_glass = pygame.image.load("Images/Magnifying Glass.png")
binder_highlight = pygame.image.load("Images/yellow border.png")
back_card = pygame.image.load("Images/card_back.png")

binder = pygame.image.load("Images/binder2.png")
resized_binder = pygame.transform.scale(binder, (1000, 600))
dispenser = pygame.image.load("Images/dispenser.png")
resized_dispenser = pygame.transform.scale(dispenser, (600, 600))
lever = pygame.image.load("Images/test6.png")
lever = pygame.transform.scale(lever, (65, 364))
rotated_lever = pygame.transform.rotate(lever, -16)
lever_rect = rotated_lever.get_rect(center=(480, 250))
binder_highlight = pygame.transform.scale(binder_highlight, (222, 196))
back_card = pygame.transform.scale(back_card, (90, 123))

page = "Start"

#Define Variables
username = ""
password = ""
send = ""
receive = ""
sbattle_page = "00"
battle_page = "00"
fontx3 = pygame.font.Font("Teachemon.ttf", 21)
fontx5 = pygame.font.Font("Teachemon.ttf", 35)
teacher_file = open("Data/TeacheData.txt", "r")
teacher_data = teacher_file.readlines()
pteach1 = teacher_data[0].split(",")
pteach2 = []
pteach3 = []
pointer_on = True
pointer_x = 55
pointer_y = 257
left_page = 1
right_page = 2
coins = 0
circle_x = 0
circle_y = 0
circle_angle = 0
circle_start = True
gacha = ""
max_angle = 90
clock = pygame.time.Clock()
rotating_backward = False
rotating_forward = False 
username_box = TypingBox((center_x, 150), 800, 100, 1)
password_box = TypingBox((center_x, 350), 800, 100, 2)
highlight_x = 95
highlight_y = 73
highlight_num = 0

#dicionary of cards for binder. numbers will correlate to cards, and they are all false for now 
dict = {}
for i in range(59):
    dict[i] = False

font = pygame.font.Font(None, 70)
# Font Setup
base_font = pygame.font.Font("teachemon.ttf", 30)

pivot_point = (450, 400) # The fixed pivot point around which to rotate
angle = 0  # Initial rotation angle
rotation_speed = 2  # Degrees per frame

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

pointer_pos = 1

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((server, port))
running = [True]
# login return, signup return, searching
server_messages = [None, None, None]
userdata = [username, password]

threading.Thread(target=handle_server_connection, args=(connection,running,server_messages,userdata)).start()

#Run Program
while running[0]:
    key_pressed = False
    clock.tick(24)
    #Sense for events like Quit and Key presses
    events = pygame.event.get()

    # Check if user in queue
    if server_messages[2] is not None:
        if not server_messages[2]:
            page = "Loading"

    for event in events:
        if event.type == pygame.QUIT:
            connection.close()
            run = False
        if event.type == pygame.KEYDOWN: 
            key_pressed = True
            keys = pygame.key.get_pressed()


        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if page == "SBattle" or page == "Battle":
                if pointer_pos < 3:
                    pointer_pos += 2
            elif page == "Binder":
                if highlight_y == 344:
                    pointer_pos = 2
            else:
                pointer_pos += 1


        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if page == "SBattle" or page == "Battle":
                if pointer_pos > 2:
                    pointer_pos -= 2
            elif page == "Binder":
                pointer_pos = 1
            else:
                if pointer_pos > 1:
                    pointer_pos -= 1


        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if page == "Start":
                if pointer_pos == 1:
                    page = "Login"
                elif pointer_pos == 2:
                    page = "Signup"
            elif page == "Menu":
                if pointer_pos == 1:
                    page = "Battle_Menu"
                elif pointer_pos == 2:
                    page = "Binder"
                elif pointer_pos == 3:
                    page = "Claim"
                elif pointer_pos == 4:
                    page = "Settings"
            elif page == "Battle_Menu":
                if pointer_pos == 1:
                    page = "Loading"
                    connection.send("match".encode())
                elif pointer_pos == 2:
                    page = "SBattle"
                elif pointer_pos == 3:
                    page = "Menu"
            elif page == "SBattle":
                if sbattle_page == "00":
                    if pointer_pos == 1:
                        sbattle_page = "10"
                    elif pointer_pos == 2:
                        sbattle_page = "20"
                    elif pointer_pos == 3:
                        sbattle_page = "30"
                    elif pointer_pos == 4:
                        page = "Battle_Menu"
                        pointer_pos = 1
                elif sbattle_page in ["10", "20", "30"]:
                    if pointer_pos == 1:
                        sbattle_page = sbattle_page[0] + "1"
                    if pointer_pos == 2:
                        sbattle_page = sbattle_page[0] + "2"
                    if pointer_pos == 3:
                        sbattle_page = sbattle_page[0] + "3"
                    if pointer_pos == 4:
                        pointer_pos = 1
                        sbattle_page = "00"
            elif page == "Battle":
                if battle_page == "00":
                    if pointer_pos == 1:
                        battle_page = "10"
                    elif pointer_pos == 2:
                        battle_page = "20"
                    elif pointer_pos == 3:
                        battle_page = "30"
                    elif pointer_pos == 4:
                        page = "Battle_Menu"
                        pointer_pos = 1
                elif battle_page in ["10", "20", "30"]:
                    if pointer_pos == 1:
                        battle_page = battle_page[0] + "1"
                    if pointer_pos == 2:
                        battle_page = battle_page[0] + "2"
                    if pointer_pos == 3:
                        battle_page = battle_page[0] + "3"
                    if pointer_pos == 4:
                        pointer_pos = 1
                        battle_page = "00"
            elif page == "Claim":
                if pointer_pos == 1:
                    page = "Menu"
            elif page == "Settings":
                if pointer_pos == 1:
                    print("credits")
                elif pointer_pos == 2:
                    page = "Menu"
            elif page == "Binder":
                if pointer_pos == 2:
                    page = "Menu"
            elif page == "Login" or page == "Signup":
                if pointer_pos == 3:
                    # update user data and requeset login/signup
                    userdata[0] = username_box.return_text()
                    userdata[1] = password_box.return_text()
                    if page == "Login":
                        # login_return = handle_login(connection, True, username_box.return_text(), password_box.return_text())
                        connection.send("login".encode())
                    else:
                        # login_return = handle_login(connection, False, username_box.return_text(), password_box.return_text())
                        connection.send("signup".encode())
                if pointer_pos == 4:
                    page = "Start"
                    username_box.reset()
                    password_box.reset()
            pointer_pos = 1
        

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if page == "SBattle" or page == "Battle":
                """
                [1 2
                 3 4]
                """
                if pointer_pos % 2 == 0:
                    pointer_pos -= 1
            # for individual flipping of binder
            #elif page == "Binder":
                #if pointer_pos == 1:
                    #if left_page >= 3 and right_page <= 8:
                        #left_page -= 2
                        #right_page -= 2
    

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if page == "SBattle" or page == "Battle":
                if pointer_pos % 2 == 1:
                    pointer_pos += 1
            #elif page == "Binder":
                #if pointer_pos == 1:
                    #if left_page > 0 and right_page < 7:
                        #left_page += 2
                        #right_page += 2


        if event.type == pygame.MOUSEBUTTONDOWN and page == "Claim":
            gacha = random.randint(0, 58)
            dict[gacha] = True 
        
            rotated_lever = pygame.transform.rotate(lever, -16)
            lever_rect = rotated_lever.get_rect(center=(480, 250))

            # Start rotation forward when the mouse is clicked
            rotating_forward = True
            rotating_backward = False

        
        if page == "Binder" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not pointer_on:
                if highlight_x == 285:
                    highlight_x += 228
                    highlight_num += 7
                else:
                    highlight_x += 95
                    highlight_num += 1
                if highlight_x > 708:
                    if right_page < 8:
                        highlight_x = 95
                        right_page += 2
                        left_page += 2
                    else:
                        highlight_x = 708
                
            elif event.key == pygame.K_LEFT and not pointer_on:
                if highlight_x == 513:
                    highlight_x -= 228
                    highlight_num -= 7
                else:
                    highlight_x -= 95
                    highlight_num -= 1
                if highlight_x < 180:
                    if right_page > 2:
                        right_page -= 2
                        left_page -= 2
                        highlight_x = 703
                    else:
                        highlight_x = 95

            elif event.key == pygame.K_UP and highlight_y >= 211:
                if pointer_on:
                    highlight_y = 344
                else:
                    highlight_y -= 133
                    highlight_num -= 3

            elif event.key == pygame.K_DOWN and highlight_y <= 211:
                highlight_y += 133
                highlight_num += 3

    ### HANDLE SERVER MESSAGES
    

    if page == "Start":
        pointer_on = True
        if pointer_pos > 2:
            pointer_pos = 2
        
        pointer_x = 55
        pointer_y = 257 + 70 * (pointer_pos-1)
        draw_start(screen, logo, button_login, button_signup)
        
    elif page == "Login":
        pointer_on = True
        if pointer_pos > 4:
            pointer_pos = 4
        pointer_x = 55
        if pointer_pos < 3:
            pointer_y = pointer_pos * 200 - 50 - 22
        else:
            pointer_y = 400-50-22 + (pointer_pos-2)*100
        draw_login(screen, events, pointer_pos, (text_username, text_username_rect, username_box), 
                   (text_password, text_password_rect, password_box), (text_login_bg, text_login, text_login_rect), (text_back, text_back_rect), base_font)

        
        # check login response
        if server_messages[0] is not None:
            response = server_messages[0]
            if response == "1":
                page = "Menu"
            elif response == "0":
                display_box(screen, "INCORRECT PASSWORD", base_font, 3)
            elif response == "2":
                display_box(screen, "ALREADY LOGGED IN", base_font, 3)
            elif response == "3":
                display_box(screen, "NO MATCHING USERNAME", base_font, 3)
            server_messages[0] = None
        
    elif page == "Signup":
        pointer_on = True
        if pointer_pos > 4:
            pointer_pos = 4
        
        pointer_x = 55
        if pointer_pos < 3:
            pointer_y = pointer_pos * 200 - 50 - 22
        else:
            pointer_y = 400-50-22 + (pointer_pos-2)*100
        draw_login(screen, events, pointer_pos, (text_username, text_username_rect, username_box), 
                   (text_password, text_password_rect, password_box), (text_signup_bg, text_signup, text_signup_rect), (text_back, text_back_rect), base_font)
        
        # check signup response
        if server_messages[1] is not None:
            response = server_messages[1]
            if response == "1":
                page = "Menu"
            elif response == "0":
                display_box(screen, "BLANK PASSWORD", base_font, 3)
            elif response == "2":
                display_box(screen, "USERNAME TAKEN", base_font, 3)
            server_messages[1] = None

    elif page == "Menu":
        pointer_on = True
        if pointer_pos > 4:
            pointer_pos = 4
        
        pointer_x = 55
        pointer_y = 257 + 70 * (pointer_pos - 1)
        draw_menu(screen, logo, button_battle, button_binder, button_claim, button_settings)

    elif page == "Battle_Menu":
        if pointer_pos > 3:
            pointer_pos = 3
        
        pointer_x = 55
        pointer_y = 257 + 70 * (pointer_pos - 1)
        draw_battle_menu(screen, logo, button_multiplayer, button_singleplayer, button_exit)

    elif page == "SingleplayerMenu":
        draw_singleplayer_menu(screen)

    elif page == "SBattle":
        """
        pointer pos
        [1 2
         3 4]
        """
        if pointer_pos % 2 == 1:
            pointer_x = 30
        else:
            pointer_x = 525
        
        if pointer_pos <= 2:
            pointer_y = 435
        else:
            pointer_y = 530
        draw_battle(screen, sbattle_page, player_placeholder, enemy_placeholder, fontx3, battle_00, battle_main, pteach1)
        
    elif page == "Loading":
        pointer_on = False
        if server_messages[2] is not None and server_messages[2]:
            page = "Battle"
        else:
            draw_loading(screen, search_glass, circle_x, circle_y)
            toUpdate = update_circle(circle_x, circle_y, circle_angle, circle_start, 50)
            circle_x, circle_y, circle_angle, circle_start = toUpdate
    
    elif page == "Battle":
        pointer_on = True
        if pointer_pos % 2 == 1:
            pointer_x = 30
        else:
            pointer_x = 525
        
        if pointer_pos <= 2:
            pointer_y = 435
        else:
            pointer_y = 530

        draw_battle(screen, battle_page, player_placeholder, enemy_placeholder, fontx3, battle_00, battle_main, pteach1)

        
    elif page == "Binder":
        pointer_x = 750
        pointer_y = 550
        if pointer_pos == 2:
            pointer_on = True
        else:
            pointer_on = False
        draw_binder(screen, left_page, right_page, resized_binder, base_font, button_exit)
        screen.blit(back_card, (150, 101))
        screen.blit(back_card, (245, 101))
        screen.blit(back_card, (340, 101))

        screen.blit(binder_highlight, (highlight_x, highlight_y))


        # for future - making card bigger when pressed enter 
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not pointer_pos == 2:
            #screen.blit(base_font.render(str(highlight_num), True, (0, 0, 0)), (300, 300))


    elif page == "Claim":
        pointer_on = True
        pointer_pos = 1
        pointer_x = 740
        pointer_y = 550
        draw_claim(screen, button_exit, resized_dispenser, font, coins, gacha)
        # Update rotation angle based on direction
        if rotating_forward:
            angle += rotation_speed
            if angle >= max_angle:
                angle = max_angle
                rotating_forward = False
                rotating_backward = True
            rotated_lever = pygame.transform.rotate(rotated_lever, -2)
        elif rotating_backward:
            angle -= rotation_speed
            if angle <= 0:
                angle = 0
                rotating_backward = False
            rotated_lever = pygame.transform.rotate(rotated_lever, 2)
            
        #if rotating_forward or rotating_backward:
        lever_rect = rotated_lever.get_rect(center=pivot_point)
        draw_rotating_lever(screen, rotated_lever, lever_rect)    

       
    elif page == "Settings":
        pointer_on = True
        if pointer_pos > 2:
            pointer_pos = 2
        
        pointer_x = 270
        pointer_y = 107 + 70 * (pointer_pos-1)
        draw_settings(screen, button_credits, button_exit)
    if pointer_on:
        screen.blit(pointer, (pointer_x, pointer_y))

    pygame.display.update()

pygame.quit()
