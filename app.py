"""
    Machine Problem 4: Six Men Morris AI vs Player
    Made by: John Paul Monter

    Need to install:
        pip install pygame
        pip install gif_pygame
"""

import pygame
import sys 
import gif_pygame

HEIGHT = 600
WIDTH = 800
ICON_HEIGHT = 84
ICON_WEIGHT = 84
LIGHTGRAY = "#D9D9D9"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Six Men Morris")
clock = pygame.time.Clock()

surface = pygame.Surface((WIDTH, HEIGHT))
surface.fill(LIGHTGRAY)
# background_image = pygame.image.load("./assets/background.png")
# background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
background_gif = gif_pygame.load("./assets/fox.gif")

# Play Button
play_button_image = pygame.image.load("./assets/icons8-play-128.png")
play_button_rect = play_button_image.get_rect()
play_button_rect.center = (WIDTH*0.5, HEIGHT*0.5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    screen.blit(surface, (0,0))
    background_gif.render(screen, (400-background_gif.get_width()*0.5, 300-background_gif.get_height()*0.5))
    screen.blit(play_button_image, play_button_rect)
    
    pygame.display.update()
    clock.tick(60)
