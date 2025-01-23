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
def draw_loading(screen, search_glass, circle_x, circle_y, exit_button):
    screen.fill("darkgrey")
    screen.blit(search_glass, (450+circle_x, 250+circle_y))
    screen.blit(exit_button, (785,555))

# DRAW MAIN MENU
def draw_menu(screen, logo, battle, binder, claim, settings, screen_bg):
    #screen.fill("grey")
    screen.blit(screen_bg, (0,0))
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

def draw_battle(screen:pygame.SurfaceType, page, player_img, enemy_img, font, battle_base, battle_blank, teacher_info:dict, opp_username, small_font:pygame.font.Font, other_cards:tuple):
    if page == "00":
        screen.blit(battle_base, (0,0))
    else:
        screen.blit(battle_blank, (0,0))
        if page == "10":
            t11 = font.render(teacher_info["Move 1 Name"].upper(), True, "White")
            t12 = font.render(teacher_info["Move 2 Name"].upper(), True, "White")
            t13 = font.render(teacher_info["Move 3 Name"].upper(), True, "White")
            t14 = font.render("Back".upper(), True, "White")

        elif page == "20":
            t11 = font.render("Item 1".upper(), True, "White")
            t12 = font.render("Item 2".upper(), True, "White")
            t13 = font.render("Item 3".upper(), True, "White")
            t14 = font.render("Back".upper(), True, "White")
            
        elif page == "30":
            t11 = font.render(str(other_cards[0]).upper(), True, "White")
            t12 = font.render(str(other_cards[1]).upper(), True, "White")
            t13 = font.render(str(other_cards[2]).upper(), True, "White")
            t14 = font.render("Back".upper(), True, "White")
        
        elif page == "40":
            t11 = font.render("FORFEIT", True, "White")
            t12 = font.render("BACK", True, "White")
            t13 = font.render("", True, "White")
            t14 = font.render("", True, "White")
        screen.blit(t11, ((253-(t11.get_width()/2)),430))
        screen.blit(t12, ((747-(t12.get_width()/2)),430))
        screen.blit(t13, ((253-(t13.get_width()/2)),525))
        screen.blit(t14, ((747-(t14.get_width()/2)),525))
    
    screen.blit(player_img, (140,135))
    screen.blit(enemy_img, (700,100))
    
    opp_name = small_font.render(opp_username, True, "White")
    opp_name_rect = opp_name.get_rect(topright=(screen.get_width()-20, 20))
    screen.blit(opp_name, opp_name_rect)

# def draw_battle(screen, battle_page, battle_main):
#     if battle_page == "Main":
#         screen.blit(battle_main, (0, 0))

