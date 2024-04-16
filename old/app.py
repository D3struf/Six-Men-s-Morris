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
from Board import Board

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

board_positions = [Board(position) for position in variable.board_piece_positions]

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
    variable.CURRENT_PLAYER = "player1"
    white_pieces_copy.clear()
    black_pieces_copy.clear()

def switch_player():
    variable.CURRENT_PLAYER = 'player2' if variable.CURRENT_PLAYER == 'player1' else 'player1'

def handle_home_state(mouse_pos):
    if play_button.is_clicked(mouse_pos):
        variable.GAME_STATE = 'instruction1'

def handle_instruction1_state(mouse_pos):
    if back_button.is_clicked(mouse_pos):
        variable.GAME_STATE = 'home'
    elif next_button.is_clicked(mouse_pos):
        variable.GAME_STATE = 'instruction2'

def handle_instruction2_state(mouse_pos):
    if back_button.is_clicked(mouse_pos):
        variable.GAME_STATE = 'instruction1'
    elif start_button.is_clicked(mouse_pos):
        variable.GAME_STATE = 'board'

def handle_board_state(mouse_pos, event):
    if pause_button.is_clicked(mouse_pos):
        variable.GAME_STATE = 'pause'
    elif github_button.is_clicked(mouse_pos):
        webbrowser.open(variable.GITHUB_URL)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        total = sum(len(coords) for coords in variable.PLAYERS_POSITION.values())
        if total < 12:
            handle_place_pieces(event)
        else:
            handle_piece_movement(mouse_pos, event)
            

## OPENING GAME
white_pieces_copy = [piece for piece in white_pieces]
black_pieces_copy = [piece for piece in black_pieces]
def handle_place_pieces(event):
    def move_piece_to_board_position(board_pos):
        if variable.CURRENT_PLAYER == 'player1':
            if valid_move(board_pos, 'player1'):
                piece = white_pieces_copy.pop()  # Get the last white piece copy
                piece.move(board_pos.position)
                update_piece_position(piece, board_pos)
                switch_player()
        else:
            if valid_move(board_pos, 'player2'):
                piece = black_pieces_copy.pop()  # Get the last black piece copy
                piece.move(board_pos.position)
                update_piece_position(piece, board_pos)
                switch_player()
                
    def update_piece_position(piece, board_pos):
        old_position = piece.current_position
        piece.rect.center = board_pos.position
        board_pos.occupied = True
        piece.current_position = board_pos.position
        if old_position in variable.PLAYERS_POSITION[variable.CURRENT_PLAYER]:
            variable.PLAYERS_POSITION[variable.CURRENT_PLAYER].remove(old_position)
        variable.PLAYERS_POSITION[variable.CURRENT_PLAYER].append(piece.current_position)
        print("PLAYERS POSITION: ", variable.PLAYERS_POSITION)
    
    for board_pos in board_positions:
        if board_pos.is_clicked(event.pos):
            if board_pos.occupied:
                print("Position already occupied! 1")
                break
            move_piece_to_board_position(board_pos)

## MIDDLE GAME
def handle_piece_movement(mouse_pos, event):
    for board_pos in board_positions:
        if board_pos.is_clicked(event.pos):
            if board_pos.occupied:
                print("Position already occupied! 1")
                break
            handle_player_pieces(board_pos)

def handle_player_pieces(board_pos):
    if variable.CURRENT_PLAYER == 'player1':
        for piece in white_pieces:
            if piece.clicked:
                handle_piece_movement_player(piece, board_pos, "player1")
    else:
        for piece in black_pieces:
            if piece.clicked:
                handle_piece_movement_player(piece, board_pos, "player2")

def handle_piece_movement_player(piece, board_pos, player):
    if piece.current_position != board_pos.position:
        if valid_move(board_pos, player):
            piece.move(board_pos.position)
            update_piece_position(piece, board_pos)
            switch_player()
        else:
            update_piece_position_same_player(piece, board_pos, player)
    else:
        print("Position already occupied! 2")

def valid_move(board_pos, player):
    return board_pos not in variable.PLAYERS_POSITION['player1'] + variable.PLAYERS_POSITION['player2'] and len(variable.PLAYERS_POSITION[player]) < 6

def update_piece_position(piece, board_pos):
    old_position = piece.current_position
    piece.rect.center = board_pos.position
    board_pos.occupied = True
    piece.current_position = board_pos.position
    if old_position in variable.PLAYERS_POSITION[variable.CURRENT_PLAYER]:
        variable.PLAYERS_POSITION[variable.CURRENT_PLAYER].remove(old_position)
    variable.PLAYERS_POSITION[variable.CURRENT_PLAYER].append(piece.current_position)
    board_pos.position = old_position
    board_pos.occupied = False
    piece.clicked = False
    print("PLAYERS POSITION: ", variable.PLAYERS_POSITION)

def update_piece_position_same_player(piece, board_pos, player):
    old_position = piece.current_position
    old_position_index = variable.PLAYERS_POSITION[player].index(piece.current_position)
    variable.PLAYERS_POSITION[player][old_position_index] = board_pos.position
    piece.move(board_pos.position)
    board_pos.position = old_position
    board_pos.occupied = False
    piece.clicked = False
    switch_player()
    print("PLAYERS POSITION: ", variable.PLAYERS_POSITION)

