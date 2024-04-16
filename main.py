import pygame
import sys 
import gif_pygame
import webbrowser

import SixMenMorris.constants as VAR
from SixMenMorris.Button import Button
from SixMenMorris.Board import Board
from SixMenMorris.Piece import Pieces

pygame.init()
screen = pygame.display.set_mode((VAR.WIDTH, VAR.HEIGHT))
pygame.display.set_caption("Six Men's Morris")
pygame.display.set_icon(VAR.ICON)
clock = pygame.time.Clock()
surface = pygame.Surface((VAR.WIDTH, VAR.HEIGHT))
surface.fill(VAR.LIGHTGRAY)

class Overlay():
    def __init__(self, image_page, position):
        self.image = pygame.image.load(image_page).convert_alpha()
        self.rect = self.image.get_rect(center=position)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Load components
background_gif = gif_pygame.load(VAR.BACKGROUNDGIF_PATH)
background = Overlay(VAR.BACKGROUND_PATH, VAR.CENTER)
play_button = Button(VAR.PLAY_PATH, (336, 235)) 
back_button = Button(VAR.BACK_PATH, (214, 467))
next_button = Button(VAR.NEXT_PATH, (514, 467))
start_button = Button(VAR.START_PATH, (340, 467))
instruction1_image = Overlay(VAR.INSTRUCTION1_PATH, VAR.CENTER)
instruction2_image = Overlay(VAR.INSTRUCTION2_PATH, VAR.CENTER)
board = Overlay(VAR.BOARD_PATH, VAR.CENTER)
pause_overlay = Overlay(VAR.PAUSEOVER_PATH, VAR.CENTER)
pause_button = Button(VAR.PAUSE_PATH, (708, 19))
play_again_button = Button(VAR.PLAYAGAIN_PATH, (360, 300))
restart_button = Button(VAR.RESTART_PATH, (239, 300))
exit_button = Button(VAR.EXIT_PATH, (481, 300))
github_button = Button(VAR.GITHUB_PATH, (740, 540))
github_button.transform_scale((40, 40))
board_positions = [Board(position) for position in VAR.board_piece_positions]
white = Button(VAR.WHITEPIECE_PATH, (150, 280))
black = Button(VAR.BLACKPIECE_PATH, (500, 280))
white_pieces = [Pieces(VAR.WHITEPIECE_PATH, pos) for pos in [(708, y) for y in range(100, 494, 66)]]
black_pieces = [Pieces(VAR.BLACKPIECE_PATH, pos) for pos in [(27, y) for y in range(100, 494, 66)]]

def handle_home_state(handle, mouse_pos=None):
    if handle:
        screen.blit(surface, (0,0))
        background_gif.render(screen, (400-background_gif.get_width()*0.5, 300-background_gif.get_height()*0.5))
        play_button.draw(screen)
    else:
        if play_button.is_clicked(mouse_pos):
            VAR.GAME_STATE = 'instruction1'

def handle_instruction_state(handle, page, mouse_pos=None):
    if handle:
        if page == 1:
            screen.blit(surface, (0,0))
            instruction1_image.draw(screen)
            back_button.draw(screen)
            next_button.draw(screen)
        else:
            screen.blit(surface, (0,0))
            instruction2_image.draw(screen)
            back_button.draw(screen)
            next_button.draw(screen)
    else:
        if page == 1:
            if back_button.is_clicked(mouse_pos):
                VAR.GAME_STATE = 'home'
            elif next_button.is_clicked(mouse_pos):
                VAR.GAME_STATE = 'instruction2'
        else:
            if back_button.is_clicked(mouse_pos):
                VAR.GAME_STATE = 'instruction1'
            elif next_button.is_clicked(mouse_pos):
                VAR.GAME_STATE = 'selection'

