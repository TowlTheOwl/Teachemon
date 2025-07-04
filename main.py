#Import and Initialize PyGame and math
import json
import pygame
from sb3_contrib import MaskablePPO
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
from AI.battleEnv import BattleGymEnv

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
hong = pygame.image.load("Images/hong.png")
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
dispenser = pygame.image.load("Images/singleDispenser.png")
resized_dispenser = pygame.transform.scale(dispenser, (500, 300))
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

#sfx

volume = 50  
select_sfx = pygame.mixer.Sound("SFx/select.wav")
dispense_sfx = pygame.mixer.Sound("SFX/dispense.wav")
page_turn_sfx = pygame.mixer.Sound("SFX/paperSlide.wav")
card_zoom_sfx = pygame.mixer.Sound("SFx/pageTurn.wav")
no_coins_sfx = pygame.mixer.Sound("SFX/noCoins.wav")
new_card_sfx = pygame.mixer.Sound("SFX/new.wav")
owned_card_sfx = pygame.mixer.Sound("SFX/owned.wav")
coins_sfx = pygame.mixer.Sound("SFX/coins.mp3")

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
# variable to determine what to transition to after the cut scene
cut_to = 1
trade_success = False

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

coins = 50
selected_cards = [None, None, None, None]
userdata = [username, password, [], selected_cards, 50] # username, password, owned cards, selected cards
cards_owned = userdata[2]
must_swap = False
opponent_username = None

