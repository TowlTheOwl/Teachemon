#Import and Initialize PyGame
#eesther 

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
binder = pygame.image.load("Images/binder2.png")
resized_binder = pygame.transform.scale(binder, (1000, 600))
dispenser = pygame.image.load("Images/dispenser.png")
resized_dispenser = pygame.transform.scale(dispenser, (281.25, 492.5))

#dicionary of cards for binder. numbers will correlate to cards, and they are all false for now 
dict = {}
for i in range(59):
    dict[i] = False
font = pygame.font.Font(None, 70)

#Define Variables
page = "Menu"
pointer_on = True
pointer_x = 55
pointer_y = 257
left_page = 1
right_page = 2
coins = 0

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
def draw_binder(left, right):
    screen.fill("grey")
    screen.blit(resized_binder, (0, 0))
    x = 170
    y = 0
    #printing numbers for left page 
    for i in range((left - 1) * 9, (left) * 9):
        if i % 3 == 0:
            y += 130
            x = 170
        else:
            x += 100
        if i <= 58:
            screen.blit(font.render(str(i), True, (0, 0, 0)), (x, y))
    
    screen.blit(font.render(str(left), True, (0, 0, 0)), (110, 430))


    x = 580
    y = 0
    #printing numbers for right page 
    for i in range((right - 1) * 9, right * 9):
        if i % 3 == 0:
            y += 130
            x = 580
        else:
            x += 100

        if i <= 58:
            screen.blit(font.render(str(i), True, (0, 0, 0)), (x, y))

    screen.blit(font.render(str(right), True, (0, 0, 0)), (860, 430))
    screen.blit(button_exit, (785,555))



def draw_claim():
    screen.fill("grey")
    screen.blit(button_exit, (785,555))
    screen.blit(resized_dispenser, (350,50))
    screen.blit(font.render(str(coins), True, (0, 0, 0)), (25, 0))
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and pointer_on:
            if page == "Menu":
                if pointer_y == 257:
                    page = "Battle"
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

        #binder 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if page == "Binder" and left_page > 0 and right_page < 7:
                left_page += 2
                right_page += 2
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
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

                    
    if page == "Menu":
        draw_menu()
    elif page == "Battle":
        draw_battle()
    elif page == "Binder":
        draw_binder(left_page, right_page)
    elif page == "Claim":
        draw_claim()
    elif page == "Settings":
        draw_settings()
    if pointer_on:
        screen.blit(pointer, (pointer_x, pointer_y))
    pygame.display.update()

pygame.quit()
