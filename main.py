#Import and Initialize PyGame and math
import json
import pygame
pygame.init()
import math
import socket
import random
from utils.utils import *
from utils.battle import *
from utils.draw import *
import threading
import numpy as np
import csv

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
vs_bg = pygame.image.load("Images/vs_bg.png")
pointer = pygame.image.load("Images/pointer x5.png")
pointer_up = pygame.transform.rotate(pointer, 90)
pointer_down = pygame.transform.rotate(pointer, 270)
search_glass = pygame.image.load("Images/Magnifying Glass.png")
binder_highlight = pygame.image.load("Images/yellow_border.png")
placeholder_card = pygame.image.load("Images/placeholder.png")
main_screen_bg = pygame.image.load("Images/mainbg.png")
coin = pygame.image.load("Images/coin.png")
login = pygame.image.load("Images/loginbg.png")
animation_bg = pygame.image.load("Images/animation_bg.png")
animation_bg = pygame.transform.scale_by(animation_bg, 50)

resized_coin = pygame.transform.scale(coin, (112,112))
login_bg = pygame.transform.scale(login, (ScreenWidth, ScreenHeight))
screen_bg = pygame.transform.scale(main_screen_bg, (ScreenWidth, ScreenHeight))
binder = pygame.image.load("Images/binder2.png")
resized_binder = pygame.transform.scale(binder, (1000, 600))
dispenser = pygame.image.load("Images/draft dispense.png")
resized_dispenser = pygame.transform.scale(dispenser, (600, 600))
sprite_sheet = pygame.image.load("Images/dispense sheet.png").convert_alpha()
cardanim_sheet = pygame.image.load("Images/cardanim.png").convert_alpha()
lever = pygame.image.load("Images/test6.png")
lever = pygame.transform.scale(lever, (65, 364))
rotated_lever = pygame.transform.rotate(lever, -16)
cut_scene_sheet = pygame.image.load("Images/cut_scene_sheet.png").convert_alpha()


page = "Start"

#Define Variables
username = ""
password = ""
send = ""
receive = ""
sbattle_page = "00"
battle_page = "00"
fontx1 = pygame.font.Font("Teachemon.ttf", 15)
fontx3 = pygame.font.Font("Teachemon.ttf", 21)
fontx5 = pygame.font.Font("Teachemon.ttf", 35)

print("Retrieving Teachemon data.")
with open("Data/TeachemonData - Teachemon.csv", 'r') as file:
    teachemon_data = []
    csvfile = csv.DictReader(file) # reads data file for teachemon
    for row in csvfile:
        teachemon_data.append(row)
print("Complete.\r")


pointer_on = True
pointer_x = 55
pointer_y = 257
left_page = 1
coins = 50
circle_x = 0
circle_y = 0
circle_angle = 0
circle_start = True
gacha = ""
clock = pygame.time.Clock()
username_box = TypingBox((center_x, 150), 800, 100, 1)
password_box = TypingBox((center_x, 350), 800, 100, 2)
highlight_x = 95
highlight_y = 73
highlight_num = 0

#animaiton for card reveal
alpha = 0
fade_started = False
fading_in = False
fade_speed = 5
WHITE = (225, 225, 225)
card_started = False
card_anim = 0
max_cardanim = 30
#not enough coins display
no_coins = ""
no_coins_timer = 0
no_coins_duration = 2000
owned = False

#sprite animation for card dispenser
back = (0,0,0)

