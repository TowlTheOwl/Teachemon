import math
import pygame
import socket
import threading
import time

def update_circle(circle_x, circle_y, circle_angle, circle_start: bool, radius) -> tuple:
    """
    Update circle values for magnifying glass
    """
    if circle_start:
        circle_x = radius
        circle_start = False
    circle_x = math.sin(circle_angle) * radius
    circle_y = math.cos(circle_angle) * radius
    circle_angle += 0.05
    if circle_angle == 360:
        circle_angle = 0
    return (circle_x, circle_y, circle_angle, circle_start)

class Timer:
    def __init__(self, time, screen, run, font:pygame.font.Font, pos):
        self.screen = screen
        self.time = time
        self.run = run
        self.pos = pos
        self.font = font
        self.sprite = None
        self.rect = None
        threading.Thread(target=self.countdown).start()
    
    def countdown(self):
        while self.run[0]:
            self.update_sprite()
            if self.time > 0:
                time.sleep(1)
                self.time -= 1
            else:
                break
    
    def update_sprite(self):
        self.sprite = self.font.render(str(self.time), True, "white")
        self.rect = self.sprite.get_rect(center=self.pos)

    def draw(self):
        self.screen.blit(self.sprite, self.rect)