def handle_select_piece(handle, mouse_pos=None):
    white.transform_scale((150, 150))
    black.transform_scale((150, 150))
    if handle:
        screen.blit(surface, (0,0))
        background.draw(screen)
        start_button.draw(screen)
        white.draw(screen)
        black.draw(screen)
        if white.selected:
            pygame.draw.circle(screen, "blue", white.rect.center, 75, width=3)
            VAR.PLAYER_PIECE = "white"
        if black.selected:
            pygame.draw.circle(screen, "blue", black.rect.center, 75, width=3)
            VAR.PLAYER_PIECE = "black"
    else:
        if start_button.is_clicked(mouse_pos):
            VAR.GAME_STATE = 'board'
        white.update(mouse_pos)
        black.update(mouse_pos)
        if white.clicked:
            white.selected = not white.selected
            black.selected = False  # Deselect black if white is selected
        if black.clicked:
            black.selected = not black.selected
            white.selected = False

def handle_board_state(handle, event=None, mouse_pos=None):
    if handle:
        screen.blit(surface, (0,0))
        board.draw(screen)
        pause_button.draw(screen)
        github_button.draw(screen)
        if VAR.GAME_PHASE == 'opening':
            for boards_pos in board_positions:
                boards_pos.draw_circle(screen, 'darkgray')
            for pieces in white_pieces + black_pieces:
                pieces.draw(screen)
        if VAR.GAME_PHASE == 'middlegame':
            for boards_pos in board_positions:
                boards_pos.draw_circle(screen, 'darkgray')
            for piece in white_pieces + black_pieces:
                if piece.clicked:
                    pygame.draw.circle(screen, "RED", piece.rect.center, 32, width=3)
                piece.draw(screen)
    else:
        if pause_button.is_clicked(mouse_pos):
            VAR.GAME_STATE = 'pause'
        elif github_button.is_clicked(mouse_pos):
            webbrowser.open(VAR.GITHUB_URL)

def handle_pause_state(handle, mouse_pos=None):
    if handle:
        screen.blit(surface, (0,0))
        pause_overlay.draw(screen)
        play_again_button.draw(screen)
        restart_button.draw(screen)
        exit_button.draw(screen)
    else:
        if play_again_button.is_clicked(mouse_pos):
            VAR.GAME_STATE = 'board'
        elif exit_button.is_clicked(mouse_pos):
            VAR.GAME_STATE = 'home'
            reset_board()
        elif restart_button.is_clicked(mouse_pos):
            VAR.GAME_STATE = 'board'
            reset_board()
            
def reset_board():
    VAR.CURRENT_PLAYER = "player1"
    VAR.GAME_PHASE = 'opening'
    for piece, pos in zip(white_pieces, [(708, y) for y in range(100, 494, 66)]):
        piece.rect.topleft = pos
    for piece, pos in zip(black_pieces, [(27, y) for y in range(100, 494, 66)]):
        piece.rect.topleft = pos

def main():
    loop = True
    while loop:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VAR.GAME_STATE == 'home':
                    handle_home_state(False, mouse_pos)
                elif VAR.GAME_STATE == 'instruction1':
                    handle_instruction_state(False, 1, mouse_pos)
                elif VAR.GAME_STATE == 'instruction2':
                    handle_instruction_state(False, 2, mouse_pos)
                elif VAR.GAME_STATE =='selection':
                    handle_select_piece(False, mouse_pos)
                elif VAR.GAME_STATE == 'board':
                    handle_board_state(False, event, mouse_pos)
                elif VAR.GAME_STATE == 'pause':
                    handle_pause_state(False, mouse_pos)
            
        if VAR.GAME_STATE == 'home':
            handle_home_state(True)
        elif VAR.GAME_STATE == 'instruction1':
            handle_instruction_state(True, 1)
        elif VAR.GAME_STATE == 'instruction2':
            handle_instruction_state(True, 2)
        elif VAR.GAME_STATE == 'selection':
            handle_select_piece(True)
        elif VAR.GAME_STATE == 'board':
            handle_board_state(True)
        elif VAR.GAME_STATE == 'pause':
            handle_pause_state(True)
            
        pygame.display.update()
        clock.tick(VAR.FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()