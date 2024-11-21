import math
import pygame
import socket

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