import pygame
from utils import *

# START SCREEN
def draw_start(screen: pygame.Surface, logo, button_login, button_signup):
    screen.fill("grey")
    screen.blit(logo, (30,50))
    screen.blit(button_login, (100,262))
    screen.blit(button_signup, (100,332))

# LOGIN SCREEN
def draw_login(screen: pygame.Surface, events, arrow_pos, username_tup, password_tup, login_button, back_tup, font):
    """
    Parameters
    screen: displays screen
    events: pygame event input
    arrow_pos: position of arrow
    username_tup: tuple of (text_username, text_username_rect, username_box)
    password_tup: tuple of (text_password, text_password_rect, password_box)
    login_button:tuple of (text_login_bg or text_signup_bg, text_login or text_signup, text_login_rect or text_signup_rect)
    back_tup: tupble of (text_back, text_back_rect)
    """
    screen.fill("grey")
    screen.blit(username_tup[0], username_tup[1])
    screen.blit(password_tup[0], password_tup[1])
    pygame.draw.rect(screen, (66, 245, 152), login_button[0], border_radius=5)
    screen.blit(login_button[1], login_button[2])
    screen.blit(back_tup[0], back_tup[1])
    username_tup[2].update(events, arrow_pos)
    password_tup[2].update(events, arrow_pos)
    username_tup[2].draw(screen, font)
    password_tup[2].draw(screen, font)

# DRAW MAGNIFYING GLASS
def draw_loading(screen, search_glass, circle_x, circle_y):
    screen.fill("darkgrey")
    screen.blit(search_glass, (450+circle_x, 250+circle_y))

# DRAW MAIN MENU
def draw_menu(screen, logo, battle, binder, claim, settings):
    screen.fill("grey")
    screen.blit(logo, (30,50))
    screen.blit(battle, (100,262))
    screen.blit(binder, (100,332))
    screen.blit(claim, (100,402))
    screen.blit(settings, (100,472))

def draw_battle_menu(screen, logo, button_m, button_s, button_e):
    screen.fill("grey")
    screen.blit(logo, (30, 50))
    screen.blit(button_m, (100, 262))
    screen.blit(button_s, (100, 332))
    screen.blit(button_e, (100, 402))

def draw_singleplayer_menu(screen):
    screen.fill("grey")

def draw_battle(screen, page, player_img, enemy_img, font, battle_base, battle_blank, teacher_info):
    if page == "00":
        screen.blit(battle_base, (0,0))
    else:
        screen.blit(battle_blank, (0,0))
    if page == "10":
        t11 = font.render(teacher_info[3].upper(), True, "White")
        t12 = font.render(teacher_info[7].upper(), True, "White")
        t13 = font.render(teacher_info[11].upper(), True, "White")
        t14 = font.render(teacher_info[0].upper(), True, "White")
        screen.blit(t11, ((253-(t11.get_width()/2)),430))
        screen.blit(t12, ((747-(t12.get_width()/2)),430))
        screen.blit(t13, ((253-(t13.get_width()/2)),525))
        screen.blit(t14, ((747-(t14.get_width()/2)),525))

    elif page == "20":
        pass
    elif page == "30":
        pass
    screen.blit(player_img, (140,135))
    screen.blit(enemy_img, (700,100))

# def draw_battle(screen, battle_page, battle_main):
#     if battle_page == "Main":
#         screen.blit(battle_main, (0, 0))

def draw_binder(screen, left, right, binder, font, button_exit):
    screen.fill("grey")
    screen.blit(binder, (0, 0))

    x = 170
    y = 0
    for i in range((left-1)*9, left*9):
        if i % 3 == 0:
            y += 130
            x = 170
        else:
            x += 100
        if i <= 58:
            screen.blit(font.render(str(i), True, (0, 0, 0)), (x, y))
    screen.blit(font.render(str(left), True, (0, 0, 0)), (110, 450))
    x = 580
    y = 0
    for i in range((right - 1) * 9, right * 9):
        if i % 3 == 0:
            y += 130
            x = 580
        else:
            x += 100
            
        if i <= 58:
            screen.blit(font.render(str(i), True, (0, 0, 0)), (x, y))

    screen.blit(font.render(str(right), True, (0, 0, 0)), (860, 450))
    screen.blit(button_exit, (785,555))

def draw_claim(screen, button_exit, dispenser, font, coins, gacha):
    screen.fill("grey")
    screen.blit(button_exit, (785,555))
    screen.blit(dispenser, (200,10))
    screen.blit(font.render(str(coins), True, (0, 0, 0)), (25, 5))
    screen.blit(font.render(str(gacha), True, (0, 0, 0)), (480, 250))

def draw_rotating_lever(screen, new_lever, rect):
    screen.blit(new_lever, rect)

def draw_settings(screen, button_credits, button_exit):
    screen.fill("grey")
    screen.blit(button_credits, (315,112))
    screen.blit(button_exit, (398,182))