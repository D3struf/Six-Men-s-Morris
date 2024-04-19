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

# Handle States
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
        first_move()

def first_move():
    if VAR.PLAYER_PIECE == "white":
        VAR.CURRENT_PLAYER = 'player1'
    elif VAR.PLAYER_PIECE == "black":
        VAR.CURRENT_PLAYER = 'ai'

def switch_player():
    VAR.CURRENT_PLAYER = 'ai' if VAR.CURRENT_PLAYER == 'player1' else 'player1'

def player_piece(placed, player, game):
    if game == 'opening':
        if VAR.PLAYER_PIECE == "white":
            if player == 'player1':
                piece = white_pieces[placed]
            elif player == 'ai':
                piece = black_pieces[placed]
        elif VAR.PLAYER_PIECE == "black":
            if player == 'player1':
                piece = black_pieces[placed]
            elif player == 'ai':
                piece = white_pieces[placed]
        return piece
    if game == 'middlegame':
        if VAR.PLAYER_PIECE == "white":
            if player == 'player1':
                pieces = white_pieces
            elif player == 'ai':
                pieces = black_pieces
        elif VAR.PLAYER_PIECE == "black":
            if player == 'player1':
                pieces = black_pieces
            elif player == 'ai':
                pieces = white_pieces
        return pieces

# Opening Game
def opening_game(player, board_pos):
    placed = VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['placed']
    # if all of the pieces has been placed
    if placed >= 6 or VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['in_board'] == 0:
        return
    
    piece_to_move = player_piece(placed, player, 'opening')
            
    piece_to_move.move(board_pos.position)  # Move the piece to the selected board position
    VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'].add(piece_to_move.current_position)  # Update piece position in the dictionary
    VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['placed'] += 1  # Update the count of placed pieces
    VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['in_board'] -= 1  # Update the count of placed pieces
    board_pos.occupied = True

def check_mill_formed(player):
    if VAR.GAME_PHASE == 'opening':
        if VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['placed'] == 6:
            return
    mill = VAR.PLAYER_DICT[player]['positions']
    for possible_mill in VAR.POSSIBLE_MILLS:
        mills = set(possible_mill)
        if len(mill) >= 3 and mills.issubset(mill):
            if not mills.issubset(VAR.PLAYER_DICT[player]['previous_mill']):
                print("MILL!!!!")
                VAR.PLAYER_DICT[player]['previous_mill'].update(mills)
                VAR.PLAYER_DICT[player]['mill_formed'] = mills
                VAR.IS_MILL = True
        else: VAR.CIRCLES_TO_DRAW = []  # Clear circles to draw if no mill is formed

def remove_piece(player, game):
    if player == 'player1':
        # pieces = white_pieces if VAR.PLAYER_PIECE == "white" else black_pieces
        opponent_pieces = black_pieces if VAR.PLAYER_PIECE == "white" else white_pieces
    else:
        # pieces = black_pieces if VAR.PLAYER_PIECE == "black" else white_pieces
        opponent_pieces = black_pieces if VAR.PLAYER_PIECE == "black" else white_pieces
    
    # get possible pieces to be removed
    player_positions = set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'])
    prev_mill = set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['previous_mill'])
    possible_pieces_to_remove = player_positions - prev_mill
    
    VAR.CIRCLES_TO_DRAW = [position for position in possible_pieces_to_remove]
    
    if game == 'opening':
        # if mouse clicked is near the position
        mouse_pos = pygame.mouse.get_pos()
        for board_pos in board_positions:
            if board_pos.is_clicked(mouse_pos) and board_pos.occupied:
                for opponent_piece in opponent_pieces:
                    if opponent_piece.is_clicked(mouse_pos):
                        opponent_pieces.remove(opponent_piece)
                        VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'].remove(opponent_piece.current_position)
                        board_pos.occupied = False
                        VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['placed'] -= 1
                        VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['num_pieces'] -= 1
                        VAR.IS_MILL = False
                        VAR.PLAYER_DICT[player]['mill_formed'] = set()
                        print('REMOVED', VAR.PLAYER_DICT)
                        break
    elif game == 'middlegame':
        print('REMOVING player')
        mouse_pos = pygame.mouse.get_pos()
        
        for opponent_piece in opponent_pieces:
            print('OPPONENT PIECES', opponent_piece.current_position)
            if opponent_piece.is_clicked(mouse_pos):
                opponent_pieces.remove(opponent_piece)
                VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'].remove(opponent_piece.current_position)
                # board_pos.occupied = False
                VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['placed'] -= 1
                VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['num_pieces'] -= 1
                VAR.IS_MILL = False
                VAR.PLAYER_DICT[player]['mill_formed'] = set()
                print('REMOVED', VAR.PLAYER_DICT)
                break
        
def place_pieces(event):
    for board_pos in board_positions:
        if board_pos.is_clicked(event.pos):
            if board_pos.occupied:
                print("Position already occupied!")
                break
            
            if VAR.GAME_PHASE == 'opening':
                opening_game(VAR.CURRENT_PLAYER, board_pos)
                check_mill_formed(VAR.CURRENT_PLAYER)
                switch_player()

