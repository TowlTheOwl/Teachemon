import pygame
from utils import *

# START SCREEN
def draw_start(screen: pygame.Surface, logo, button_login, button_signup, login_bg):
    screen.blit(login_bg, (0,0))
    screen.blit(logo, (30,50))
    screen.blit(button_login, (100,262))
    screen.blit(button_signup, (100,332))

# LOGIN SCREEN
def draw_login(screen: pygame.Surface, events, arrow_pos, username_tup, password_tup, login_button, back_tup, font, login_bg):
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
    screen.blit(login_bg, (0,0))
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

def draw_claim_menu(screen, logo, gacha, trade, exit):
    screen.fill("grey")
    screen.blit(logo, (30, 50))
    screen.blit(gacha, (100, 262))
    screen.blit(trade, (100, 332))
    screen.blit(exit, (100, 402))


def draw_trade(screen, cards_owned, cards, exit, font, highlight, available_players):
    screen.fill("grey")
    # screen.blit(font.render("YOUR TRADE:", True, "Black"), (50, 100))

    if len(cards_owned) == 0: 
        screen.blit(font.render("NO CARDS", True, "Black"), (50, 200))

    else:
        screen.blit(font.render("AVAILABLE PLAYERS", True, "Black"), (100, 100))
        # available_players is a placeholder
        for i in range(3):
            screen.blit(font.render(available_players[i], True, "Black"), (300, 200 + 100 * i))

        screen.blit(exit, (785,555))

def draw_trade_loading(screen, font, player):
    screen.fill("grey")
    screen.blit(font.render("WAITING FOR " + player + "...", True, "Black"), (50, 250))

def draw_trade_wheel(screen, cards, pointer, font:pygame.font.Font, big_font, button_go_text, button_go_bg, button_go_rect, card_images):
    screen.fill("grey")
    len_cards = len(cards)
    cards_to_draw = [cards[pointer+i] if i>=-pointer and i+pointer<len_cards else None for i in (-2, -1, 0, 1, 2)]
    card = cards_to_draw[2]
    
    screen.blit(big_font.render("CHOOSE YOUR CARD", True, "Black"), (140, 100))
    # placeholder timer
    screen.blit(font.render("TIMER", True, "Black"), (800, 25))
    pygame.draw.rect(screen, (150, 150, 150), button_go_bg, border_radius=5)
    screen.blit(button_go_text, button_go_rect)

    screen.blit(card_images[card], (460, 270))

    y = 320
    card_size = (55, 75)

    # draw left cards
    for i in range(2):
        card = cards_to_draw[i]
        if card is not None:
            screen.blit(card_images[card], (200+(i*110), y))
    # draw right cards
    for i in range(2):
        card = cards_to_draw[i+3]
        if card is not None:
            screen.blit(card_images[card], (610+(i*110), y))

def draw_view_trade(screen, big_font, small_font, trade_card, receive_card):
    screen.fill("grey")
    screen.blit(big_font.render("VIEW TRADE", True, "Black"), (250, 50))
    screen.blit(small_font.render("TRADE", True, "Black"), (70, 160))
    screen.blit(small_font.render("RECEIVE", True, "Black"), (670, 160))
    screen.blit(pygame.transform.scale(trade_card, (180, 246)), (80, 250))
    screen.blit(pygame.transform.scale(receive_card, (180, 246)), (710, 250))
    screen.blit(small_font.render("ACCEPT", True, "Black"), (390, 300))
    screen.blit(small_font.render("DECLINE", True, "Black"), (390, 430))

def draw_trade_result(screen, font, success, exit):
    screen.fill("grey")
    if success:
        screen.blit(font.render("TRADE SUCCESSFUL", True, "Black"), (150, 200))
    else:
        screen.blit(font.render("TRADE DENCLINED...", True, "Black"), (200, 200))
    screen.blit(exit, (785,555))

def draw_singleplayer_menu(screen:pygame.SurfaceType, font, big_font):
    screen.fill("grey")
    screen.blit(big_font.render("SINGLE PLAYER", True, "Black"), (150, 50))
    screen.blit(font.render("EASY", True, "Black"), (150, 200))
    screen.blit(font.render("MEDIUM", True, "Black"), (150, 350))
    screen.blit(font.render("HARD", True, "Black"), (150, 500))