def get_image(sheet, frame, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0,0), ((frame * width), 0, width, height))
    image.blit(sheet, (0,0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)

    return image

#animation list for card dispenser
animation_list = []
animation_steps = [1, 11]
action = 0
last_update = pygame.time.get_ticks()
anim_cooldown = 120
dispenser_frame = 0
step = 0

display_started = False
cardanim_list = []
cardanim_frame = 0
cardanim_cooldown = 75
for i in range(11):
    cardanim_list.append(get_image(cardanim_sheet, i, 500, 300, 2, back))

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(get_image(sprite_sheet, step, 320, 320, 1.75, back))
        step += 1
    animation_list.append(temp_img_list)

cut_scene_animation = []
cut_scene_frame = 0
cut_scene_cooldown = 75
for i in range(33):
    cut_scene_animation.append(get_image(cut_scene_sheet, i, 1000, 600, 1.3, back))

#variable for card zoom factor
card_zoom = 1
#card display for claim
card_visible = False
current_card = None
card_rect = None
lever_rect = pygame.Rect(445, 288, 40, 170)

#dicionary of cards for binder, key = card#, value = image. array cards_owned stores card# of cards owned
card_images = {}
card_back = pygame.transform.scale(pygame.image.load("Images/card_back.png"), (90, 123))
for i in range(59):
    if i < 18: 
        card = pygame.transform.scale(pygame.image.load("Images/card_" + str(i) + ".png"), (90, 123))
    #temporary placeholder for the rest of the card b/c too lazy to load in rn
    else:
        card = pygame.transform.scale(pygame.image.load("Images/card_placeholder.png"), (90, 123))

    card_images[i] = card

font = pygame.font.Font(None, 70)
# Font Setup
big_font = pygame.font.Font("teachemon.ttf", 38)
base_font = pygame.font.Font("teachemon.ttf", 30)
small_font = pygame.font.Font("teachemon.ttf", 15)



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

server_messages = [None, None, None, None, None, None, None] # check utils

selected_cards = [None, None, None, None]
userdata = [username, password, [], selected_cards, coins] # username, password, owned cards, selected cards
cards_owned = userdata[2]
must_swap = False
opponent_username = None

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
                if highlight_num%9//3 == 2:
                    pointer_pos = 2
                elif highlight_num%9//3 < 2:
                    highlight_num += 3
                if card_zoom >= 3:
                    card_zoom = 1
            elif page == "Choose Card":
                if pointer_pos <=4:
                    pointer_pos = 5
                elif pointer_pos < 7:
                    pointer_pos += 1
            elif page == "Trade":
                pointer_pos = (pointer_pos%2) + 1
            else:
                pointer_pos += 1


        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if page == "SBattle" or page == "Battle":
                if pointer_pos > 2:
                    pointer_pos -= 2
            elif page == "Binder":
                if pointer_pos == 2:
                    pointer_pos = 1
                elif highlight_num%9//3 > 0:
                    highlight_num -= 3
                if card_zoom >= 3:
                    card_zoom = 1
            elif page == "Choose Card":
                if pointer_pos == 5:
                    pointer_pos = 1
                elif pointer_pos > 5:
                    pointer_pos -= 1
            elif page == "Trade":
                pointer_pos = (pointer_pos%2) + 1
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
                    left_page = 1
                    card_zoom = 1
                elif pointer_pos == 3:
                    page = "Claim"
                    dispenser_frame = 0
                    action = 0
                elif pointer_pos == 4:
                    page = "Settings"
            elif page == "Battle_Menu":
                if pointer_pos == 1:
                    if len(userdata[2]) > 3:
                        page = "Choose Card"
                        if selected_cards[0] is None:
                            selected_cards[:] = userdata[2][:4]
                    else:
                        display_box(screen, "AT LEAST 4 CARDS NEEDED", base_font, 1)
                        page = "Battle_Menu"
                elif pointer_pos == 2:
                    page = "SBattle"
                elif pointer_pos == 3:
                    page = "Menu"
            elif page == "Claim":
                if pointer_pos == 1:
                    page = "Gacha"
                elif pointer_pos == 2:
                    page = "Trade"
                elif pointer_pos == 3:
                    page = "Menu"
            elif page == "Gacha":
                if pointer_pos == 1:
                    page = "Menu"
            elif page == "Trade":
                if pointer_pos == 2:
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
                if pointer_on:
                    if battle_page == "00":
                        if not must_swap:
                            if pointer_pos == 1:
                                battle_page = "10"
                            elif pointer_pos == 2:
                                battle_page = "20"
                            elif pointer_pos == 3:
                                battle_page = "30"
                            elif pointer_pos == 4:
                                battle_page = "40"
                                pointer_pos = 2
                        else:
                            if pointer_pos == 3:
                                battle_page = "30"
                            elif pointer_pos == 4:
                                battle_page = "40"
                                pointer_pos = 2
                    elif battle_page in ("10", "20"):
                        if pointer_pos < 4:
                            selected_move = battle_page[0] + str(pointer_pos)
                        elif pointer_pos == 4:
                            pointer_pos = 1
                            battle_page = "00"
                    elif battle_page == "30":
                        if pointer_pos != 4:
                            card_idx = selected_cards.index(other_cards[pointer_pos-1])
                            if card_idx != curr_cards[player_num] and self_hps[card_idx] > 0:
                                selected_move = "3" + str(card_idx+1)
                        else:
                            pointer_pos = 1
                            battle_page = "00"
                    elif battle_page == "40":
                        if pointer_pos == 1:
                            connection.send("xL".encode())
                            page = "Battle_Menu"
                        elif pointer_pos == 2:
                            battle_page = "00"
            elif page == "Loading":
                page = "Menu"
                connection.send("exit queue".encode())
                server_messages[2] = None
            elif page == "Claim":
                if pointer_pos == 1:
                    page = "Menu"
            elif page == "Trade":
                if pointer_pos == 2:
                    page = "Menu"
            elif page == "Settings":
                if pointer_pos == 1:
                    print("credits")
                elif pointer_pos == 2:
                    page = "Menu"
            elif page == "Binder":
                if pointer_pos == 2:
                    page = "Menu"
                
                if card_zoom < 3:
                    card_zoom += 0.2
                if card_zoom >= 3:
                    card_zoom = 1
                
        

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
                    if highlight_num % 9 % 3 > 0:
                        highlight_num -= 1
                    elif highlight_num // 9 == 1:
                        highlight_num -= 7
                    elif left_page + 1 > 2:
                        left_page -= 2
                        highlight_num = 11 + highlight_num
                    if card_zoom >= 3:
                        card_zoom = 1

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
                    if highlight_num % 9 % 3 < 2:
                        highlight_num += 1
                    elif highlight_num // 9 == 0:
                        highlight_num += 7
                    elif left_page + 1 < 8:
                        left_page += 2
                        highlight_num = highlight_num % 9 - 2
                    if card_zoom >= 3:
                        card_zoom = 1

            elif page == "Choose Card":
                if pointer_pos < 4:
                    pointer_pos += 1
                if pointer_pos == 5:
                    if pointer_hover<len(userdata[2])-1: pointer_hover+=1


        if event.type == pygame.MOUSEBUTTONDOWN and page == "Gacha":
            if lever_rect.collidepoint(event.pos) and not card_visible:
                if coins >= 10:
                    coins -= 10
                    userdata[4] = coins
                    connection.send(f"k{userdata[4]}".encode())
                    
                    gacha = random.randint(1, 59)
                
                    if gacha not in cards_owned:
                        cards_owned.insert(np.searchsorted(cards_owned, gacha), gacha)
                        connection.send(f"a{gacha}".encode())
                        owned = True

                    current_card = card_images[gacha]
                    card_rect = current_card.get_rect(center=(ScreenWidth // 2, ScreenHeight // 2))
                    card_visible = True
                    #fade effect
                    alpha = 0
                    fading_in = True
                    #card display animation
                    dispalay_started = False
                    cardanim_frame = 0
                    #update animation
                    if action == 1:
                        action -= 1
                    action += 1
                    dispenser_frame = 0
                else:
                    no_coins = "NOT ENOUGH COINS"
                    no_coins_timer = pygame.time.get_ticks()
            elif card_visible and card_rect and card_rect.collidepoint(event.pos):
                #hide card if clicked
                display_started = False
                card_visible = False
                current_card = None
                card_rect = None
                card_started = False
                card_anim = 0
  



    ### HANDLE SERVER MESSAGES
    

    if page == "Start":
        pointer_on = True
        if pointer_pos > 2:
            pointer_pos = 2
        
        pointer_x = 55
        pointer_y = 257 + 70 * (pointer_pos-1)
        draw_start(screen, logo, button_login, button_signup, login_bg)
        
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
                   (text_password, text_password_rect, password_box), (text_login_bg, text_login, text_login_rect), (text_back, text_back_rect), base_font, login_bg)

        
        # check login response
        if server_messages[0] is not None:
            response = server_messages[0]
            if response == "1":
                page = "Menu"
                connection.send("get cards".encode())
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
                   (text_password, text_password_rect, password_box), (text_signup_bg, text_signup, text_signup_rect), (text_back, text_back_rect), base_font, login_bg)
        
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
        draw_menu(screen, logo, button_battle, button_binder, button_claim, button_settings, screen_bg)

    elif page == "Battle_Menu":
        if pointer_pos > 3:
            pointer_pos = 3
        
        pointer_x = 55
        pointer_y = 257 + 70 * (pointer_pos - 1)
        draw_battle_menu(screen, logo, button_multiplayer, button_singleplayer, button_exit)

    elif page == "SingleplayerMenu":
        draw_singleplayer_menu(screen)

    elif page == "SBattle":
        page = "Menu"
        # """
        # pointer pos
        # [1 2
        #  3 4]
        # """
        # if pointer_pos % 2 == 1:
        #     pointer_x = 30
        # else:
        #     pointer_x = 525
        
        # if pointer_pos <= 2:
        #     pointer_y = 435
        # else:
        #     pointer_y = 530
        # draw_battle(screen, sbattle_page, player_placeholder, enemy_placeholder, fontx3, battle_00, battle_main, pteach1)
    
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
        
        draw_choose_your_team(screen, button_exit, text_choose_your_team, text_choose_your_team_rect, text_go, text_go_bg, text_go_rect, selected_cards, base_font, card_images)

        # draw selected card pointer
        screen.blit(pointer_down, ((pointer_selected * 200)-22, 60))
        # draw hover card pointer
        if pointer_pos <= 4:
            screen.blit(pointer_up, ((pointer_pos * 200)-22, 270))
        if pointer_pos == 5:
            screen.blit(pointer_down, (478, 270))
            screen.blit(pointer_up, (478, 480))
        
        draw_card_wheel(screen, userdata[2], selected_cards, pointer_hover, base_font, small_font, card_images)

    elif page == "Loading":
        pointer_on = True
        pointer_x = 740
        pointer_y = 550
        if server_messages[2]:
            print("MATCH FOUND\n")
            page = "Match Found"
            opponent_username = None
            player_num = int(server_messages[6])-1
            opp_num = (player_num+1)%2
            timer = None
            timer_on = False
            server_messages[2] = None
        else:
            draw_loading(screen, search_glass, circle_x, circle_y, button_exit)
            toUpdate = update_circle(circle_x, circle_y, circle_angle, circle_start, 50)
            circle_x, circle_y, circle_angle, circle_start = toUpdate
    
    elif page == "Match Found":
        while (opponent_username is None):
            display_box(screen, "MATCH FOUND", base_font)
            if server_messages[3] is not None:
                if server_messages[3] == "DC":
                    display_box(screen, "OPPONENT DISCONNECTED", base_font, 3)
                    timer_on = False
                    timer = None
                    page = "Menu"
                    server_messages[3] = None
                    print("DC\n")
                elif server_messages[3][0] == "u":
                    user_datas = server_messages[3][1:].split("'")
                    opponent_username = user_datas[opp_num]
                    opponent_cards = json.loads(user_datas[opp_num+2])
                    self_hps = json.loads(user_datas[player_num + 4])
                    opp_hps = json.loads(user_datas[opp_num + 4])
                    curr_cards = [0, 0]
                    server_messages[3] = None
                    battle_page = "00"
                    game_status = None
                    other_cards = selected_cards.copy()
                    other_cards.pop(0)
                    other_cards = tuple(other_cards)
                    time.sleep(3)
                    pointer_pos = 1
                    selected_move = None
                    first_frame = False
                    names = [None, None]
                    names[player_num] = userdata[0]
                    names[(player_num+1)%2] = opponent_username
                    all_cards = [None, None]
                    all_cards[player_num] = selected_cards.copy()
                    all_cards[(player_num+1)%2] = opponent_cards
                    must_swap = False
                    actions = [None, None]
                    waiting = False
                    page = "Cut"
                    print("CUT SCENE\n")
                else:
                    print(f"Wart {server_messages[3]}")

    elif page == "Battle":
        if server_messages[3] is not None:
            game_message = server_messages[3]
            if game_message == "DC":
                display_box(screen, "OPPONENT DISCONNECTED", base_font, 3)
                timer_on = False
                timer = None
                page = "Menu"
            elif game_message[0] == "d":
                winner = int(game_message[1])
                if winner == player_num: # won
                    display_box(screen, "YOU WON", base_font, 3)
                    timer_on = False
                    timer = None
                    page = "Menu"
                else: # lost
                    display_box(screen, "YOU LOST", base_font, 3)
                    timer_on = False
                    timer = None
                    page = "Menu"

            elif game_message[0] == "g":
                if game_message[1:5] == "move":
                    game_status = "move"
                    timer_on = True
                    timer = Timer(int(server_messages[3][5:]), screen, running, base_font, (center_x, 250))
                    waiting = False
            elif game_message[0] == "m":
                parsed_msg = game_message[2:].split("'")
                if game_message[1] == "0":
                    self_action = parsed_msg[player_num]
                    opp_action = parsed_msg[opp_num]
                    actions[:] = [opp_action, opp_action]
                    actions[player_num] = self_action
                    first_to_cast = int(parsed_msg[2])
                    self_hps[:] = json.loads(parsed_msg[player_num+3])
                    opp_hps[:] = json.loads(parsed_msg[opp_num+3])
                    game_status = "animate"
                    animating = 0
                    turn = (first_to_cast, (first_to_cast+1)%2)
                    first_frame = True
                    move_num = 0
                    waiting = False
                    print(actions)
                elif game_message[1] == "1":
                    # someone died
                    dead_players = json.loads(parsed_msg[0])
                    game_status = "dead"
                    if player_num in dead_players:
                        battle_page = "30"
                    timer_on = True
                    timer = Timer(int(parsed_msg[1]), screen, running, base_font, (center_x, 250))
                elif game_message[1] == "2":
                    first_to_cast = 0
                    actions = json.loads(parsed_msg[0])
                    game_status = "animate"
                    animating = 0
                    move_num = 0
                else:
                    print(f"Unexpected server message: {game_message}")
            else:
                print(f"Wart {server_messages[3]}")
            server_messages[3] = None

        if game_status != None:
            pointer_on = not waiting
            if pointer_pos % 2 == 1:
                pointer_x = 30
            else:
                pointer_x = 525
            
            if pointer_pos <= 2:
                pointer_y = 435
            else:
                pointer_y = 530

            draw_battle(screen, battle_page, fontx3, battle_00, battle_main, teachemon_data[selected_cards[curr_cards[player_num]]-1], opponent_username, small_font, other_cards)
            screen.blit(player_placeholder, (140,135))
            screen.blit(enemy_placeholder, (700,100))
            # Teachemon Data for Current Player: teachemon_data[selected_cards[curr_cards[player_num]]-1] 
            # Teachemon Data for Opponent Player: teachemon_data[opponent_cards[curr_cards[opp_num]]-1]
            # -> Get Total HP
            p_total_hp, o_total_hp = int(teachemon_data[selected_cards[curr_cards[player_num]]-1]["HP"]), int(teachemon_data[opponent_cards[curr_cards[opp_num]]-1]["HP"])
            # Current HP: self_hps[curr_cards[player_num]], opp_hps[curr_cards[opp_num]]
            p_curr_hp, o_curr_hp = int(self_hps[curr_cards[player_num]]), int(opp_hps[curr_cards[opp_num]])
            
            # DRAW
            pygame.draw.rect(screen, (0, 0, 0), (155, 372, 200, 30)) # player hp bar background
            pygame.draw.rect(screen, (100, 255, 100), (160, 377, int(190*(p_curr_hp/p_total_hp)), 20)) # player hp bar red thing

            pygame.draw.rect(screen, (0, 0, 0), (690, 290, 200, 30)) # opponent hp bar background
            pygame.draw.rect(screen, (255, 100, 100), (695, 295, int(190*(o_curr_hp/o_total_hp)), 20)) # opponent hp bar red thing

            opp_card = base_font.render(str(opponent_cards[curr_cards[opp_num]]), True, (0, 0, 0))
            self_card = base_font.render(str(selected_cards[curr_cards[player_num]]), True, (0, 0, 0))
            opp_card_hp = base_font.render(str(opp_hps[curr_cards[opp_num]]), True, (200, 50, 50))
            self_card_hp = base_font.render(str(self_hps[curr_cards[player_num]]), True, (50, 200, 50))
            screen.blit(opp_card, (750, 120))
            screen.blit(self_card, (200, 200))
            screen.blit(opp_card_hp, (750, 170))
            screen.blit(self_card_hp, (200, 250))
            
            if game_status == "move":
                game_announcement = base_font.render("CHOOSE YOUR MOVE", True, (245, 66, 66))
                game_announcement_rect = game_announcement.get_rect(center=(center_x, 50))
                screen.blit(game_announcement, game_announcement_rect)
                selected_move_display = small_font.render(f"SELECTED {selected_move}".upper(), True, (0, 0, 0))
                screen.blit(selected_move_display, selected_move_display.get_rect(center=(center_x, center_y+50)))
                if timer_on:
                    timer.draw()
                    if timer.time == 0:
                        timer_on = False
                        # send selected move to the server
                        if selected_move is not None:
                            sent_move = ("m", "i", "s")[int(selected_move[0])-1] + str(int(selected_move[1])-1)
                        else:
                            sent_move = "n0"
                        connection.send(f"x{sent_move}".encode())
                        selected_move = None
            
            elif game_status == "animate":
                if move_num < 2:
                    source = turn[move_num]
                    if actions[source] is not None and actions[source] != "None":
                        if animating == 0:
                            source_name = names[source]
                            action_name = actions[source]
                            print(f"ANIMATING: {action_name} by PLAYER {source_name}\nMOVE NUM: {move_num}\nSOURCE NUM: {source}\nPLAYER NUM: {player_num}")
                            display_box(screen, f"{source_name} {action_name}".upper(), base_font, 2)
                            animating = 1
                            player_img_pos = (140, 135)
                            opp_img_pos = (700, 100)
                            animation_bg_pos = (-1000, -600)
                            battle_page = "00"
                            bounce_out = True
                            is_self = False
                            frame = 0
                            if action_name[0] == "m":
                                card_num = selected_cards[curr_cards[player_num]] if source == player_num else opponent_cards[curr_cards[source]]
                                data = teachemon_data[card_num-1]
                                move_info = (source_name.upper(), data["Name"].upper(), data[f"Move {int(action_name[1]) + 1} Name"].upper(), data[f"Move {int(action_name[1]) + 1} Damage"].upper())
                                scene = 0
                                print_delay = 3
                            if source == player_num:
                                is_self = True
                            print()
                        
                        elif animating == 1:
                            if action_name[0] == "s":
                                """
                                image = 240x240
                                initial pos:
                                - player: (140, 135)
                                - opponent: (700, 100)
                                """
                                if bounce_out:
                                    if is_self:
                                        player_img_pos = (player_img_pos[0] - 10, player_img_pos[1])
                                        if player_img_pos[0] <= -240:
                                            bounce_out = False
                                    else:
                                        opp_img_pos = (opp_img_pos[0] + 10, opp_img_pos[1])
                                        if opp_img_pos[0] >= 1000:
                                            bounce_out = False
                                else:
                                    if is_self:
                                        player_img_pos = (player_img_pos[0] + 10, player_img_pos[1])
                                        if player_img_pos[0] >= 140:
                                            animating = 2
                                    else:
                                        opp_img_pos = (opp_img_pos[0] - 10, opp_img_pos[1])
                                        if opp_img_pos[0] <= 700:
                                            animating = 2
                                

                                draw_battle(screen, battle_page, fontx3, battle_00, battle_main, teachemon_data[selected_cards[curr_cards[player_num]]-1], opponent_username, small_font, other_cards)
                                screen.blit(player_placeholder, player_img_pos)
                                screen.blit(enemy_placeholder, opp_img_pos)
                            elif action_name[0] == "m":
                                screen.blit(animation_bg, animation_bg_pos)
                                if animation_bg_pos[0] < 0:
                                    animation_bg_pos = (animation_bg_pos[0] + 50, animation_bg_pos[1] + 30)
                                else:
                                    """
                                    Background fully animated -> Need to display:
                                    - Player Name
                                    - Teachemon Name
                                    - Ability Name
                                    - Damage
                                    """
                                    if scene >= 0:
                                        if scene == 0:
                                            if (frame//print_delay <= len(move_info[0])):
                                                name = base_font.render(move_info[0][:frame//print_delay], True, (0, 0, 0))
                                            else:
                                                name = base_font.render(move_info[0], True, (0, 0, 0))
                                                if frame//print_delay - len(move_info[0]) == 2:
                                                    scene += 1
                                                    frame = 0
                                        else:
                                            name = base_font.render(move_info[0], True, (0, 0, 0))
                                        screen.blit(name, (100, 100))
                                    if scene >= 1:
                                        if scene == 1:
                                            if (frame//print_delay <= len(move_info[1])):
                                                tname = base_font.render(move_info[1][:frame//print_delay], True, (0, 0, 0))
                                            else:
                                                tname = base_font.render(move_info[1], True, (0, 0, 0))
                                                if frame//print_delay - len(move_info[1]) == 2:
                                                    scene += 1
                                                    frame = 0
                                        else:
                                            tname = base_font.render(move_info[1], True, (0, 0, 0))
                                        screen.blit(tname, (250, 200))
                                    if scene >= 2:
                                        if scene == 2:
                                            if (frame//print_delay <= len(move_info[2])):
                                                ability = base_font.render(move_info[2][:frame//print_delay], True, (0, 0, 0))
                                            else:
                                                ability = base_font.render(move_info[2], True, (0, 0, 0))
                                                if frame//print_delay - len(move_info[2]) == 2:
                                                    scene += 1
                                                    frame = 0
                                        else:
                                            ability = base_font.render(move_info[2], True, (0, 0, 0))
                                        screen.blit(ability, (400, 300))
                                    if scene >= 3:
                                        if scene == 3:
                                            if (frame//print_delay <= len(move_info[3])):
                                                damage = base_font.render(move_info[3][:frame//print_delay], True, (0, 0, 0))
                                            else:
                                                damage = base_font.render(move_info[3], True, (0, 0, 0))
                                                if frame//print_delay - len(move_info[3]) == 2:
                                                    scene += 1
                                                    frame = 0
                                        else:
                                            damage = base_font.render(move_info[3], True, (0, 0, 0))
                                        screen.blit(damage, (550, 400))
                                    if scene > 3:
                                        if frame >= 24*2:
                                            animating = 2
                                    frame += 1
                            else:
                                animating = 2

                        elif animating == 2:
                            animating = 0
                            if action_name[0] == "s":
                                curr_cards[source] = int(action_name[1])
                                if source == player_num:
                                    other_cards = selected_cards.copy()
                                    other_cards.remove(selected_cards[curr_cards[player_num]])
                                    other_cards = tuple(other_cards)
                            move_num += 1
                    else:
                        move_num+=1
                else:
                    connection.send("xanicomp".encode())
                    game_status = "waiting"
                if first_frame:
                    first_fame = False
            
            elif game_status == "dead":
                if timer_on:
                    timer.draw()
                    if timer.time == 0:
                        timer_on = False
                if player_num in dead_players:
                    game_announcement = base_font.render("SWAP YOUR TEACHEMON", True, (245, 66, 66))
                    game_announcement_rect = game_announcement.get_rect(center=(center_x, 200))
                    screen.blit(game_announcement, game_announcement_rect)
                    must_swap = True
                    if timer.time == 0:
                        # send selected move to the server
                        if selected_move is not None:
                            sent_move = ("n", "n", "s")[int(selected_move[0])-1] + str(int(selected_move[1])-1)
                        else:
                            sent_move = "n0"
                        connection.send(f"x{sent_move}".encode())
                        selected_move = None
                else:
                    game_announcement = base_font.render("WAITING FOR OPPONENT", True, (245, 66, 66))
                    game_announcement_rect = game_announcement.get_rect(center=(center_x, 200))
                    screen.blit(game_announcement, game_announcement_rect)
                    waiting = True
                
                if timer.time == 0:
                    game_status = "waiting"
            
            elif game_status == "waiting":
                display_box(screen, "WAITING", base_font)

        else:
            display_box(screen, "GAME STARTING", base_font)

        
    elif page == "Binder":
        pointer_x = 750
        pointer_y = 550
        if pointer_pos == 2:
            pointer_on = True
        else:
            pointer_on = False
        if card_zoom > 1 and card_zoom <= 3:
            card_zoom += 0.2
        draw_binder(screen, left_page, left_page + 1, resized_binder, fontx1, card_images, cards_owned, card_back, button_exit, card_zoom, binder_highlight, highlight_num, teachemon_data)
        

        
        
        # if highlight_num < 9:
        #    screen.blit(binder_highlight, (150 + highlight_num%3*95, 100 + highlight_num//3*135))
        # else:
        #    screen.blit(binder_highlight, (570 + (highlight_num-9)%3*95, 100 + (highlight_num-9)//3*135))

        # for future - making card bigger when pressed enter 
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not pointer_pos == 2:
            #screen.blit(base_font.render(str(highlight_num), True, (0, 0, 0)), (300, 300))


    elif page == "Claim":
        if pointer_pos > 3:
            pointer_pos = 3
        
        pointer_x = 55
        pointer_y = 257 + 70 * (pointer_pos - 1)        
        draw_claim_menu(screen, logo, big_font.render("GACHA", True, (0, 0, 0)), big_font.render("TRADE", True, (0, 0, 0)), big_font.render("EXIT", True, (0, 0, 0)))
    
    elif page == "Gacha":
        pointer_on = True
        pointer_pos = 1
        pointer_x = 740
        pointer_y = 550
        draw_claim(screen, button_exit, font, coins, animation_list, dispenser_frame, action, card_visible, current_card, card_rect, screen_bg, resized_coin,
                   alpha, card_started, card_anim, max_cardanim, fade_started,
                   cardanim_list, cardanim_frame, display_started, no_coins, no_coins_duration, no_coins_timer, owned, big_font)
        current_time = pygame.time.get_ticks()

        if card_visible:
            if fading_in:
                alpha += fade_speed
                if alpha >= 170:
                    alpha = 170              
                    fading_in = False 
                    card_started = True
                    card_anim = 0
        if display_started:
            if current_time - last_update >= cardanim_cooldown:
                cardanim_frame += 1
                last_update = current_time
                if cardanim_frame >= len(cardanim_list):  #reset animation if it reaches the last frame
                    cardanim_frame = 0
        
        if card_started:
            card_anim += 1
            if card_anim >= max_cardanim:
                card_anim = max_cardanim
                display_started = True

        if current_time - last_update >= anim_cooldown:
            dispenser_frame += 1
            last_update = current_time
            if dispenser_frame == 11:
                action = (action + 1) % len(animation_list)
                #fade_started = True
                dispenser_frame = 0          
            elif dispenser_frame >= len(animation_list[action]):
                dispenser_frame = 0
    
    elif page == "Trade":
        pointer_x = 750
        pointer_y = 550
        if pointer_pos == 2:
            pointer_on = True
        else:
            pointer_on = False
        draw_trade(screen, cards_owned, card_images, button_exit, big_font, binder_highlight, pointer_up)
    
    elif page == "Cut":
        pointer_on = False
        draw_cut(screen, button_exit, fontx3, cut_scene_animation, cut_scene_frame, vs_bg, main_screen_bg, userdata[0], opponent_username)
        
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= cut_scene_cooldown:
            if cut_scene_frame == 32:
                pygame.time.wait(1500)
                cut_scene_frame = 0
                page = "Battle"
                connection.send("xCONNECTED".encode())
            else:
                cut_scene_frame += 1
                last_update = current_time
            
       
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
