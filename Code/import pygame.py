import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Gacha Rotation")

# Load the lever image and other assets if needed
lever_image = pygame.image.load("Images/test6.png").convert_alpha()
lever_image = pygame.transform.scale(lever_image, (65, 364))
lever_rect = lever_image.get_rect()

# Set up rotation parameters
pivot_point = lever_rect.center  # The fixed pivot point around which to rotate
angle = 0  # Initial rotation angle
rotation_speed = 2  # Degrees per frame
max_angle = 45  # Maximum angle to rotate

# Flags for rotation and gacha
rotating_forward = False
rotating_backward = False
gacha_dict = {}  # Store gacha results
gacha = ""
# Main loop
running = True
clock = pygame.time.Clock()

def draw_claim(rotated_lever, lever_rect, gacha):
    screen.fill((255, 255, 255))  # Fill the screen with white
    screen.blit(rotated_lever, lever_rect)  # Draw the rotated lever
    
    # Display gacha outcome
    font = pygame.font.Font(None, 36)
    text = font.render(f'Gacha Result: {gacha}', True, (0, 0, 0))
    screen.blit(text, (50, 50))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gacha = random.randint(0, 58)
            gacha_dict[gacha] = True  # Store the gacha result

            # Start the rotation sequence
            rotating_forward = True
            rotating_backward = False

    # Update rotation angle based on direction
    if rotating_forward:
        angle += rotation_speed
        if angle >= max_angle:
            angle = max_angle
            rotating_forward = False
            rotating_backward = True
    elif rotating_backward:
        angle -= rotation_speed
        if angle <= 0:
            angle = 0
            rotating_backward = False

    # Rotate the lever image
    rotated_lever = pygame.transform.rotate(lever_image, -angle)
    rotated_rect = rotated_lever.get_rect(center=pivot_point)

    # Draw everything on screen
    draw_claim(rotated_lever, rotated_rect, gacha)  # Update display with gacha result
    pygame.display.flip()  # Refresh the screen

    # Control the frame rate
    clock.tick(30)
