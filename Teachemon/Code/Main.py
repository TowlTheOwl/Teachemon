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
button_exit = pygame.image.load("Images/exit x5.png")
battle = pygame.image.load("Images/fight_scene.png")
pointer = pygame.image.load("Images/pointer x5.png")
search_glass = pygame.image.load("Images/Magnifying Glass.png")

#Define Variables
username = ""
password = ""
clock = pygame.time.Clock()
page = "Menu"
pointer_on = True
pointer_x = 55
pointer_y = 257
circle_x = 0
circle_y = 0

#Define Screen drawing
def update_circle(radius):
    if circle_x >= radius:
        circle_y = math.sqrt((radius**2) - (circle_x**2))
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
            elif page == "Settings":
                if pointer_y != 177:
                    pointer_y += 70
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if page == "Start":
                if pointer_y == 257:
                    page = "Login"
                elif pointer_y == 327:
                    page = "Signup"
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