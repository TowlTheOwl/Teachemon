#Import and Initialize PyGame and math
import pygame
pygame.init()
import math
import socket
import random
from utils.utils import *
from utils.battle import *
from utils.draw import *

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
button_singleplayer = pygame.image.load("Images/singleplayer x5.png")
player_placeholder = pygame.image.load("Images/Test char.png")
enemy_placeholder = pygame.image.load("Images/Test opp.png")
button_multiplayer = pygame.image.load("Images/multiplayer x5.png")
button_exit = pygame.image.load("Images/exit x5.png")
battle_main = pygame.image.load("Images/battle_main.png")
battle_00 = pygame.image.load("Images/battle_00.png")
pointer = pygame.image.load("Images/pointer x5.png")
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
battle_page = "Main"
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
            pointer_pos += 1
            if False:
                pass
            elif page == "Menu" or page == "Battle_Menu":
                if pointer_y != 467:
                    pointer_y += 70
            elif page == "Battle_Menu":
                if pointer_y != 397:
                    pointer_y += 70
            elif page == "SBattle":
                if pointer_y != 530:
                    pointer_y += 95
            elif page == "Settings":
                if pointer_y != 177:
                    pointer_y += 70
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            pointer_pos -= 1
            if pointer_pos < 1:
                pointer_pos = 1
            if page == "Menu" or page == "Battle_Menu":
                if pointer_y != 257:
                    pointer_y -= 70
            elif page == "SBattle":
                if pointer_y != 435:
                    pointer_y -= 95
            elif page == "Settings":
                if pointer_y != 107:
                    pointer_y -= 70
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
                    page = "Battle_Menu"
                elif pointer_y == 327:
                    page = "Binder"
                    pointer_on = False
                elif pointer_y == 397:
                    page = "Claim"
                    pointer_x = 740
                    pointer_y = 550
                elif pointer_y == 467:
                    page = "Settings"
                    pointer_x = 270
                    pointer_y = 107
            elif page == "Battle_Menu":
                if pointer_y == 257:
                    page = "Loading"
                elif pointer_y == 327:
                    page = "SBattle"
                    pointer_y = 435
                    pointer_x = 30
                elif pointer_y == 397:
                    page = "Menu"
                    pointer_y = 257
            elif page == "SBattle":
                if sbattle_page == "00":
                    if pointer_x == 30 and pointer_y == 435:
                        sbattle_page = "10"
                    elif pointer_x == 525 and pointer_y == 435:
                        sbattle_page = "20"
                    elif pointer_x == 30 and pointer_y == 530:
                        sbattle_page = "30"
                    elif pointer_x == 525 and pointer_y == 530:
                        page = "Battle_Menu"
                        pointer_x = 55
                        pointer_y = 257
                elif sbattle_page == "10":
                    if pointer_x == 30 and pointer_y == 435:
                        sbattle_page = "11"
                    elif pointer_x == 525 and pointer_y == 435:
                        sbattle_page = "12"
                    elif pointer_x == 30 and pointer_y == 530:
                        sbattle_page = "13"
                    elif pointer_x == 525 and pointer_y == 530:
                        sbattle_page = "00"
                        pointer_x = 30
                        pointer_y = 435
                elif sbattle_page == "20":
                    if pointer_x == 30 and pointer_y == 435:
                        sbattle_page = "21"
                    elif pointer_x == 525 and pointer_y == 435:
                        sbattle_page = "22"
                    elif pointer_x == 30 and pointer_y == 530:
                        sbattle_page = "23"
                    elif pointer_x == 525 and pointer_y == 530:
                        sbattle_page = "00"
                        pointer_x = 30
                        pointer_y = 435
                elif sbattle_page == "30":
                    if pointer_x == 30 and pointer_y == 435:
                        sbattle_page = "31"
                    elif pointer_x == 525 and pointer_y == 435:
                        sbattle_page = "32"
                    elif pointer_x == 30 and pointer_y == 530:
                        sbattle_page = "33"
                    elif pointer_x == 525 and pointer_y == 530:
                        sbattle_page = "00"
                        pointer_x = 30
                        pointer_y = 435
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
            elif page == "Binder":
                if pointer_y == 550:
                    page = "Menu"
                    pointer_x = 55
                    pointer_y = 257
            elif page == "Login" or page == "Signup":
                if pointer_pos == 3:
                    if page == "Login":
                        login_return = handle_login(server, port, True, username_box.return_text(), password_box.return_text())
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
            pointer_pos = 1
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if page == "SBattle":
                if pointer_x != 30:
                    pointer_x -= 495
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if page == "SBattle":
                if pointer_x != 525:
                    pointer_x += 495

        if event.type == pygame.MOUSEBUTTONDOWN and page == "Claim":
            gacha = random.randint(0, 58)
            dict[gacha] = True 
        
            rotated_lever = pygame.transform.rotate(lever, -16)
            lever_rect = rotated_lever.get_rect(center=(480, 250))

            # Start rotation forward when the mouse is clicked
            rotating_forward = True
            rotating_backward = False            

        # Binder 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and not pointer_on:
            if page == "Binder" and left_page > 0 and right_page < 7:
                left_page += 2
                right_page += 2
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and not pointer_on:
            if page == "Binder" and left_page >= 3 and right_page <= 8:
                left_page -= 2
                right_page -= 2
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if page == "Binder":
                pointer_x = 750
                pointer_y = 550
                pointer_on = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and page == "Binder":
            pointer_on = False


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
        
        if pointer_pos < 3:
            pointer_y = pointer_pos * 200 - 50 - 22
        else:
            pointer_y = 400-50-22 + (pointer_pos-2)*100
        draw_login(screen, events, pointer_pos, (text_username, text_username_rect, username_box), 
                   (text_password, text_password_rect, password_box), (text_login_bg, text_login, text_login_rect), (text_back, text_back_rect), base_font)
        
    elif page == "Signup":
        pointer_on = True
        if pointer_pos > 4:
            pointer_pos = 4

        if pointer_pos < 3:
            pointer_y = pointer_pos * 200 - 50 - 22
        else:
            pointer_y = 400-50-22 + (pointer_pos-2)*100
        draw_login(screen, events, pointer_pos, (text_username, text_username_rect, username_box), 
                   (text_password, text_password_rect, password_box), (text_signup_bg, text_signup, text_signup_rect), (text_back, text_back_rect), base_font)
        
    elif page == "Menu":
        pointer_on = True
        draw_menu(screen, logo, button_battle, button_binder, button_claim, button_settings)
        
    elif page == "Loading":
        pointer_on = False
        draw_loading(screen, search_glass, circle_x, circle_y)
        toUpdate = update_circle(circle_x, circle_y, circle_angle, circle_start, 50)
        circle_x, circle_y, circle_angle, circle_start = toUpdate
    elif page == "Battle_Menu":
        draw_battle_menu(screen, logo, button_multiplayer, button_singleplayer, button_exit)
    elif page == "SingleplayerMenu":
        draw_singleplayer_menu(screen)
    elif page == "SBattle":
        draw_singleplayer_battle(screen, sbattle_page, player_placeholder, enemy_placeholder, fontx3, battle_00, battle_main, pteach1)
        
    elif page == "Binder":
        draw_binder(screen, left_page, right_page, resized_binder, font, button_exit)

    elif page == "Claim":
        pointer_on = True
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
        draw_settings()
    if pointer_on:
        screen.blit(pointer, (pointer_x, pointer_y))

    pygame.display.update()

pygame.quit()