# for trading - players can only trade with other players who are also on the trade page b/c live trading
# similar to finding an opponent to battle but instead finding all the possible trade players
available_players = []

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
                if pointer_pos < 4:
                    pointer_pos += 1
            elif page == "Choose Trade Card":
                if pointer_pos < 2:
                    pointer_on = True
                    pointer_pos += 1
            # replace this next sprint (?), rn cut scene to view trade is triggered by pressing the DOWN button 
            # but once server connection is implemented, cut scene will be triggered once the other players selects their card
            elif page == "Trade Loading":
                page = "Cut"     
                cut_to = 3 
            
            elif page == "View Trade":
                if pointer_pos < 2:
                    pointer_pos += 1
            
            elif page == "SinglePlayerMenu":
                if pointer_pos < 3:
                    pointer_pos += 1
            
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
                if pointer_pos > 1:
                    pointer_pos -= 1
            elif page == "View Trade":
                if pointer_pos > 1:
                    pointer_pos -= 1
                    
            # replace this next sprint (?), rn cut scene is triggered by pressing the UP button 
            # but once server connection is implemented, cut scene will be triggered once the other players selects this player (must match)
            elif page == "Trade Loading":
                page = "Cut"     
                cut_to = 2 
            elif page == "Choose Trade Card":
                if pointer_pos > 1:
                    pointer_on = False
                    pointer_pos -= 1                    

            else:
                if pointer_pos > 1:
                    pointer_pos -= 1


        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            keep_pointer = False
            select_sfx.play()
            select_sfx.set_volume(volume/100)
            
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
                    page = "SinglePlayerMenu"
                elif pointer_pos == 3:
                    page = "Menu"
            elif page == "SinglePlayerMenu":
                bot_mode = pointer_pos-1
                page = "SBattle"
                sbattle_page = "00"
                env = BattleGymEnv()
                model_dirs = ("AI/easy.zip", "AI/medium.zip", "AI/hard.zip")
                enemy_model = MaskablePPO.load(model_dirs[bot_mode], env=env)
                bot_names = ("EASY BOT", "MEDIUM BOT", "HARD BOT")
                bot_name = bot_names[bot_mode]

                game_state = 0
                user_action = None
                obs, _ = env.reset()

                player_cards, bot_cards = env.get_cards()
                player_obs = env._get_observation(0)
                curr_card = -1
                for i in range(4):
                    if (player_obs[i]):
                        curr_card = i
                curr_energy = [int(i*10) for i in player_obs[8:12]]
                curr_hp = [int(i*100) for i in player_obs[4:8]]

                print(f"curr_energy: {curr_energy}")
                print(f"curr_hp: {curr_hp}")
                
                other_cards = player_cards.copy()
                other_cards.pop(curr_card)
                other_cards = tuple(other_cards)

                bot_obs = env._get_observation(1)
                bot_curr_card = -1
                for i in range(4):
                    if (bot_obs[i]):
                        bot_curr_card = i
                bot_curr_energy = [int(i*10) for i in bot_obs[8:12]]
                bot_curr_hp = [int(i*100) for i in bot_obs[4:8]]

                selected_move = None
                done = False


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
                if pointer_pos == 4:
                    page = "Menu"
                else: 
                    page = "Trade Loading"
                    keep_pointer = True
            elif page == "Choose Trade Card":
                if pointer_pos == 2:
                    page = "Trade Loading"
            elif page == "View Trade":
                page = "Trade Result"
                if pointer_pos == 1:
                    trade_success = True
                elif pointer_pos == 2:
                    trade_success = False
            elif page == "Trade Result":
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
                if pointer_on:
                    if sbattle_page == "00":
                        if not must_swap:
                            if pointer_pos == 1:
                                sbattle_page = "10"
                            elif pointer_pos == 2:
                                sbattle_page = "20"
                            elif pointer_pos == 3:
                                sbattle_page = "30"
                            elif pointer_pos == 4:
                                sbattle_page = "40"
                                pointer_pos = 2
                        else:
                            if pointer_pos == 3:
                                sbattle_page = "30"
                            elif pointer_pos == 4:
                                sbattle_page = "40"
                                pointer_pos = 2
                    elif sbattle_page in ("10", "20"):
                        if pointer_pos < 4:
                            if sbattle_page == "10":
                                # check whether the player has enough energy to use the move
                                if curr_energy[curr_card] >= int(teachemon_data[player_cards[curr_card]-1][f"Move {pointer_pos} Cost"]):
                                    selected_move = sbattle_page[0] + str(pointer_pos)
                                else:
                                    display_box(screen, "NOT ENOUGH ENERGY", base_font, 1)
                            else:
                                selected_move = sbattle_page[0] + str(pointer_pos)
                        elif pointer_pos == 4:
                            pointer_pos = 1
                            sbattle_page = "00"
                    elif sbattle_page == "30":
                        if pointer_pos != 4:
                            card_idx = player_cards.index(other_cards[pointer_pos-1])
                            if card_idx != curr_card and curr_hp[card_idx] > 0:
                                selected_move = "3" + str(card_idx+1)
                        else:
                            pointer_pos = 1
                            sbattle_page = "00"
                    elif sbattle_page == "40":
                        if pointer_pos == 1:
                            page = "Menu"
                        elif pointer_pos == 2:
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
                            if battle_page == "10":
                                # check whether the player has enough energy to use the move
                                if energy[curr_cards[player_num]] > int(teachemon_data[selected_cards[curr_cards[player_num]]-1][f"Move {pointer_pos} Cost"]):
                                    selected_move = battle_page[0] + str(pointer_pos)
                                else:
                                    display_box(screen, "NOT ENOUGH ENERGY", base_font, 1)
                            else:
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
                page = "Menu"
            elif page == "Settings":
                if pointer_pos == 1:
                    draw_credits(screen, button_exit, fontx1, hong)
                elif pointer_pos == 2:
                    page = "Volume"
                    slider_x = 200
                    slider_y = 300
                    slider_width = 600
                    slider_height = 100
                    target_volume = volume
                elif pointer_pos == 3:
                    page = "Menu"
            elif page == "Volume":
                page = "Settings"
            elif page == "Binder":
                if pointer_pos == 2:
                    page = "Menu"
                
                if card_zoom < 3:
                    card_zoom += 0.2
                    card_zoom_sfx.play()
                    card_zoom_sfx.set_volume(volume/100)
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
                        page_turn_sfx.play()
                        page_turn_sfx.set_volume(volume/100)
                    if card_zoom >= 3:
                        card_zoom = 1

            elif page == "Choose Card":
                if pointer_pos <= 4 and pointer_pos > 1:
                    pointer_pos -= 1
                if pointer_pos == 5:
                    if pointer_hover>0: pointer_hover-=1

            elif page == "Choose Trade Card":
                if pointer_hover>0: pointer_hover-=1

            elif page == "Volume":
                target_volume = max(target_volume - 5, 0)


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
                        page_turn_sfx.play()
                        page_turn_sfx.set_volume(volume/100)
                    if card_zoom >= 3:
                        card_zoom = 1

            elif page == "Choose Card":
                if pointer_pos < 4:
                    pointer_pos += 1
                if pointer_pos == 5:
                    if pointer_hover<len(userdata[2])-1: pointer_hover+=1
                        
            elif page == "Volume":
                target_volume = min(target_volume + 5, 100)
                
            elif page == "Trade":
                if pointer_pos < 4:
                    pointer_pos = 4

            elif page == "Choose Trade Card":
                if pointer_hover<len(userdata[2])-1: pointer_hover+=1

        if event.type == pygame.MOUSEBUTTONDOWN and page == "Gacha":
            if lever_rect.collidepoint(event.pos) and not card_visible:
                if coins >= 10:
                    coins_sfx.play()
                    coins_sfx.set_volume(volume/100)

                    dispense_sfx.play()
                    dispense_sfx.set_volume(volume/100)
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
                    no_coins_sfx.play()
                    no_coins_sfx.set_volume(volume/100)
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
                connection.send("get coins".encode())
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

    elif page == "SinglePlayerMenu":
        pointer_on = True
        pointer_x = 20
        
        pointer_y = 150 * pointer_pos + 45
        draw_singleplayer_menu(screen, base_font, big_font)

    elif page == "SBattle":
        if not done:
            
            """
            game states
            0: waiting for user input
            1: calculating bot action
            2: animating
            """
            if game_state == 0:
                if pointer_pos % 2 == 1:
                    pointer_x = 30
                else:
                    pointer_x = 525
                
                if pointer_pos <= 2:
                    pointer_y = 435
                else:
                    pointer_y = 530

                # wait for user action
                draw_battle(
                    screen, 
                    sbattle_page, 
                    fontx3, 
                    battle_00, 
                    battle_main, 
                    teachemon_data[player_cards[curr_card]-1], 
                    bot_name,
                    small_font, 
                    other_cards
                )

                screen.blit(player_placeholder, (140,135))
                screen.blit(enemy_placeholder, (700,100))
                # Teachemon Data for Current Player: teachemon_data[selected_cards[curr_cards[player_num]]-1] 
                # Teachemon Data for Opponent Player: teachemon_data[opponent_cards[curr_cards[opp_num]]-1]
                # -> Get Total HP
                curr_card_data = teachemon_data[player_cards[curr_card]-1]
                # p_total_hp, o_total_hp = int(teachemon_data[player_cards[curr_card]-1]["HP"]), int(teachemon_data[bot_cards[bot_curr_card]-1]["HP"])
                p_total_hp = o_total_hp = 100
                # Current HP: self_hps[curr_cards[player_num]], opp_hps[curr_cards[opp_num]]
                p_curr_hp, o_curr_hp = int(curr_hp[curr_card]), int(bot_curr_hp[bot_curr_card])
                
                # DRAW
                pygame.draw.rect(screen, (0, 0, 0), (155, 372, 200, 30)) # player hp bar background
                pygame.draw.rect(screen, (100, 255, 100), (160, 377, int(190*(p_curr_hp/p_total_hp)), 20)) # player hp bar red thing

                pygame.draw.rect(screen, (0, 0, 0), (690, 290, 200, 30)) # opponent hp bar background
                pygame.draw.rect(screen, (255, 100, 100), (695, 295, int(190*(o_curr_hp/o_total_hp)), 20)) # opponent hp bar red thing

                opp_card = base_font.render(str(bot_cards[bot_curr_card]), True, (0, 0, 0))
                self_card = base_font.render(str(player_cards[curr_card]), True, (0, 0, 0))
                opp_card_hp = base_font.render(str(bot_curr_hp[bot_curr_card]), True, (200, 50, 50))
                self_card_hp = base_font.render(str(curr_hp[curr_card]), True, (50, 200, 50))
                screen.blit(opp_card, (750, 120))
                screen.blit(self_card, (200, 200))
                screen.blit(opp_card_hp, (750, 170))
                screen.blit(self_card_hp, (200, 250))

                if sbattle_page[0] == "1" and pointer_pos < 4:
                    # display info about the move
                    # Damage, Cost, Speed
                    text_damage = base_font.render("DAMAGE", True, (0, 0, 0))
                    damage_value_text = small_font.render(str(curr_card_data[f"Move {pointer_pos} Damage"]), True, (0, 0, 0))
                    text_cost = base_font.render("COST", True, (0, 0, 0))
                    cost_value_text = small_font.render(str(curr_card_data[f"Move {pointer_pos} Cost"]), True, (0, 0, 0))
                    text_speed = base_font.render("SPEED", True, (0, 0, 0))
                    speed_value_text = small_font.render(str(curr_card_data[f"Move {pointer_pos} Speed"]), True, (0, 0, 0))
                    pygame.draw.rect(screen, (200, 200, 255), (360, 150, 300, 260)) # screen size: 1000 x 600
                    screen.blit(text_damage, (400, 170))
                    screen.blit(damage_value_text, (420, 210))
                    screen.blit(text_cost, (400, 250))
                    screen.blit(cost_value_text, (420, 290))
                    screen.blit(text_speed, (400, 340))
                    screen.blit(speed_value_text, (420, 380))

                game_announcement = base_font.render("CHOOSE YOUR MOVE", True, (245, 66, 66))
                game_announcement_rect = game_announcement.get_rect(center=(center_x, 50))
                screen.blit(game_announcement, game_announcement_rect)
                energy_display = small_font.render(f"ENERGY {curr_energy[curr_card]}", True, (0, 0, 0))
                screen.blit(energy_display, energy_display.get_rect(center=(center_x, center_y-200)))
                # self_effects_display = small_font.render(f"EFFECTS {self_effect[0]} {self_effect[1]}", True, (0, 0, 0))
                # opp_effects_display = small_font.render(f"EFFECTS {opp_effect[0]} {opp_effect[1]}", True, (0, 0, 0))
                # screen.blit(self_effects_display, self_effects_display.get_rect(center=(center_x-250, center_y+50)))
                # screen.blit(opp_effects_display, opp_effects_display.get_rect(center=(center_x+300, center_y+50)))


                if (selected_move is not None and selected_move[1] != "0"):
                    game_state = 1
            elif game_state == 1:
                # calculate user action and animation
                mask = env.get_action_mask(1)
                bot_action, _ = enemy_model.predict(env._get_observation(1), action_masks=mask)
                
                user_action = (int(selected_move[0])-1) * 3 + int(selected_move[1]) - 1
                final_actions = (user_action, bot_action)
                obs, reward, done, truncated, info= env.step(final_actions)

                # update observation
                player_obs = env._get_observation(0)
                curr_card = -1
                for i in range(4):
                    if (player_obs[i]):
                        curr_card = i
                curr_energy = [int(i*10) for i in player_obs[8:12]]
                curr_hp = [int(i*100) for i in player_obs[4:8]]

                other_cards = player_cards.copy()
                other_cards.pop(curr_card)
                other_cards = tuple(other_cards)

                bot_obs = env._get_observation(1)
                bot_curr_card = -1
                for i in range(4):
                    if (bot_obs[i]):
                        bot_curr_card = i
                bot_curr_energy = [int(i*10) for i in bot_obs[8:12]]
                bot_curr_hp = [int(i*100) for i in bot_obs[4:8]]

                
                if curr_hp[curr_card] <= 0:
                    must_swap = True
                else:
                    must_swap = False

                sbattle_page = "00"
                selected_move = None
                game_state = 2  # animate
                animating = 0
                animation_idx = 0
            else: # animation
                if animation_idx < 2:
                    if animating == 0:
                        if animation_idx == len(env.cast_order):
                            animation_idx += 1
                            continue
                        casting = env.cast_order[animation_idx]
                        if casting == 0:
                            source_name = userdata[0]
                        else:
                            source_name = bot_name
                        
                        if final_actions[casting] < 3: # 0 - 2: ability
                            action_name = f"m{final_actions[casting]}"
                        elif final_actions[casting] < 6: # 3, 4, 5: items
                            action_name = f"i{final_actions[casting]-3}"
                        else: # swap
                            action_name = f"s{final_actions[casting]-6}"

                        print(f"ANIMATING: {action_name} by {source_name}\nMOVE NUM: {animation_idx}\nSOURCE NUM: {casting}")
                        # display_box(screen, f"{source_name} {action_name}".upper(), base_font, 2)
                        animating = 1
                        player_img_pos = (140, 135)
                        opp_img_pos = (700, 100)
                        animation_bg_pos = (-1000, -600)
                        bounce_out = True
                        is_self = False
                        frame = 0
                        if action_name[0] == "m":
                            card_num = player_cards[curr_card] if casting == 0 else bot_cards[bot_curr_card]
                            data = teachemon_data[card_num-1]
                            move_info = (source_name.upper(), data["Name"].upper(), data[f"Move {int(action_name[1]) + 1} Name"].upper(), data[f"Move {int(action_name[1]) + 1} Damage"].upper())
                            scene = 0
                            print_delay = 1
                        elif action_name[0] == "i":
                            card_num = player_cards[curr_card] if casting == 0 else bot_cards[bot_curr_card]
                            data = teachemon_data[card_num-1]
                            potion_names = ("Attack Potion", "Defense Potion", "Energy Potion")
                            item_info = (source_name.upper(), data["Name"].upper(), potion_names[int(action_name[1])].upper())
                            scene = 0
                            print_delay = 1
                        if casting == 0:
                            is_self = True
                    
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
                            

                            draw_battle(
                                screen, 
                                sbattle_page, 
                                fontx3, 
                                battle_00, 
                                battle_main, 
                                teachemon_data[player_cards[curr_card]-1], 
                                bot_name,
                                small_font, 
                                other_cards
                            )                            
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
                        elif action_name[0] == "i":
                            screen.blit(animation_bg, animation_bg_pos)
                            if animation_bg_pos[0] < 0:
                                animation_bg_pos = (animation_bg_pos[0] + 50, animation_bg_pos[1] + 30)
                            else:
                                """
                                Background fully animated -> Need to display:
                                - Player Name
                                - Teachemon Name
                                - Item Name
                                """
                                if scene >= 0:
                                    if scene == 0:
                                        if (frame//print_delay <= len(item_info[0])):
                                            name = base_font.render(item_info[0][:frame//print_delay], True, (0, 0, 0))
                                        else:
                                            name = base_font.render(item_info[0], True, (0, 0, 0))
                                            if frame//print_delay - len(item_info[0]) == 2:
                                                scene += 1
                                                frame = 0
                                    else:
                                        name = base_font.render(item_info[0], True, (0, 0, 0))
                                    screen.blit(name, (100, 100))
                                if scene >= 1:
                                    if scene == 1:
                                        if (frame//print_delay <= len(item_info[1])):
                                            tname = base_font.render(item_info[1][:frame//print_delay], True, (0, 0, 0))
                                        else:
                                            tname = base_font.render(item_info[1], True, (0, 0, 0))
                                            if frame//print_delay - len(item_info[1]) == 2:
                                                scene += 1
                                                frame = 0
                                    else:
                                        tname = base_font.render(item_info[1], True, (0, 0, 0))
                                    screen.blit(tname, (250, 200))
                                if scene >= 2:
                                    if scene == 2:
                                        if (frame//print_delay <= len(item_info[2])):
                                            item = base_font.render(item_info[2][:frame//print_delay], True, (0, 0, 0))
                                        else:
                                            item = base_font.render(item_info[2], True, (0, 0, 0))
                                            if frame//print_delay - len(item_info[2]) == 2:
                                                scene += 1
                                                frame = 0
                                    else:
                                        item = base_font.render(item_info[2], True, (0, 0, 0))
                                    screen.blit(item, (400, 300))
                                if scene > 2:
                                    if frame >= 24*2:
                                        animating = 2
                                frame += 1

                                
                        else:
                            animating = 2

                    elif animating == 2:
                        animating = 0
                        animation_idx+=1
                else:
                    game_state = 0
        else:
            # find out whether the player won, display, add coins if won
            if not any([hp>0 for hp in curr_hp]):
                display_box(screen, "YOU WON", big_font, 3)
            else:
                display_box(screen, "YOU LOST", big_font, 3)
            
            page = "Menu"
    
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
        
        draw_choose_your_team(screen, button_exit, text_choose_your_team, text_choose_your_team_rect, text_go, text_go_bg, text_go_rect, selected_cards, pygame.font.Font("Teachemon.ttf", 6), card_images, teachemon_data)
        # draw selected card pointer
        screen.blit(pointer_down, ((pointer_selected * 180)+30, 60))
        # draw hover card pointer
        if pointer_pos <= 4:
            screen.blit(pointer_up, ((pointer_pos * 180)+30, 270))
        if pointer_pos == 5:
            screen.blit(pointer_down, (478, 280))
            screen.blit(pointer_up, (478, 490))
        
        draw_card_wheel(screen, userdata[2], selected_cards, pointer_hover, base_font, pygame.font.Font("Teachemon.ttf", 6), card_images, teachemon_data)
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
                    # initialize variables for the game
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
                    energy = [10, 10, 10, 10]
                    self_effect = [0, 0]
                    opp_effect = [0, 0]
                    waiting = False

                    
                    time.sleep(3)
                    pointer_pos = 1
                    page = "Cut"
                    cut_to = 1
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
                    if self_hps[curr_cards[player_num]] <= 0:
                        game_status = "dead"
                        battle_page = "30"
                    else:
                        game_status = "move"
                    timer_on = True
                    timer = Timer(int(server_messages[3][5:]), screen, running, base_font, (50, 50))
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
                    timer = Timer(int(parsed_msg[1]), screen, running, base_font, (50, 50))
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
            p_total_hp = o_total_hp = 100
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
                screen.blit(selected_move_display, selected_move_display.get_rect(center=(center_x, center_y+70)))
                energy_display = small_font.render(f"ENERGY {energy[curr_cards[player_num]]}", True, (0, 0, 0))
                screen.blit(energy_display, energy_display.get_rect(center=(center_x, center_y-200)))
                self_effects_display = small_font.render(f"EFFECTS {self_effect[0]} {self_effect[1]}", True, (0, 0, 0))
                opp_effects_display = small_font.render(f"EFFECTS {opp_effect[0]} {opp_effect[1]}", True, (0, 0, 0))
                screen.blit(self_effects_display, self_effects_display.get_rect(center=(center_x-250, center_y+50)))
                screen.blit(opp_effects_display, opp_effects_display.get_rect(center=(center_x+300, center_y+50)))
                must_swap = False

                if battle_page[0] == "1" and pointer_pos < 4:
                    curr_card_data = teachemon_data[selected_cards[curr_cards[player_num]]-1]
                    # display info about the move
                    # Damage, Cost, Speed
                    text_damage = base_font.render("DAMAGE", True, (0, 0, 0))
                    damage_value_text = small_font.render(str(curr_card_data[f"Move {pointer_pos} Damage"]), True, (0, 0, 0))
                    text_cost = base_font.render("COST", True, (0, 0, 0))
                    cost_value_text = small_font.render(str(curr_card_data[f"Move {pointer_pos} Cost"]), True, (0, 0, 0))
                    text_speed = base_font.render("SPEED", True, (0, 0, 0))
                    speed_value_text = small_font.render(str(curr_card_data[f"Move {pointer_pos} Speed"]), True, (0, 0, 0))
                    pygame.draw.rect(screen, (200, 200, 255), (360, 150, 300, 260)) # screen size: 1000 x 600
                    screen.blit(text_damage, (400, 170))
                    screen.blit(damage_value_text, (420, 210))
                    screen.blit(text_cost, (400, 250))
                    screen.blit(cost_value_text, (420, 290))
                    screen.blit(text_speed, (400, 340))
                    screen.blit(speed_value_text, (420, 380))

                if timer_on:
                    timer.draw()
                    if timer.time == 0:
                        timer_on = False
                        # send selected move to the server
                        if selected_move is not None:
                            sent_move = ("m", "i", "s")[int(selected_move[0])-1] + str(int(selected_move[1])-1)
                            if sent_move[0] == "m":
                                energy[curr_cards[player_num]] -= int(teachemon_data[selected_cards[curr_cards[player_num]]-1][f"Move {selected_move[1]} Cost"])
                        else:
                            sent_move = "n0"
                        connection.send(f"x{sent_move}".encode())
                        selected_move = None
                        game_status = "waiting"
            
            elif game_status == "dead":                
                game_announcement = base_font.render("SWAP YOUR TEACHEMON", True, (245, 66, 66))
                game_announcement_rect = game_announcement.get_rect(center=(center_x, 200))
                screen.blit(game_announcement, game_announcement_rect)
                selected_move_display = small_font.render(f"SELECTED {selected_move}".upper(), True, (0, 0, 0))
                screen.blit(selected_move_display, selected_move_display.get_rect(center=(center_x, center_y+70)))
                energy_display = small_font.render(f"ENERGY {energy[curr_cards[player_num]]}", True, (0, 0, 0))
                screen.blit(energy_display, energy_display.get_rect(center=(center_x, center_y-200)))
                self_effects_display = small_font.render(f"EFFECTS {self_effect[0]} {self_effect[1]}", True, (0, 0, 0))
                opp_effects_display = small_font.render(f"EFFECTS {opp_effect[0]} {opp_effect[1]}", True, (0, 0, 0))
                screen.blit(self_effects_display, self_effects_display.get_rect(center=(center_x-250, center_y+50)))
                screen.blit(opp_effects_display, opp_effects_display.get_rect(center=(center_x+300, center_y+50)))
                must_swap = True

                if timer_on:
                    timer.draw()
                    if timer.time == 0:
                        timer_on = False
                        # send selected move to the server
                        if selected_move is not None:
                            sent_move = ("m", "i", "s")[int(selected_move[0])-1] + str(int(selected_move[1])-1)
                            if sent_move[0] == "m":
                                energy[curr_cards[player_num]] -= int(teachemon_data[selected_cards[curr_cards[player_num]]-1][f"Move {selected_move[1]} Cost"])
                        else:
                            sent_move = "n0"
                        connection.send(f"x{sent_move}".encode())
                        selected_move = None
                        game_status = "waiting"
                
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
                                print_delay = 1
                            elif action_name[0] == "i":
                                card_num = selected_cards[curr_cards[player_num]] if source == player_num else opponent_cards[curr_cards[source]]
                                data = teachemon_data[card_num-1]
                                potion_names = ("Attack Potion", "Defense Potion", "Energy Potion")
                                item_info = (source_name.upper(), data["Name"].upper(), potion_names[int(action_name[1])].upper())
                                scene = 0
                                print_delay = 1
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
                            elif action_name[0] == "i":
                                screen.blit(animation_bg, animation_bg_pos)
                                if animation_bg_pos[0] < 0:
                                    animation_bg_pos = (animation_bg_pos[0] + 50, animation_bg_pos[1] + 30)
                                else:
                                    """
                                    Background fully animated -> Need to display:
                                    - Player Name
                                    - Teachemon Name
                                    - Item Name
                                    """
                                    if scene >= 0:
                                        if scene == 0:
                                            if (frame//print_delay <= len(item_info[0])):
                                                name = base_font.render(item_info[0][:frame//print_delay], True, (0, 0, 0))
                                            else:
                                                name = base_font.render(item_info[0], True, (0, 0, 0))
                                                if frame//print_delay - len(item_info[0]) == 2:
                                                    scene += 1
                                                    frame = 0
                                        else:
                                            name = base_font.render(item_info[0], True, (0, 0, 0))
                                        screen.blit(name, (100, 100))
                                    if scene >= 1:
                                        if scene == 1:
                                            if (frame//print_delay <= len(item_info[1])):
                                                tname = base_font.render(item_info[1][:frame//print_delay], True, (0, 0, 0))
                                            else:
                                                tname = base_font.render(item_info[1], True, (0, 0, 0))
                                                if frame//print_delay - len(item_info[1]) == 2:
                                                    scene += 1
                                                    frame = 0
                                        else:
                                            tname = base_font.render(item_info[1], True, (0, 0, 0))
                                        screen.blit(tname, (250, 200))
                                    if scene >= 2:
                                        if scene == 2:
                                            if (frame//print_delay <= len(item_info[2])):
                                                item = base_font.render(item_info[2][:frame//print_delay], True, (0, 0, 0))
                                            else:
                                                item = base_font.render(item_info[2], True, (0, 0, 0))
                                                if frame//print_delay - len(item_info[2]) == 2:
                                                    scene += 1
                                                    frame = 0
                                        else:
                                            item = base_font.render(item_info[2], True, (0, 0, 0))
                                        screen.blit(item, (400, 300))
                                    if scene > 2:
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
                            elif action_name[0] == "i":
                                if action_name[1] == "0":
                                    if is_self:
                                        self_effect[0] = 3
                                    else:
                                        opp_effect[0] = 3
                                elif action_name[1] == "1":
                                    if is_self:
                                        self_effect[1] = 1
                                    else:
                                        opp_effect[1] = 1
                                elif action_name[1] == "2":
                                    if is_self:
                                        energy[curr_cards[player_num]] = min(10, energy[curr_cards[player_num]] + 5)
                            move_num += 1
                    else:
                        move_num+=1
                else:
                    ### handle end of turn events ###
                    # update effects
                    self_effect[0] = max(self_effect[0]-1, 0)
                    self_effect[1] = 0
                    opp_effect[0] = max(opp_effect[0]-1, 0)
                    opp_effect[1] = 0
                    for i in range(len(energy)):
                        energy[i] = min(10, energy[i]+1)

                    connection.send("xanicomp".encode())
                    game_status = "waiting"
                if first_frame:
                    first_fame = False
            
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
        draw_binder(screen, left_page, left_page + 1, resized_binder, pygame.font.Font("Teachemon.ttf", 9), card_images, cards_owned, card_back, button_exit, card_zoom, binder_highlight, highlight_num, teachemon_data, login_bg)
        
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
        draw_claim_menu(screen, logo, big_font.render("GACHA", True, (0, 0, 0)), big_font.render("TRADE", True, (0, 0, 0)), big_font.render("EXIT", True, (0, 0, 0)), resized_dispenser, screen_bg)
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
                    if gacha not in cards_owned:
                        new_card_sfx.play()
                        new_card_sfx.set_volume(volume/100)
                    else:
                        owned_card_sfx.play()
                        owned_card_sfx.set_volume(volume/100)
        
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
        pointer_on = True
        if pointer_pos == 4:
            pointer_x = 750
            pointer_y = 550
        else: 
            pointer_x = 150
            pointer_y = 200 + 100 * (pointer_pos - 1)
        # send some server message that this player is trying to trade and receive from server list of available players trying to trade
        # placeholder
        available_players = ["PLAYER 1", "PLAYER 2", "PLAYER 3", "PLAYER 4", "PLAYER 5"]
        draw_trade(screen, cards_owned, card_images, button_exit, big_font, binder_highlight, available_players)
    
    elif page == "Trade Loading":
        pointer_on = False
        # "up to continue" is temporary placeholder until server connections are implemented
        draw_trade_loading(screen, small_font, available_players[pointer_pos - 1])
    
    elif page == "Choose Trade Card":
        pointer_x = 350
        pointer_y = 530
        draw_trade_wheel(screen, userdata[2], pointer_hover, base_font, big_font, text_go, text_go_bg, text_go_rect, card_images)
        screen.blit(pointer_down, (485, 230))
        screen.blit(pointer_up, (485, 400))
    
    elif page == "View Trade":
        # last argument card_images[0] (recieve card) is placeholder for now
        # replace once server connection is implemented
        pointer_on = True
        pointer_x = 350
        pointer_y = 165 + pointer_pos * 130
        draw_view_trade(screen, big_font, base_font, card_images[userdata[2][pointer_hover]], card_images[0])

    elif page == "Trade Result": 
        pointer_on = True
        pointer_x = 750
        pointer_y = 550
        # if trade_success:
            # add the traded card to the other player idk how to do that lololol
            # remove the traded card from this player userdata
        draw_trade_result(screen, big_font, trade_success, button_exit)

    elif page == "Cut":
        pointer_on = False
        draw_cut(screen, button_exit, fontx3, big_font, cut_scene_animation, cut_scene_frame, vs_bg, main_screen_bg, userdata[0], opponent_username, cut_to)

        current_time = pygame.time.get_ticks()
        if current_time - last_update >= cut_scene_cooldown:
            if cut_scene_frame == 32:
                pygame.time.wait(1500)
                cut_scene_frame = 0
                if cut_to == 1:
                    page = "Battle"
                    connection.send("xCONNECTED".encode())
                if cut_to == 2:
                    page = "Choose Trade Card"
                    # send server connection 
                if cut_to == 3:
                    page = "View Trade"
                    # send server connection 

            else:
                cut_scene_frame += 1
                last_update = current_time
            
       
    elif page == "Settings":
        pointer_on = True
        if pointer_pos > 3:
            pointer_pos = 3
        pointer_x = 270
        pointer_y = 107 + 70 * (pointer_pos-1)
        draw_settings(screen, button_credits, base_font.render("VOLUME", True, (0, 0, 0)), button_exit)

    elif page == "Volume":
        pointer_on = False  

        screen.fill("grey")
        screen.blit(font.render("ADJUST VOLUME", True, "Black"), (260, 150))
        screen.blit(button_exit, (785, 555))
        screen.blit(pointer, (730, 555))

        if abs(volume - target_volume) > 0.5:  
            volume += (target_volume - volume) * 0.1  

        pygame.mixer.music.set_volume(volume / 100)
        pygame.draw.rect(screen, "black", (slider_x, slider_y, slider_width, slider_height))
        filled_width = int((volume / 100) * slider_width)
        pygame.draw.rect(screen, "yellow", (slider_x, slider_y, filled_width, slider_height))
    if pointer_on:
        screen.blit(pointer, (pointer_x, pointer_y))

    pygame.display.update()

pygame.quit()