def show_possible_moves(selected_piece):
    if selected_piece.current_position in variable.POSSIBLE_MOVES:
        moves = variable.POSSIBLE_MOVES[selected_piece.current_position]
        for move in moves:
            for board_pos in board_positions:
                if board_pos.position == move:
                    board_pos.draw_circle(screen)

# In-game Real Time Checking for Mill Formations
def check_mill_formation():
    variable.check_mill = False
    for mill, _ in variable.POSSIBLE_MILLS.items():
        for player, positions in variable.PLAYERS_POSITION.items():
            if all(pos in positions for pos in mill):
                if mill not in variable.PLAYERS_MILL_FORMATION[player]:
                    print(f"Mill formed by {player}: {mill}")
                    variable.PLAYERS_MILL_FORMATION[player] = mill
                    return True
    return False

def piece_removal(player):
    if player == 'player1':
        for piece in white_pieces:
            if piece.clicked and piece.current_position not in variable.POSSIBLE_MILLS:
                pygame.draw.circle(screen, "RED", piece.rect.center, 32, width=3)
                remove(piece)
                return
    else:
        for piece in black_pieces:
            if piece.clicked and piece.current_position not in variable.POSSIBLE_MILLS:
                pygame.draw.circle(screen, "RED", piece.rect.center, 32, width=3)
                remove(piece)
                return
    
def remove(piece):
    if piece in white_pieces: white_pieces.remove(piece) 
    else: black_pieces.remove(piece)
    variable.check_mill = False
    for board_pos in board_positions:
        if board_pos.position == piece.current_position:
            board_pos.occupied = False
            break

def clear_mill_circles(screen):
    screen.blit(surface, (0,0))
    board.draw(screen)
    pause_button.draw(screen)
    github_button.draw(screen)
    total = sum(len(coords) for coords in variable.PLAYERS_POSITION.values())
    if total < 12:
        for boards_pos in board_positions:
            boards_pos.draw_circle(screen)
    else:
        for piece in white_pieces + black_pieces:
            if piece.clicked:
                show_possible_moves(piece)
    for piece in white_pieces:
        if piece.clicked:
            pygame.draw.circle(screen, "RED", piece.rect.center, 32, width=3)
        piece.draw(screen)
    for piece in black_pieces:
        if piece.clicked:
            pygame.draw.circle(screen, "RED", piece.rect.center, 32, width=3)
        piece.draw(screen)
    pygame.display.update()

def handle_pause_state(mouse_pos):
    if play_again_button.is_clicked(mouse_pos):
        variable.GAME_STATE = 'board'
    elif exit_button.is_clicked(mouse_pos):
        variable.GAME_STATE = 'home'
        reset_board()
    elif restart_button.is_clicked(mouse_pos):
        variable.GAME_STATE = 'board'
        reset_board()


while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if variable.GAME_STATE == 'home':
                handle_home_state(mouse_pos)
            elif variable.GAME_STATE == 'instruction1':
                handle_instruction1_state(mouse_pos)
            elif variable.GAME_STATE == 'instruction2':
                handle_instruction2_state(mouse_pos)
            elif variable.GAME_STATE == 'board':
                handle_board_state(mouse_pos, event)
                if check_mill_formation(): variable.check_mill = True
            elif variable.GAME_STATE == 'pause':
                handle_pause_state(mouse_pos)
            
            if variable.CURRENT_PLAYER == 'player1':
                for piece in white_pieces:
                    piece.update(event)
            else:
                for piece in black_pieces:
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
        total = sum(len(coords) for coords in variable.PLAYERS_POSITION.values())
        if total < 12:
            for boards_pos in board_positions:
                boards_pos.draw_circle(screen)
        else:
            for piece in white_pieces + black_pieces:
                if piece.clicked:
                    show_possible_moves(piece)
        for piece in white_pieces:
            if piece.clicked:
                pygame.draw.circle(screen, "RED", piece.rect.center, 32, width=3)
            piece.draw(screen)
        for piece in black_pieces:
            if piece.clicked:
                pygame.draw.circle(screen, "RED", piece.rect.center, 32, width=3)
            piece.draw(screen)
        if variable.check_mill:
            piece_removal(variable.CURRENT_PLAYER)
            other_player = 'player2' if variable.CURRENT_PLAYER == 'player1' else 'player1'
            variable.PLAYERS_PREVIOUS_MILL = variable.PLAYERS_MILL_FORMATION[other_player]
            print(variable.PLAYERS_MILL_FORMATION[other_player])
            for mill in variable.PLAYERS_PREVIOUS_MILL:
                if mill not in variable.PLAYERS_MILL_FORMATION[variable.CURRENT_PLAYER]:
                    pygame.draw.circle(screen, "blue", mill, 32, width=3)
    elif variable.GAME_STATE == 'pause':
        screen.blit(surface, (0,0))
        pause_overlay.draw(screen)
        play_again_button.draw(screen)
        restart_button.draw(screen)
        exit_button.draw(screen)
    pygame.display.update()
    clock.tick(60)
    