def draw_binder(screen, left, right, binder, font, card_images, cards_owned, card_back, button_exit, card_zoom, binder_highlight, highlight_num):
    screen.fill("grey")
    screen.blit(binder, (0, 0))
    x = 150
    y = 100

    for i in range(18):
        card_num = (i + 18 * int(left / 2))
        if card_num in cards_owned:
            screen.blit(card_images[card_num], (x, y))
        else:
            screen.blit(card_back, (x, y))
        
        if (i + 1) % 9 == 0:
            x = 475
            y = 100
        elif (i + 1) % 3 == 0:
            y += 135
            x -= 285

        x += 95

    screen.blit(font.render(str(left), True, (0, 0, 0)), (110, 430))
    screen.blit(font.render(str(right), True, (0, 0, 0)), (860, 430))
    screen.blit(button_exit, (785,555))

    if highlight_num < 9:
        screen.blit(binder_highlight, (150 + highlight_num%3*95, 100 + highlight_num//3*135))
    else:
        screen.blit(binder_highlight, (570 + (highlight_num-9)%3*95, 100 + (highlight_num-9)//3*135))

    # print(card_zoom)
    card_num = highlight_num + 18 * int(left/2)
    if card_zoom > 1 and card_num in cards_owned:
        width = 90 * card_zoom
        height = 123 * card_zoom
        screen.blit(pygame.transform.scale(card_images[card_num], (width, height)), (500 - (width / 2), 300 - (height / 2)))

def draw_claim(screen, button_exit, font, coins, gacha, animation_list, frame, action, card_visible, current_card, card_rect, lever_rect, screen_bg, resized_coin):
    screen.blit(screen_bg, (0,0))
    screen.blit(button_exit, (785,555))
    screen.blit(animation_list[action][frame], (250,50))
    screen.blit(font.render(str(coins), True, (0, 0, 0)), (25, 5))
    screen.blit(resized_coin, (40, 5))
    #screen.blit(font.render(str(gacha), True, (255, 255, 255)), (480, 250))
    #pygame.draw.rect(screen, "grey", lever_rect)
    if card_visible and current_card:
        screen.blit(current_card, card_rect)

def draw_cut(screen, button_exit, font, animation_list, frame, vs_bg):
    if frame <= 16:
        screen.fill("grey")
    else:
        vs_bg.blit(font.render("TEACHER 1", True, "White"), (50, 300))
        vs_bg.blit(font.render("TEACHER 2", True, "White"), (450, 150))
        vs_bg.blit(font.render("VS", True, "White"), (375, 250))
        screen.blit(pygame.transform.scale(vs_bg, (1000, 600)), (0, 0))
    # screen.blit(button_exit, (785,555))
    screen.blit(animation_list[frame], (0,-150))

# def draw_rotating_lever(screen, new_lever, rect):
#     screen.blit(new_lever, rect)

def draw_settings(screen, button_credits, button_exit):
    screen.fill("grey")
    screen.blit(button_credits, (315,112))
    screen.blit(button_exit, (398,182))

def draw_choose_your_team(screen:pygame.Surface, button_exit, text_cyt, cyt_rect, button_go_text, button_go_bg, button_go_rect, selected_cards, font):
    screen.fill("grey")
    pygame.draw.rect(screen, (150, 150, 150), button_go_bg, border_radius=5)
    screen.blit(button_go_text, button_go_rect)
    screen.blit(button_exit, (785,555))
    screen.blit(text_cyt, cyt_rect)
    for i in range(4):
        pygame.draw.rect(screen, (20, 20, 20), (145+i*200, 105, 110, 150))
        draw_text(screen, str(selected_cards[i]), font, (255, 255, 255), (200+i*200, 180))

def draw_card_wheel(screen, cards, selected_cards, pointer, font:pygame.font.Font, font_small):
    len_cards = len(cards)
    cards_to_draw = [cards[pointer+i] if i>=-pointer and i+pointer<len_cards else None for i in (-2, -1, 0, 1, 2)]
    pygame.draw.rect(screen, (0, 0, 0), ((445, 315),(110, 150)))    # draw center card
    card = cards_to_draw[2]
    color = (255, 255, 255)
    if card in selected_cards:
        color = (255, 100, 100)
    draw_text(screen, str(card), font, color, (500, 390))

    y = 352
    card_size = (55, 75)
    
    # draw left cards
    for i in range(2):
        card = cards_to_draw[i]
        if card is not None:
            color = (255, 255, 255)
            if card in selected_cards:
                color = (255, 100, 100)
            pygame.draw.rect(screen, (0, 0, 0), ((255+(i*95),y),card_size))
            draw_text(screen, str(card), font_small, color, (282+(i*95), 390))
    # draw right cards
    for i in range(2):
        card = cards_to_draw[i+3]
        if card is not None:
            color = (255, 255, 255)
            if card in selected_cards:
                color = (255, 100, 100)
            pygame.draw.rect(screen, (0, 0, 0), ((595+(i*95),y),card_size))
            draw_text(screen, str(card), font_small, color, (622+(i*95), 390))

def draw_text(screen:pygame.Surface, text:str, font:pygame.font.Font, color:tuple, pos:tuple):
    render = font.render(text, True, color)
    render_rect = render.get_rect(center=pos)
    screen.blit(render, render_rect)
