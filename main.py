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
import pickle   # helps send data types other than string over socket

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
pointer_up = pygame.transform.rotate(pointer, 90)
pointer_down = pygame.transform.rotate(pointer, 270)
search_glass = pygame.image.load("Images/Magnifying Glass.png")

binder = pygame.image.load("Images/binder2.png")
resized_binder = pygame.transform.scale(binder, (1000, 600))
dispenser = pygame.image.load("Images/dispenser.png")
resized_dispenser = pygame.transform.scale(dispenser, (600, 600))
lever = pygame.image.load("Images/test6.png")
lever = pygame.transform.scale(lever, (65, 364))
rotated_lever = pygame.transform.rotate(lever, -16)
lever_rect = rotated_lever.get_rect(center=(480, 250))


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


#dicionary of cards for binder. numbers will correlate to cards, and they are all false for now 
dict = {}
for i in range(59):
    dict[i] = False

font = pygame.font.Font(None, 70)
# Font Setup
base_font = pygame.font.Font("teachemon.ttf", 30)
small_font = pygame.font.Font("teachemon.ttf", 15)

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
text_signup_bg = text_signup.get_rect(width=400, height=60, center=signup_button_pos)

text_choose_your_team = base_font.render("CHOOSE YOUR TEAM", True, (0, 0, 0))
text_choose_your_team_rect = text_choose_your_team.get_rect(center=(center_x, 30))

text_go = base_font.render("GO", True, (255, 255, 255))
button_go_pos = (center_x, 555)
text_go_rect = text_go.get_rect(center=button_go_pos)
text_go_bg = text_go.get_rect(width=200, height=60, center=button_go_pos)

pointer_pos = 1
pointer_selected = 1
pointer_hover = 0