def draw_battle(screen:pygame.SurfaceType, page, font, battle_base, battle_blank, teacher_info:dict, opp_username, small_font:pygame.font.Font, other_cards:tuple):
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
            t11 = font.render("Attack Potion".upper(), True, "White")
            t12 = font.render("Defense Potion".upper(), True, "White")
            t13 = font.render("Energy Potion".upper(), True, "White")
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
    
    opp_name = small_font.render(opp_username, True, "White")
    opp_name_rect = opp_name.get_rect(topright=(screen.get_width()-20, 20))
    screen.blit(opp_name, opp_name_rect)

# def draw_battle(screen, battle_page, battle_main):
#     if battle_page == "Main":
#         screen.blit(battle_main, (0, 0))

def draw_binder(screen, left, right, binder, font, card_images, cards_owned, card_back, button_exit, card_zoom, binder_highlight, highlight_num, data):
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
        
        
        if card_zoom >= 3:
            move1 = data[card_num]["Move 1 Name"] + "-" + data[card_num]["Move 1 Damage"]
            screen.blit(font.render(move1.upper(), True, "Black"), (395, 315))
            move2 = data[card_num]["Move 2 Name"] + "-" + data[card_num]["Move 2 Damage"]
            screen.blit(font.render(move2.upper(), True, "Black"), (395, 365))
            move3 = data[card_num]["Move 3 Name"]+ "-" + data[card_num]["Move 2 Damage"]
            screen.blit(font.render(move3.upper(), True, "Black"), (395, 415))

def draw_claim(screen, button_exit, font, coins, animation_list, frame, action, card_visible, current_card, card_rect, screen_bg, resized_coin, 
               alpha, card_started, card_anim, max_cardanim, fade_started, 
               cardanim_list, cardanim_frame, display_started, no_coins, no_coins_duration, no_coins_timer, owned, big_font:pygame.font.Font):
    owned_msg = "CARD ALREADY OWNED"
    screen.blit(screen_bg, (0,0))
    screen.blit(button_exit, (785,555))
    screen.blit(animation_list[action][frame], (250,50))
    screen.blit(big_font.render(str(coins), True, (0, 0, 0)), (30, 30))
    screen.blit(resized_coin, (90, 5))
    fade_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

    #not enough coins warning
    if no_coins and pygame.time.get_ticks() - no_coins_timer < no_coins_duration:
        warning_surf = big_font.render(no_coins, True, (255,0,0))
        warning_rect = warning_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() - 80))
        screen.blit(warning_surf, warning_rect)
    #faded overlay
    if card_visible and current_card:
        fade_surface.fill((255, 255, 255, alpha)) 
        screen.blit(fade_surface, (0, 0)) 
    #card animation display
    if display_started:
        anim_x = screen.get_width() // 2 - cardanim_list[0].get_width() // 2
        anim_y = screen.get_height() // 2 - cardanim_list[0].get_height() // 2
        screen.blit(cardanim_list[cardanim_frame], (anim_x, anim_y))
    #scaling card up
    if card_started:
        scale = 1 + (card_anim / max_cardanim) * 1
        new_card = pygame.transform.smoothscale(current_card, (int(card_rect.width * scale), int(card_rect.height * scale)))
        new_rect = new_card.get_rect(center=card_rect.center)
        card_rect = new_rect
        screen.blit(new_card, new_rect)
        #if card is already owned
        if not owned:
            owned_surf = big_font.render(owned_msg, True, (255,0,0))
            owned_rect = owned_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() - 80))
            screen.blit(owned_surf, owned_rect)      
        elif owned:
            not_owned = "NEW"
            not_owned_surf = big_font.render(not_owned, True, (255,0,0))
            not_owned_rect = not_owned_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() - 80))
            screen.blit(not_owned_surf, not_owned_rect) 
       

def draw_cut(screen, button_exit, font, big_font, animation_list, frame, vs_bg, main_bg, username, opponent_username, cut_to):
    if frame <= 16:
        screen.blit(pygame.transform.scale(main_bg, (1000, 600)), (0, 0))
    else:
        if cut_to == 1: # cut to battle
            screen.blit(pygame.transform.scale(main_bg, (1000, 600)), (0, 0))
            screen.blit(font.render(username.upper(), True, "Black"), (150, 300))
            screen.blit(font.render(opponent_username.upper(), True, "Black"), (725, 300))
            screen.blit(font.render("VS", True, "Black"), (500, 300))
            screen.blit(pygame.transform.scale(vs_bg, (1270, 720)), (0, -50))
        elif cut_to == 2: # cut to choose your trade card
            screen.fill("grey")
            screen.blit(big_font.render("CHOOSE YOUR CARD", True, "Black"), (140, 100))
        elif cut_to == 3: # cut to view trade
            screen.fill("grey")
            screen.blit(big_font.render("VIEW TRADE", True, "Black"), (250, 50))

    screen.blit(animation_list[frame], (0, -150))

