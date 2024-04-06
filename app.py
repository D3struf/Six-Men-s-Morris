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
import webbrowser

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

# Background

background_gif = gif_pygame.load("./assets/fox.gif")

# Play Button
play_button_image = pygame.image.load("./assets/icons8-play-128.png").convert_alpha()
play_button_rect = play_button_image.get_rect()
play_button_rect.center = (WIDTH*0.5, HEIGHT*0.5)

# Instructions
instruction1_image = pygame.image.load("./assets/instruction1.png").convert_alpha()
instruction1_rect = instruction1_image.get_rect()
instruction1_rect.center = (WIDTH*0.5, HEIGHT*0.5)

instruction2_image = pygame.image.load("./assets/instruction2.png").convert_alpha()
instruction2_rect = instruction2_image.get_rect()
instruction2_rect.center = (WIDTH*0.5, HEIGHT*0.5)

# Back Button
back_button = pygame.image.load("./assets/icons8-rewind-64.png").convert_alpha()
back_button_rect = back_button.get_rect()
back_button_rect.topleft = (214, 467)

# Next Button
next_button = pygame.image.load("./assets/icons8-forward-64.png").convert_alpha()
next_button_rect = next_button.get_rect()
next_button_rect.topleft = (514, 467)

# Start Button
start_button = pygame.image.load("./assets/start_button.png").convert_alpha()
start_button_rect = start_button.get_rect()
start_button_rect.topleft = (449, 467)

# Game Board
board = pygame.image.load("./assets/board.png").convert_alpha()
board_rect = board.get_rect()
board_rect.topleft = (0, 0)

# Pause Button
pause_button = pygame.image.load("./assets/icons8-pause-64.png").convert_alpha()
pause_button_rect = pause_button.get_rect()
pause_button_rect.topleft = (708, 19)

# Pause Overlay
pause_overlay = pygame.image.load("./assets/icons8-pause.png").convert_alpha()
pause_overlay_rect = pause_overlay.get_rect()
pause_overlay_rect.center = (WIDTH*0.5, HEIGHT*0.5)

# Play Again Button
play_again_button = pygame.image.load("./assets/icons8-play-80.png").convert_alpha()
play_again_button_rect = play_again_button.get_rect()
play_again_button_rect.topleft = (360, 300)

# Restart Button
restart_button = pygame.image.load("./assets/icons8-restart-80.png")
restart_button_rect = restart_button.get_rect()
restart_button_rect.topleft = (239, 300)

# Exit Button
exit_button = pygame.image.load("./assets/icons8-exit-80.png")
exit_button_rect = exit_button.get_rect()
exit_button_rect.topleft = (481, 300)

# White Board Piece
white_pieces = []
white_piece_image = pygame.image.load("./assets/icons8-circle-64.png").convert_alpha()

piece_positions = [
    (708, 100),
    (708, 164),
    (708, 230),
    (708, 296),
    (708, 362),
    (708, 427)
]

for position in piece_positions:
    piece_rect = white_piece_image.get_rect(topleft=position)
    white_pieces.append(piece_rect)
    
# Black Board Piece
black_pieces = []
black_piece_image = pygame.image.load("./assets/icons8-circle-64 (1).png").convert_alpha()

piece_positions = [
    (27, 100),
    (27, 164),
    (27, 230),
    (27, 296),
    (27, 362),
    (27, 427)
]

for position in piece_positions:
    piece_rect = black_piece_image.get_rect(topleft=position)
    black_pieces.append(piece_rect)

# Piece-Board Position
green_pieces = []
green_piece_image = pygame.image.load("./assets/icons8-circle-50.png").convert_alpha()
green_piece_image = pygame.transform.scale(green_piece_image, (25, 25))

board_piece_positions = [
    (185, 82),
    (385, 82),
    (590, 82),
    (284, 182),
    (385, 182),
    (488, 182),
    (185, 287),
    (284, 287),
    (488, 287),
    (590, 287),
    (284, 386),
    (385, 386),
    (488, 386),
    (185, 488),
    (385, 488),
    (590, 488),
]

for position in board_piece_positions:
    piece_rect = green_piece_image.get_rect(topleft=position)
    green_pieces.append(piece_rect)

# Github Button
github_button = pygame.image.load("./assets/icons8-github-64.png").convert_alpha()
github_button = pygame.transform.scale(github_button, (40, 40))
github_button_rect = github_button.get_rect()
github_button_rect.topleft = (740, 540)

github_url = "https://github.com/D3struf/Six-Men-s-Morris.git"

# Game States
home_page = False
instruction1_page = False
instruction2_page = False
board_page = True
is_pause = False

while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if home_page:
                if play_button_rect.collidepoint(mouse_pos):
                    home_page = False
                    instruction1_page = True
            elif instruction1_page:
                if back_button_rect.collidepoint(mouse_pos):
                    instruction1_page = False
                    home_page = True
                elif next_button_rect.collidepoint(mouse_pos):
                    instruction1_page = False
                    instruction2_page = True
            elif instruction2_page:
                if back_button_rect.collidepoint(mouse_pos):
                    instruction2_page = False
                    instruction1_page = True
                elif start_button_rect.collidepoint(mouse_pos):
                    instruction2_page = False
                    board_page = True
            elif github_button_rect.collidepoint(mouse_pos):
                webbrowser.open(github_url)
            elif pause_button_rect.collidepoint(mouse_pos):
                is_pause = not is_pause
            elif play_again_button_rect.collidepoint(mouse_pos):
                is_pause = not is_pause
            elif exit_button_rect.collidepoint(mouse_pos):
                is_pause = not is_pause
                board_page = False
                home_page = True
        

    if home_page:
        print("Home")
        screen.blit(surface, (0,0))
        background_gif.render(screen, (400-background_gif.get_width()*0.5, 300-background_gif.get_height()*0.5))
        screen.blit(play_button_image, play_button_rect)
    elif instruction1_page:
        print("ins1")
        screen.blit(surface, (0,0))
        screen.blit(instruction1_image, instruction1_rect)
        screen.blit(back_button, back_button_rect)
        screen.blit(next_button, next_button_rect)
    elif instruction2_page:
        print("ins2")
        screen.blit(surface, (0,0))
        screen.blit(instruction2_image, instruction2_rect)
        screen.blit(back_button, back_button_rect)
        screen.blit(start_button, start_button_rect)
    elif board_page:
        print("board")
        screen.blit(surface, (0,0))
        screen.blit(board, board_rect)
        screen.blit(pause_button, pause_button_rect)
        screen.blit(github_button, github_button_rect)
        for piece_rect in white_pieces:
            screen.blit(white_piece_image, piece_rect)
        for piece_rect in black_pieces:
            screen.blit(black_piece_image, piece_rect)
        for piece_rect in green_pieces:
            screen.blit(green_piece_image, piece_rect)
            
        if is_pause:
            screen.blit(pause_overlay, pause_overlay_rect)
            screen.blit(play_again_button, play_again_button_rect)
            screen.blit(restart_button, restart_button_rect)
            screen.blit(exit_button, exit_button_rect)
    
    pygame.display.update()
    clock.tick(60)