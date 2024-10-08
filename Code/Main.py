#Import and Initialize PyGame
import pygame
pygame.init()

#Create display
ScreenWidth = 1000
ScreenHeight = 600
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("Teachemon")

run = True

#Import Images
logo = pygame.image.load("Images/logo x4.png")
button_battle = pygame.image.load("Images/battle x5.png")
button_binder = pygame.image.load("Images/binder x5.png")
button_claim = pygame.image.load("Images/claim x5.png")
button_settings = pygame.image.load("Images/settings x5.png")
button_credits = pygame.image.load("Images/credits x5.png")
button_exit = pygame.image.load("Images/exit x5.png")
battle = pygame.image.load("Images/fight_scene.png")
pointer = pygame.image.load("Images/pointer x5.png")

#Define Variables
page = "Menu"
pointer_on = True
pointer_x = 55
pointer_y = 257

#Define Screen drawing

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
def draw_settings():
    screen.fill("grey")
    screen.blit(button_credits, (315,112))
    screen.blit(button_exit, (398,182))
    
#Run Program
while run:
    #Sense for events like Quit and Key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if page == "Menu":
                if pointer_y != 467:
                    pointer_y += 70
            elif page == "Settings":
                if pointer_y != 177:
                    pointer_y += 70
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if page == "Menu":
                if pointer_y != 257:
                    pointer_y -= 70
            elif page == "Settings":
                if pointer_y != 107:
                    pointer_y -= 70
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if page == "Menu":
                if pointer_y == 257:
                    page = "Battle"
                elif pointer_y == 327:
                    page = "Binder"
                    pointer_on = False
                elif pointer_y == 397:
                    page = "Claim"
                    pointer_on = False
                elif pointer_y == 467:
                    page = "Settings"
                    pointer_x = 270
                    pointer_y = 107
            elif page == "Settings":
                if pointer_y == 107:
                    print("credits")
                elif pointer_y == 177:
                    page = "Menu"
                    pointer_x = 55
                    pointer_y = 467
    if page == "Menu":
        draw_menu()
    elif page == "Battle":
        draw_battle()
    elif page == "Binder":
        draw_binder()
    elif page == "Claim":
        draw_claim()
    elif page == "Settings":
        draw_settings()
    if pointer_on:
        screen.blit(pointer, (pointer_x, pointer_y))
    pygame.display.update()

pygame.quit()