# Middle Game
def middle_game(player, mouse_pos):    
    pieces = player_piece(0, player, 'middlegame') 
    pieces_loc = [pos.current_position for pos in pieces]
    for board_pos in board_positions:
        if board_pos.is_clicked(mouse_pos):
            if board_pos.position in pieces_loc:
                VAR.SELECTED_PIECE = selected_piece(pieces, board_pos)
                show_possible_moves(board_pos)
                board_pos.occupied = False
            elif board_pos.position in VAR.BOARD_TO_DRAW:
                move_piece_to(board_pos)
                break

def check_mill_deformed(player):
    mill = VAR.PLAYER_DICT[player]['positions']
    for possible_mill in VAR.POSSIBLE_MILLS:
        mills = set(possible_mill)
        if not mills.issubset(mill) and not mills.issubset(VAR.PLAYER_DICT[player]['previous_mill']):
            y = VAR.PLAYER_DICT[player]['previous_mill'].difference(mills) 
            VAR.PLAYER_DICT[player]['previous_mill'].difference_update(y)

def move_piece_to(board_pos):
    """Move the selected piece to the clicked board position"""
    selected_piece = VAR.SELECTED_PIECE
    for position in VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions']:
        if position == selected_piece.current_position:
            # update the current players positions in the dictionary
            VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'].remove(position)
            VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'].add(board_pos.position)
    selected_piece.move(board_pos.position)
    board_pos.occupied = True
    VAR.BOARD_TO_DRAW = []
    check_mill_formed(VAR.CURRENT_PLAYER)
    check_mill_deformed(VAR.CURRENT_PLAYER)
    print('moved to', VAR.PLAYER_DICT[VAR.CURRENT_PLAYER])
    switch_player()
    # if VAR.IS_MILL:
    #     other_player = 'player1' if VAR.CURRENT_PLAYER == 'ai' else 'ai'
    #     remove_piece(other_player, 'middlegame')

def selected_piece(pieces, board_pos):
    """return the piece at the given board position"""
    for piece in pieces:
        if piece.current_position == board_pos.position:
            return piece

def show_possible_moves(selected_piece):
    """set possible board positions of the piece to move"""
    possible_moves = []
    if selected_piece.position in VAR.POSSIBLE_MOVES:
        moves = VAR.POSSIBLE_MOVES[selected_piece.position]
        for move in moves:
            for board_pos in board_positions:
                if board_pos.position == move and not board_pos.occupied:
                    # board_pos.draw_circle(screen, 'green')
                    possible_moves.append(move)
    VAR.BOARD_TO_DRAW = possible_moves

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
            for position in VAR.BOARD_TO_DRAW:
                pygame.draw.circle(screen, "RED", position, 14, width=4)
            for piece in white_pieces + black_pieces:
                piece.draw(screen)
        if VAR.IS_MILL:
            for position in VAR.CIRCLES_TO_DRAW:
                pygame.draw.circle(screen, "RED", position, 32, width=3)
    else:
        if pause_button.is_clicked(mouse_pos):
            VAR.GAME_STATE = 'pause'
        elif github_button.is_clicked(mouse_pos):
            webbrowser.open(VAR.GITHUB_URL)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            total_placed = VAR.PLAYER_DICT['player1']['in_board'] + VAR.PLAYER_DICT['ai']['in_board']
            if total_placed == 0 and (len(VAR.CIRCLES_TO_DRAW) == 0 or len(VAR.CIRCLES_TO_DRAW) == 1):
                VAR.GAME_PHASE ='middlegame'
            if VAR.GAME_PHASE == 'opening':
                place_pieces(event)
                if VAR.IS_MILL:
                    other_player = 'player1' if VAR.CURRENT_PLAYER == 'ai' else 'ai'
                    remove_piece(other_player, 'opening')
            elif VAR.GAME_PHASE =='middlegame':
                print('player: ', VAR.CURRENT_PLAYER)
                print('circles to draw: ', VAR.CIRCLES_TO_DRAW)
                middle_game(VAR.CURRENT_PLAYER, mouse_pos)
                if VAR.IS_MILL:
                    other_player = 'player1' if VAR.CURRENT_PLAYER == 'ai' else 'ai'
                    remove_piece(VAR.CURRENT_PLAYER, 'middlegame')
            elif VAR.GAME_PHASE == 'lategame':
                print("Late Game!")

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
    VAR.PLAYER_PIECE = 'white'
    VAR.CIRCLES_TO_DRAW = []
    VAR.IS_MILL = False
    for _, data in VAR.PLAYER_DICT.items():
        data['in_board'] = 6
        data['num_pieces'] = 6
        data['placed'] = 0
        data['positions'] = set()
        data['previous_mill'] = set()
        data['mill_formed'] = set()

    global white_pieces, black_pieces
    white_pieces = []
    black_pieces = []
    white_pieces = [Pieces(VAR.WHITEPIECE_PATH, pos) for pos in [(708, y) for y in range(100, 494, 66)]]
    black_pieces = [Pieces(VAR.BLACKPIECE_PATH, pos) for pos in [(27, y) for y in range(100, 494, 66)]]
    for piece, pos in zip(white_pieces, [(708, y) for y in range(100, 494, 66)]):
        piece.rect.topleft = pos
    for piece, pos in zip(black_pieces, [(27, y) for y in range(100, 494, 66)]):
        piece.rect.topleft = pos
    for board_pos in board_positions:
        board_pos.occupied = False
    pygame.display.update()

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