timer_on = False
timer = None

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((server, port))
running = [True]
# login return, signup return, searching, match
server_messages = [None, None, None, None]
# username, password, cards?
userdata = [username, password, [1, 2, 3, 4, 5, 6, 7, 8, 9]]
selected_cards = [None, None, None, None]

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
            running[0] = False
        if event.type == pygame.KEYDOWN: 
            key_pressed = True
            keys = pygame.key.get_pressed()


        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if page == "SBattle" or page == "Battle":
                if pointer_pos < 3:
                    pointer_pos += 2
            elif page == "Binder":
                pointer_pos = 2
            elif page == "Choose Card":
                if pointer_pos <=4:
                    pointer_pos = 5
                elif pointer_pos < 7:
                    pointer_pos += 1
            else:
                pointer_pos += 1


        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if page == "SBattle" or page == "Battle":
                if pointer_pos > 2:
                    pointer_pos -= 2
            elif page == "Binder":
                pointer_pos = 1
            elif page == "Choose Card":
                if pointer_pos == 5:
                    pointer_pos = 1
                elif pointer_pos > 5:
                    pointer_pos -= 1
            else:
                if pointer_pos > 1:
                    pointer_pos -= 1


        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            keep_pointer = False

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
                    if len(userdata[2]) > 3:
                        page = "Choose Card"
                        if selected_cards[0] is None:
                            selected_cards[:] = userdata[2][:4]
                    else:
                        display_box(screen, "AT LEAST 4 CARDS NEEDED", base_font, 3)
                        page = "Battle_Menu"
                elif pointer_pos == 2:
                    page = "SBattle"
                elif pointer_pos == 3:
                    page = "Menu"
            elif page == "Choose Card":
                keep_pointer = True
                if pointer_pos <= 4:
                    pointer_selected = pointer_pos
                elif pointer_pos == 5:
                    if userdata[2][pointer_hover] not in selected_cards:
                        selected_cards[pointer_selected-1] = userdata[2][pointer_hover]
                elif pointer_pos == 6: # user clicked "Battle!"
                    page = "Loading"
                    connection.send("match".encode())
                elif pointer_pos == 7:
                    page = "Battle_Menu"
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
            elif page == "Loading":
                page = "Menu"
                connection.send("exit queue".encode())
                server_messages[2] = None
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
            if not keep_pointer:
                pointer_pos = 1
        

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if page == "SBattle" or page == "Battle":
                """
                [1 2
                 3 4]
                """
                if pointer_pos % 2 == 0:
                    pointer_pos -= 1
            elif page == "Binder":
                if pointer_pos == 1:
                    if left_page >= 3 and right_page <= 8:
                        left_page -= 2
                        right_page -= 2
            elif page == "Choose Card":
                if pointer_pos <= 4 and pointer_pos > 1:
                    pointer_pos -= 1
                if pointer_pos == 5:
                    if pointer_hover>0: pointer_hover-=1
    

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if page == "SBattle" or page == "Battle":
                if pointer_pos % 2 == 1:
                    pointer_pos += 1
            elif page == "Binder":
                if pointer_pos == 1:
                    if left_page > 0 and right_page < 7:
                        left_page += 2
                        right_page += 2
            elif page == "Choose Card":
                if pointer_pos < 4:
                    pointer_pos += 1
                if pointer_pos == 5:
                    if pointer_hover<len(userdata[2])-1: pointer_hover+=1


        if event.type == pygame.MOUSEBUTTONDOWN and page == "Claim":
            gacha = random.randint(0, 58)
            dict[gacha] = True 
        
            rotated_lever = pygame.transform.rotate(lever, -16)
            lever_rect = rotated_lever.get_rect(center=(480, 250))

            # Start rotation forward when the mouse is clicked
            rotating_forward = True
            rotating_backward = False

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
    
    elif page == "Choose Card":
        pointer_on = True
        
        pointer_x = 20
        # draw pointers
        if pointer_pos <= 4:
            pointer_y = 150
        elif pointer_pos == 5:
            pointer_y = 400
        elif pointer_pos == 6:
            pointer_x = 350
            pointer_y = 533
        else:
            pointer_x = 740
            pointer_y = 550
        
        draw_choose_your_team(screen, button_exit, text_choose_your_team, text_choose_your_team_rect, text_go, text_go_bg, text_go_rect, selected_cards, base_font)

        # draw selected card pointer
        screen.blit(pointer_down, ((pointer_selected * 200)-22, 60))
        # draw hover card pointer
        if pointer_pos <= 4:
            screen.blit(pointer_up, ((pointer_pos * 200)-22, 270))
        if pointer_pos == 5:
            screen.blit(pointer_down, (478, 270))
            screen.blit(pointer_up, (478, 480))
        
        draw_card_wheel(screen, userdata[2], selected_cards, pointer_hover, base_font, small_font)

    elif page == "Loading":
        pointer_on = True
        pointer_x = 740
        pointer_y = 550
        if server_messages[2] is not None and server_messages[2]:
            page = "Battle"
            timer = Timer(20, screen, running, base_font, (center_x, 50))
            timer_on = True
        else:
            draw_loading(screen, search_glass, circle_x, circle_y, button_exit)
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
        if timer_on:
            timer.draw()
            if timer.time == 0:
                timer_on = False
        
        if server_messages[3] is not None:
            if server_messages[3] == "DC":
                display_box(screen, "OPPONENT DISCONNECTED", base_font, 3)
                timer_on = False
                timer = None
                page = "Menu"
                server_messages[3] = None
        
    elif page == "Binder":
        pointer_x = 750
        pointer_y = 550
        if pointer_pos == 2:
            pointer_on = True
        else:
            pointer_on = False
        draw_binder(screen, left_page, right_page, resized_binder, font, button_exit)

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
        # Draw everything on screen
        #draw_claim(rotated_lever, lever_rect, gacha)  # Update display with gacha result
        #pygame.display.flip()  # Refresh the screen
        #clock.tick(30)

       
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