def draw_settings(screen, button_credits, button_exit):
    screen.fill("grey")
    screen.blit(button_credits, (315,112))
    screen.blit(button_exit, (398,182))

def draw_credits(screen, button_exit, font, image):
    pygame.init()
    screen.fill("grey")

    credits = [
        "",
        "IN HONOR OF MR HONG...",
        "",
        "HOW DID THE DOG GET STRAIGHT AS",
        "",
        "",
        "",
        "",
        "",
        "IT WAS THE TEACHERS PET!",
        "",
        "",
        "",
        "OUR TEAM",
        "",
        "",
        "OUR CEO HENRY NOT HARRY YANG",
        "DANTASTIC DANIEL CHOI",
        "JUBILANT JESSICA NI",
        "CHEERFUL CASSIDY TRAN",
        "ESTHER CARL SAYS HI"

    ]

    credit_surfaces = []
    for line in credits:
        credit_surfaces.append(font.render(line, True, "white"))
    content_height = image.get_height() + len(credit_surfaces) * 50
    width, height = 1000, 600
    y = height
    x = width


    speed = 1
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False

        image_x = (width - image.get_width()) // 2
        screen.blit(image, (image_x, y))

        for i, surface in enumerate(credit_surfaces):
            x = (width - surface.get_width()) // 2
            screen.blit(surface, (x, y + image.get_height() + i * 50))
        
        y -= speed
        if y + content_height < 0:
            running = False

        pygame.display.flip()
        clock.tick(60)

def draw_choose_your_team(screen:pygame.Surface, button_exit, text_cyt, cyt_rect, button_go_text, button_go_bg, button_go_rect, selected_cards, font, card_images):
    screen.fill("grey")
    pygame.draw.rect(screen, (150, 150, 150), button_go_bg, border_radius=5)
    screen.blit(button_go_text, button_go_rect)
    screen.blit(button_exit, (785,555))
    screen.blit(text_cyt, cyt_rect)
    for i in range(4):
        #pygame.draw.rect(screen, (20, 20, 20), (145+i*200, 105, 110, 150))
        #draw_text(screen, str(selected_cards[i]), font, (255, 255, 255), (200+i*200, 180))
        screen.blit((card_images[selected_cards[i]]), (160+i*200, 105))

def draw_card_wheel(screen, cards, selected_cards, pointer, font:pygame.font.Font, font_small, card_images):
    len_cards = len(cards)
    cards_to_draw = [cards[pointer+i] if i>=-pointer and i+pointer<len_cards else None for i in (-2, -1, 0, 1, 2)]
    #pygame.draw.rect(screen, (0, 0, 0), ((445, 315),(110, 150)))    # draw center card
    card = cards_to_draw[2]
    #color = (255, 255, 255)
    #if card in selected_cards:
        #color = (255, 100, 100)
    #draw_text(screen, str(card), font, color, (500, 390))
    screen.blit(card_images[card], (460, 315))

    y = 352
    card_size = (55, 75)
    

    # draw left cards
    for i in range(2):
        card = cards_to_draw[i]
        if card is not None:
            color = (255, 255, 255)
            if card in selected_cards:
                color = (255, 100, 100)
            #pygame.draw.rect(screen, (0, 0, 0), ((255+(i*95),y),card_size))
            #draw_text(screen, str(card), font_small, color, (282+(i*95), 390))
            screen.blit(card_images[card], (255+(i*95), y))
    # draw right cards
    for i in range(2):
        card = cards_to_draw[i+3]
        if card is not None:
            color = (255, 255, 255)
            if card in selected_cards:
                color = (255, 100, 100)
            #pygame.draw.rect(screen, (0, 0, 0), ((595+(i*95),y),card_size))
            #draw_text(screen, str(card), font_small, color, (622+(i*95), 390))
            screen.blit(card_images[card], (595+(i*95), y))

def draw_text(screen:pygame.Surface, text:str, font:pygame.font.Font, color:tuple, pos:tuple):
    render = font.render(text, True, color)
    render_rect = render.get_rect(center=pos)
    screen.blit(render, render_rect)
