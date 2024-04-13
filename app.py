"""
1. Need to add piece tracker when moving the pieces
2. Switching of players
3. Add another page for choosing what piece the player would choose
"""

import pygame
import sys 
import gif_pygame
import webbrowser

import classes
import variable

pygame.init()
screen = pygame.display.set_mode((variable.WIDTH, variable.HEIGHT))
pygame.display.set_caption("Six Men Morris")
clock = pygame.time.Clock()
surface = pygame.Surface((variable.WIDTH, variable.HEIGHT))
surface.fill(variable.LIGHTGRAY)

# Load images
## Background
background_gif = gif_pygame.load(variable.background_path)
instruction1_image = classes.Overlay(variable.instruction1_path, variable.CENTER)
instruction2_image = classes.Overlay(variable.instruction2_path, variable.CENTER)
board = classes.Overlay(variable.board_path, variable.CENTER)
pause_overlay = classes.Overlay(variable.pauseOver_path, variable.CENTER)

## Pieces
white_pieces = [classes.Pieces(variable.white_piece_path, pos) for pos in [(708, y) for y in range(100, 494, 66)]]
black_pieces = [classes.Pieces(variable.black_piece_path, pos) for pos in [(27, y) for y in range(100, 494, 66)]]
for pos in [(708, y) for y in range(100, 494, 66)]:
    variable.WHITE_PIECES_POSITIONS.append(pos)
for pos in [(27, y) for y in range(100, 494, 66)]:
    variable.BLACK_PIECES_POSITIONS.append(pos)

## Buttons
play_button = classes.Button(variable.play_path, (336, 235))
back_button = classes.Button(variable.back_path, (214, 467))
next_button = classes.Button(variable.next_path, (514, 467))
start_button = classes.Button(variable.start_path, (449, 467))
pause_button = classes.Button(variable.pause_path, (708, 19))
play_again_button = classes.Button(variable.play_again_path, (360, 300))
restart_button = classes.Button(variable.restart_path, (239, 300))
exit_button = classes.Button(variable.exit_path, (481, 300))
github_button = classes.Button(variable.github_path, (740, 540))
github_button.transform_scale((40, 40))

board_positions = [classes.BoardPosition(position) for position in variable.board_piece_positions]

# Functions 
def reset_board():
    # Reset white pieces to original positions
    for piece, pos in zip(white_pieces, [(708, y) for y in range(100, 494, 66)]):
        piece.rect.topleft = pos
    # Reset black pieces to original positions
    for piece, pos in zip(black_pieces, [(27, y) for y in range(100, 494, 66)]):
        piece.rect.topleft = pos
    # Reset the board position occupied by
    for board_pos in board_positions:
        board_pos.occupied = False

while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if variable.GAME_STATE == 'home':
                if play_button.is_clicked(mouse_pos):
                    variable.GAME_STATE = 'instruction1'
            elif variable.GAME_STATE == 'instruction1':
                if back_button.is_clicked(mouse_pos):
                    variable.GAME_STATE = 'home'
                elif next_button.is_clicked(mouse_pos):
                    variable.GAME_STATE = 'instruction2'
            elif variable.GAME_STATE == 'instruction2':
                if back_button.is_clicked(mouse_pos):
                    variable.GAME_STATE = 'instruction1'
                elif start_button.is_clicked(mouse_pos):
                    variable.GAME_STATE = 'board'
            elif variable.GAME_STATE == 'board':
                if pause_button.is_clicked(mouse_pos):
                    variable.GAME_STATE = 'pause'
                elif github_button.is_clicked(mouse_pos):
                    webbrowser.open(variable.GITHUB_URL)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a board position is clicked
                    for board_pos in board_positions:
                        if board_pos.is_clicked(event.pos):
                            # Find the selected piece
                            for piece in white_pieces + black_pieces:
                                if piece.clicked:
                                    # Move the selected piece to the clicked board position
                                    if not board_pos.occupied:
                                        piece.rect.center = board_pos.position
                                        board_pos.occupied = True  # Mark the position as occupied
                                    else:
                                        # Handle the case where the position is already occupied
                                        board_pos.occupied = False
                                        print("Position already occupied!")
            elif variable.GAME_STATE == 'pause':
                if play_again_button.is_clicked(mouse_pos):
                    variable.GAME_STATE = 'board'
                elif exit_button.is_clicked(mouse_pos):
                    variable.GAME_STATE = 'home'
                    reset_board()
                elif restart_button.is_clicked(mouse_pos):
                    variable.GAME_STATE = 'board'
                    reset_board()
            
            for piece in white_pieces + black_pieces:
                piece.update(event)

    if variable.GAME_STATE == 'home':
        screen.blit(surface, (0,0))
        background_gif.render(screen, (400-background_gif.get_width()*0.5, 300-background_gif.get_height()*0.5))
        play_button.draw(screen)
    elif variable.GAME_STATE == 'instruction1':
        screen.blit(surface, (0,0))
        instruction1_image.draw(screen)
        back_button.draw(screen)
        next_button.draw(screen)
    elif variable.GAME_STATE == 'instruction2':
        screen.blit(surface, (0,0))
        instruction2_image.draw(screen)
        back_button.draw(screen)
        start_button.draw(screen)
    elif variable.GAME_STATE == 'board':
        screen.blit(surface, (0,0))
        board.draw(screen)
        pause_button.draw(screen)
        github_button.draw(screen)
        for piece in white_pieces:
            if piece.clicked:
                pygame.draw.circle(screen, "RED", piece.rect.center, 32, width=3)
            piece.draw(screen)
        for piece in black_pieces:
            if piece.clicked:
                pygame.draw.circle(screen, "RED", piece.rect.center, 32, width=3)
            piece.draw(screen)
        for boards_pos in board_positions:
            boards_pos.draw_circle(screen)
    elif variable.GAME_STATE == 'pause':
        screen.blit(surface, (0,0))
        pause_overlay.draw(screen)
        play_again_button.draw(screen)
        restart_button.draw(screen)
        exit_button.draw(screen)
    pygame.display.update()
    clock.tick(60)