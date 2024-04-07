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

pygame.init()

# Constants
HEIGHT = 600
WIDTH = 800
ICON_HEIGHT = 84
ICON_WEIGHT = 84
LIGHTGRAY = "#D9D9D9"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Six Men Morris")
clock = pygame.time.Clock()

class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def transform_scale(self, sizes):
        self.image = pygame.transform.scale(self.image, sizes)
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
        
class Overlay(pygame.sprite.Sprite):
    def __init__(self, image_page, position):
        super().__init__()
        self.image = pygame.image.load(image_page).convert_alpha()
        self.rect = self.image.get_rect(center=position)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Pieces(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.clicked = False
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_clicked(pygame.mouse.get_pos()):
            self.clicked = True
        else:
            self.clicked = False

class BoardPosition:
    def __init__(self, position):
        self.rect = pygame.Rect(position[0] - 40, position[1] - 40, 80, 80)
        self.occupied = False  # Initially, the position is not occupied

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

surface = pygame.Surface((WIDTH, HEIGHT))
surface.fill(LIGHTGRAY)

# Load images
## Background
background_gif = gif_pygame.load("./assets/fox.gif")
instruction1_image = Overlay("./assets/instruction1.png", (WIDTH*0.5, HEIGHT*0.5))
instruction2_image = Overlay("./assets/instruction2.png", (WIDTH*0.5, HEIGHT*0.5))
board = Overlay("./assets/board.png", (WIDTH*0.5, HEIGHT*0.5))
pause_overlay = Overlay("./assets/icons8-pause.png", (WIDTH*0.5, HEIGHT*0.5))

## Buttons
play_button = Button("./assets/icons8-play-128.png", (336, 235))
back_button = Button("./assets/icons8-rewind-64.png", (214, 467))
next_button = Button("./assets/icons8-forward-64.png", (514, 467))
start_button = Button("./assets/start_button.png", (449, 467))
pause_button = Button("./assets/icons8-pause-64.png", (708, 19))
play_again_button = Button("./assets/icons8-play-80.png", (360, 300))
restart_button = Button("./assets/icons8-restart-80.png", (239, 300))
exit_button = Button("./assets/icons8-exit-80.png", (481, 300))
github_button = Button("./assets/icons8-github-64.png", (740, 540))

## Pieces
white_pieces = [Pieces("./assets/icons8-circle-64.png", pos) for pos in [(708, y) for y in range(100, 494, 66)]]
black_pieces = [Pieces("./assets/icons8-circle-64 (1).png", pos) for pos in [(27, y) for y in range(100, 494, 66)]]

board_piece_positions = [
    (197, 97),
    (398, 97),
    (600, 97),
    (297, 196),
    (398, 196),
    (499, 196),
    (197, 298),
    (297, 298),
    (499, 298),
    (600, 298),
    (297, 400),
    (398, 400),
    (499, 400),
    (197, 501),
    (398, 501),
    (600, 501)
]
board_positions = [BoardPosition(position) for position in board_piece_positions]

# Transform
github_button.transform_scale((40, 40))
github_url = "https://github.com/D3struf/Six-Men-s-Morris.git"

# Game States
home_page = False
instruction1_page = False
instruction2_page = False
pause_page = False
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
                if play_button.is_clicked(mouse_pos):
                    home_page = False
                    instruction1_page = True
            elif instruction1_page:
                if back_button.is_clicked(mouse_pos):
                    instruction1_page = False
                    home_page = True
                elif next_button.is_clicked(mouse_pos):
                    instruction1_page = False
                    instruction2_page = True
            elif instruction2_page:
                if back_button.is_clicked(mouse_pos):
                    instruction2_page = False
                    instruction1_page = True
                elif start_button.is_clicked(mouse_pos):
                    instruction2_page = False
                    board_page = True
            elif board_page:
                if pause_button.is_clicked(mouse_pos):
                    board_page = False
                    pause_page = True
                elif github_button.is_clicked(mouse_pos):
                    webbrowser.open(github_url)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a board position is clicked
                    for board_pos in board_positions:
                        if board_pos.is_clicked(event.pos):
                            # Find the selected piece
                            for piece in white_pieces:
                                if piece.clicked:
                                    # Move the selected piece to the clicked board position
                                    if not board_pos.occupied:
                                        piece.rect.center = board_pos.rect.center
                                        board_pos.occupied = True  # Mark the position as occupied
                                    else:
                                        # Handle the case where the position is already occupied
                                        print("Position already occupied!")
            elif pause_page:
                if play_again_button.is_clicked(mouse_pos):
                    pause_page = False
                    board_page = True
                elif exit_button.is_clicked(mouse_pos):
                    pause_page = False
                    home_page = True
            
            for piece in white_pieces:
                piece.update(event)

    if home_page:
        screen.blit(surface, (0,0))
        background_gif.render(screen, (400-background_gif.get_width()*0.5, 300-background_gif.get_height()*0.5))
        play_button.draw(screen)
    elif instruction1_page:
        screen.blit(surface, (0,0))
        instruction1_image.draw(screen)
        back_button.draw(screen)
        next_button.draw(screen)
    elif instruction2_page:
        screen.blit(surface, (0,0))
        instruction2_image.draw(screen)
        back_button.draw(screen)
        start_button.draw(screen)
    elif board_page:
        screen.blit(surface, (0,0))
        board.draw(screen)
        pause_button.draw(screen)
        github_button.draw(screen)
        for piece in white_pieces:
            if piece.clicked:
                pygame.draw.circle(screen, "RED", piece.rect.center, 32, width=3)
            piece.draw(screen)
        for piece in black_pieces:
            piece.draw(screen)
    elif pause_page:
        screen.blit(surface, (0,0))
        pause_overlay.draw(screen)
        play_again_button.draw(screen)
        restart_button.draw(screen)
        exit_button.draw(screen)
    pygame.display.update()
    clock.tick(60)