#Import and Initialize PyGame and math
import pygame
pygame.init()
import math

#Create display
ScreenWidth = 1000
ScreenHeight = 600
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
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

#Define Variables
username = ""
password = ""
send = ""
receive = ""
clock = pygame.time.Clock()
page = "Menu"
sbattle_page = "00"
battle_page = "Main"
fontx3 = pygame.font.Font("Font/Teachemon.ttf", 21)
fontx5 = pygame.font.Font("Font/Teachemon.ttf", 35)
teacher_file = open("Data/TeacheData.txt", "r")
teacher_data = teacher_file.readlines()
pteach1 = teacher_data[0].split(",")
pteach2 = []
pteach3 = []
pointer_on = True
pointer_x = 55
pointer_y = 257
circle_x = 0
circle_y = 0
circle_angle = 0
circle_start = True

#Define Screen drawing
def update_circle(radius):
    global circle_x
    global circle_y
    global circle_angle
    global circle_start
    if circle_start:
        circle_x = radius
        circle_start = False
    circle_x = math.sin(circle_angle) * radius
    circle_y = math.cos(circle_angle) * radius
    circle_angle += 0.05
    if circle_angle == 360:
        circle_angle = 0
    
def draw_start():
    screen.fill("grey")
    screen.blit(logo, (30,50))
    screen.blit(button_login, (100,262))
    screen.blit(button_signup, (100,332))
def draw_login():
    screen.fill("grey")
def draw_signup():
    screen.fill("grey")
def draw_loading():
    screen.fill("darkgrey")
    screen.blit(search_glass, (450+circle_x,250+circle_y))
def draw_menu():
    screen.fill("grey")
    screen.blit(logo, (30,50))
    screen.blit(button_battle, (100,262))
    screen.blit(button_binder, (100,332))
    screen.blit(button_claim, (100,402))
    screen.blit(button_settings, (100,472))
def draw_battle_menu():
    screen.fill("grey")
    screen.blit(logo, (30,50))
    screen.blit(button_multiplayer, (100,262))
    screen.blit(button_singleplayer, (100,332))
    screen.blit(button_exit, (100,402))
def draw_singleplayerMenu():
    screen.fill("grey")
def draw_SBattle():
    if sbattle_page == "00":
        screen.blit(battle_00, (0,0))
    else:
        screen.blit(battle_main, (0,0))
    if sbattle_page == "10":
        t11 = fontx3.render(pteach1[3].upper(), True, "White")
        t12 = fontx3.render(pteach1[7].upper(), True, "White")
        t13 = fontx3.render(pteach1[11].upper(), True, "White")
        t14 = fontx3.render(pteach1[0].upper(), True, "White")
        screen.blit(t11, ((253-(t11.get_width()/2)),430))
        screen.blit(t12, ((747-(t12.get_width()/2)),430))
        screen.blit(t13, ((253-(t13.get_width()/2)),525))
        screen.blit(t14, ((747-(t14.get_width()/2)),525))
        
    elif sbattle_page == "20":
        pass
    elif sbattle_page == "30":
        pass
    screen.blit(player_placeholder, (140,135))
    screen.blit(enemy_placeholder, (700,100))
def draw_battle():
    if battle_page == "Main":
        screen.blit(battle_main, (0,0))
def draw_binder():
    screen.fill("grey")
def draw_claim():
    screen.fill("grey")
    screen.blit(button_exit, (785,555))
def draw_settings():
    screen.fill("grey")
    screen.blit(button_credits, (315,112))
    screen.blit(button_exit, (398,182))
    
#Run Program
while run:
    clock.tick(24)
    #Sense for events like Quit and Key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if page == "Start":
                if pointer_y != 327:
                    pointer_y += 70
            elif page == "Menu":
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
            if page == "Start" or page == "Menu" or page == "Battle_Menu":
                if pointer_y != 257:
                    pointer_y -= 70
            elif page == "SBattle":
                if pointer_y != 435:
                    pointer_y -= 95
            elif page == "Settings":
                if pointer_y != 107:
                    pointer_y -= 70
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if page == "SBattle":
                if pointer_x != 30:
                    pointer_x -= 495
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if page == "SBattle":
                if pointer_x != 525:
                    pointer_x += 495
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            print(pointer_x)
            print(pointer_y)
            print(page)
            print(sbattle_page)
            if page == "Start":
                if pointer_y == 257:
                    page = "Login"
                elif pointer_y == 327:
                    page = "Signup"
            elif page == "Menu":
                if pointer_y == 257:
                    page = "Battle_Menu"
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
    if page == "Start":
        pointer_on = True
        draw_start()
    elif page == "Login":
        pointer_on = True
        draw_login()
    elif page == "Signup":
        pointer_on = True
        draw_signup()
    elif page == "Menu":
        pointer_on = True
        draw_menu()
    elif page == "Loading":
        pointer_on = False
        draw_loading()
        update_circle(50)
    elif page == "Battle_Menu":
        draw_battle_menu()
    elif page == "SingleplayerMenu":
        draw_singleplayerMenu()
    elif page == "SBattle":
        draw_SBattle()
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