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
confetti = gif_pygame.load(VAR.CONFETTI)
board_positions = [Board(position) for position in VAR.board_piece_positions]
white = Button(VAR.WHITEPIECE_PATH, (150, 280))
black = Button(VAR.BLACKPIECE_PATH, (500, 280))
white_pieces = [Pieces(VAR.WHITEPIECE_PATH, pos) for pos in [(708, y) for y in range(100, 494, 66)]]
black_pieces = [Pieces(VAR.BLACKPIECE_PATH, pos) for pos in [(27, y) for y in range(100, 494, 66)]]

def text_display(text, font_color, position, font_size):
    def text_font(size):
        return pygame.font.SysFont('googlesansdisplay', size)
    
    font = text_font(font_size)
    width, height = position
    text_surface = font.render(text, True, font_color)
    text_rect = text_surface.get_rect(center=(width, height))
    screen.blit(text_surface, text_rect)

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

def handle_winner_state(handle, mouse_pos=None):
    play_again_button = Button(VAR.PLAYAGAIN_PATH, (250, 300))
    exit_button = Button(VAR.EXIT_PATH, (250, 400))
    if handle:
        other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
        screen.blit(surface, (0,0))
        confetti.render(screen, (400-background_gif.get_width()*0.5, 300-background_gif.get_height()*0.5))
        text_display(f'WINNER: {other_player}', 'black', (400, 200), 72)
        play_again_button.draw(screen)
        exit_button.draw(screen)
        text_display('Play Again', 'blue', (450, 340), 32)
        text_display('Exit', 'red', (400, 440), 32)
    else:
        if play_again_button.is_clicked(mouse_pos):
            VAR.GAME_STATE = 'board'
        elif exit_button.is_clicked(mouse_pos):
            VAR.GAME_STATE = 'home'
            reset_board()

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

def first_move():
    if VAR.PLAYER_PIECE == "white":
        VAR.CURRENT_PLAYER = 'Player'
    elif VAR.PLAYER_PIECE == "black":
        VAR.CURRENT_PLAYER = 'AI'

def switch_player():
    VAR.CURRENT_PLAYER = 'AI' if VAR.CURRENT_PLAYER == 'Player' else 'Player'

def player_piece(placed, player, game):
    if game == 'opening':
        if VAR.PLAYER_PIECE == "white":
            if player == 'Player':
                piece = white_pieces[placed]
            elif player == 'AI':
                piece = black_pieces[placed]
        elif VAR.PLAYER_PIECE == "black":
            if player == 'Player':
                piece = black_pieces[placed]
            elif player == 'AI':
                piece = white_pieces[placed]
        return piece
    if game == 'middlegame' or game == 'lategame':
        if VAR.PLAYER_PIECE == "white":
            if player == 'Player':
                pieces = white_pieces
            elif player == 'AI':
                pieces = black_pieces
        elif VAR.PLAYER_PIECE == "black":
            if player == 'Player':
                pieces = black_pieces
            elif player == 'AI':
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
                VAR.PLAYER_DICT[player]['previous_mill'].update(mills)
                VAR.PLAYER_DICT[player]['mill_formed'] = mills
                VAR.IS_MILL = True
        else: VAR.CIRCLES_TO_DRAW = []  # Clear circles to draw if no mill is formed
    # print('MILL FORMED: ', VAR.PLAYER_DICT[player]['mill_formed'])
    # print('PREVIOUS MILL FORMED: ', VAR.PLAYER_DICT[player]['previous_mill'])

def remove_piece(player, game):
    if player == 'Player':
        # pieces = white_pieces if VAR.PLAYER_PIECE == "white" else black_pieces
        opponent_pieces = black_pieces if VAR.PLAYER_PIECE == "white" else white_pieces
    else:
        # pieces = black_pieces if VAR.PLAYER_PIECE == "black" else white_pieces
        opponent_pieces = black_pieces if VAR.PLAYER_PIECE == "black" else white_pieces
    
    if game == 'opening':
        # get possible pieces to be removed
        player_positions = set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'])
        prev_mill = set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['previous_mill'])
        
        if VAR.IS_MILL:
            possible_pieces_to_remove = player_positions - prev_mill
        else:
            possible_pieces_to_remove = player_positions
        
        VAR.CIRCLES_TO_DRAW = [position for position in possible_pieces_to_remove]
        print('circles to draw', VAR.CIRCLES_TO_DRAW)
        # if mouse clicked is near the position
        # for event in pygame.event.get():
            # if event.type == pygame.MOUSEBUTTONDOWN:
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
                        # print('REMOVED', VAR.PLAYER_DICT)
                        VAR.CIRCLES_TO_DRAW = []
                        break
    elif game == 'middlegame':
        print('REMOVING player')
        if VAR.IS_MILL:
            mouse_pos = pygame.mouse.get_pos()
            for board_pos in board_positions:
                if board_pos.is_clicked(mouse_pos):
                    for opponent_piece in opponent_pieces:
                        if opponent_piece.current_position == board_pos.position:
                            if board_pos.position in VAR.CIRCLES_TO_DRAW:
                                opponent_pieces.remove(opponent_piece)
                                VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'].remove(opponent_piece.current_position)
                                board_pos.occupied = False
                                VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['num_pieces'] -= 1
                                VAR.CIRCLES_TO_DRAW = []
                                return
                            break
    print('DONE REMOVING')

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
                show_possible_moves(board_pos, 'middlegame')
                board_pos.occupied = False
            elif board_pos.position in VAR.BOARD_TO_DRAW:
                move_piece_to(board_pos)
                break

def check_mills(player):
    mill = VAR.PLAYER_DICT[player]['positions']
    for possible_mill in VAR.POSSIBLE_MILLS:
        mills = set(possible_mill)
        if mills.issubset(mill):
            VAR.PLAYER_DICT[player]['mill_formed'].update(mills)
    
    current_mills = set(VAR.PLAYER_DICT[player]['mill_formed'])
    prev_mills = set(VAR.PLAYER_DICT[player]['previous_mill'])
    if current_mills == prev_mills or current_mills.issubset(prev_mills):
        VAR.IS_MILL = False
        deformed_coords = prev_mills - current_mills
        print("deformed_coords", deformed_coords)
        if deformed_coords == set():
            VAR.PLAYER_DICT[player]['mill_formed'] = set()
        else: VAR.PLAYER_DICT[player]['mill_formed'] -= deformed_coords
        VAR.PLAYER_DICT[player]['previous_mill'] = current_mills
        print("CURRENT MILL EXISTING!!")
    else:
        VAR.IS_MILL = True
        VAR.PLAYER_DICT[player]['previous_mill'] = current_mills
        print("CURRENT MILL NOT EXISTING!!")
    
    other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
    positions = set(VAR.PLAYER_DICT[other_player]['positions'])
    prev_mill = set(VAR.PLAYER_DICT[other_player]['mill_formed'])
    possible_pieces_to_remove = positions - prev_mill
    VAR.CIRCLES_TO_DRAW = [position for position in possible_pieces_to_remove]
    print("Positins: ", VAR.PLAYER_DICT[player]['positions'])
    print("mill formed: ", VAR.PLAYER_DICT[player]['mill_formed'])
    print("previous mill formed: ", VAR.PLAYER_DICT[player]['previous_mill'])
    print("CIRCLES: ", VAR.CIRCLES_TO_DRAW)

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
    check_mills(VAR.CURRENT_PLAYER)
    switch_player()

def selected_piece(pieces, board_pos):
    """return the piece at the given board position"""
    for piece in pieces:
        if piece.current_position == board_pos.position:
            return piece

def show_possible_moves(selected_piece, game):
    """set possible board positions of the piece to move"""
    possible_moves = []
    if game == 'middlegame':
        if selected_piece.position in VAR.POSSIBLE_MOVES:
            moves = VAR.POSSIBLE_MOVES[selected_piece.position]
            for move in moves:
                for board_pos in board_positions:
                    if board_pos.position == move and not board_pos.occupied:
                        # board_pos.draw_circle(screen, 'green')
                        possible_moves.append(move)
    elif game == 'lategame':
        for board_pos in board_positions:
            if not board_pos.occupied:
                possible_moves.append(board_pos.position)
    VAR.BOARD_TO_DRAW = possible_moves

# Late Game
def late_game(player, mouse_pos):
    pieces = player_piece(0, player, 'lategame') 
    pieces_loc = [pos.current_position for pos in pieces]
    for board_pos in board_positions:
        if board_pos.is_clicked(mouse_pos):
            if board_pos.position in pieces_loc:
                VAR.SELECTED_PIECE = selected_piece(pieces, board_pos)
                if VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]["num_pieces"] == 3:
                    show_possible_moves(board_pos, "lategame")
                else: show_possible_moves(board_pos, "middlegame")
                board_pos.occupied = False
            elif board_pos.position in VAR.BOARD_TO_DRAW:
                move_piece_to(board_pos)
                break

def check_winner(player):
    if VAR.PLAYER_DICT[player]["num_pieces"] == 2:
        return True
    return False

def handle_board_state(handle, event=None, mouse_pos=None):
    if handle:
        screen.blit(surface, (0,0))
        board.draw(screen)
        pause_button.draw(screen)
        github_button.draw(screen)
        text = ''
        if VAR.GAME_PHASE == 'opening':
            for boards_pos in board_positions:
                boards_pos.draw_circle(screen, 'darkgray')
            for pieces in white_pieces + black_pieces:
                pieces.draw(screen)
            text = f'{VAR.CURRENT_PLAYER}: Place your piece to the board'
            if VAR.CURRENT_PLAYER == 'AI' and len(VAR.CIRCLES_TO_DRAW) == 0:
                ai_move, piece_move = get_ai_move(VAR.GAME_PHASE)
                print('AI', ai_move)
                if ai_move:
                    make_move(ai_move, piece_move, VAR.GAME_PHASE)
                    switch_player()
        if VAR.GAME_PHASE == 'middlegame':
            for boards_pos in board_positions:
                boards_pos.draw_circle(screen, 'darkgray')
            for position in VAR.BOARD_TO_DRAW:
                pygame.draw.circle(screen, "RED", position, 14, width=4)
            for piece in white_pieces + black_pieces:
                piece.draw(screen)
            text = f'{VAR.CURRENT_PLAYER}: Move your piece'
            if VAR.CURRENT_PLAYER == 'AI':
                ai_move, piece_move = get_ai_move(VAR.GAME_PHASE)
                print('AI', ai_move)
                if ai_move:
                    make_move(ai_move, piece_move, VAR.GAME_PHASE)
                    switch_player()
        if VAR.GAME_PHASE == 'lategame':
            for boards_pos in board_positions:
                boards_pos.draw_circle(screen, 'darkgray')
            for position in VAR.BOARD_TO_DRAW:
                pygame.draw.circle(screen, "RED", position, 14, width=4)
            for piece in white_pieces + black_pieces:
                piece.draw(screen)
            text = f'{VAR.CURRENT_PLAYER}: Move your piece'
            if VAR.CURRENT_PLAYER == 'AI' and len(VAR.CIRCLES_TO_DRAW) == 0:
                ai_move, piece_move = get_ai_move(VAR.GAME_PHASE)
                print('AI', ai_move)
                if ai_move:
                    make_move(ai_move, piece_move, VAR.GAME_PHASE)
                    switch_player()
        if VAR.IS_MILL:
            other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
            text = f'{other_player}: Select opponent piece to remove'
            for position in VAR.CIRCLES_TO_DRAW:
                pygame.draw.circle(screen, "RED", position, 32, width=3)
        text_display(text, 'black', (400, 30), 32)
    else:
        if pause_button.is_clicked(mouse_pos):
            VAR.GAME_STATE = 'pause'
        elif github_button.is_clicked(mouse_pos):
            webbrowser.open(VAR.GITHUB_URL)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            total_placed = VAR.PLAYER_DICT['Player']['in_board'] + VAR.PLAYER_DICT['AI']['in_board']
            if VAR.GAME_PHASE == 'opening':
                place_pieces(event)
                
                if VAR.IS_MILL:
                    other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
                    remove_piece(other_player, 'opening')
                if total_placed == 0 and (len(VAR.CIRCLES_TO_DRAW) == 0 or len(VAR.CIRCLES_TO_DRAW) == 1):
                    VAR.GAME_PHASE ='middlegame'
            elif VAR.GAME_PHASE =='middlegame':
                other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
                if VAR.IS_MILL:
                    remove_piece(other_player, 'opening')
                middle_game(VAR.CURRENT_PLAYER, mouse_pos)
                if VAR.PLAYER_DICT['Player']["num_pieces"] == 3 or VAR.PLAYER_DICT['AI']["num_pieces"] == 3:
                    VAR.GAME_PHASE = 'lategame'
                if check_winner(VAR.CURRENT_PLAYER):
                    print('winner', other_player)
                    VAR.GAME_STATE = 'winner'
                player_positions = set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'])
                prev_mill = set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['previous_mill'])
                possible_pieces_to_remove = player_positions - prev_mill
                VAR.CIRCLES_TO_DRAW = [position for position in possible_pieces_to_remove]
            elif VAR.GAME_PHASE == 'lategame':
                other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
                if VAR.IS_MILL:
                    remove_piece(other_player, 'opening')
                late_game(VAR.CURRENT_PLAYER, mouse_pos)
                if check_winner(VAR.CURRENT_PLAYER):
                    print('winner', other_player)
                    VAR.GAME_STATE = 'winner'

def reset_board():
    VAR.CURRENT_PLAYER = "Player"
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

## AI Part

# Import statements here
import copy

# Constants
DEPTH_LIMIT = 3
BLOCKING_VALUE = 100
MILL_VALUE = 200

# Function definitions here

def get_ai_move(phase):
    max_eval = float('-inf')
    best_ai_move = None
    best_piece_move = None
    
    # Implement AI logic to determine the best move using Minimax
    other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
    ai_pieces = player_piece(0, VAR.CURRENT_PLAYER, 'middlegame')
    opponent_pieces = player_piece(0, other_player, 'middlegame')

    ai_pieces_onboard = set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'])
    opponent_pieces_onboard = set(VAR.PLAYER_DICT[other_player]['positions'])
    
    if phase == 'opening':
        available_moves = ai_checkAvailableMoves(ai_pieces_onboard, opponent_pieces_onboard, 'opening')
        for move in available_moves:
            new_AI_pieces = set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'].copy())
            new_AI_pieces.add(move)
            new_AI_num_pieces = VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['num_pieces'] - 1

            eval = minimax(new_AI_pieces, DEPTH_LIMIT, new_AI_num_pieces, VAR.PLAYER_DICT[other_player]['positions'], VAR.PLAYER_DICT[other_player]['num_pieces'])
        
            eval += block_opponent_mill(set(VAR.PLAYER_DICT[other_player]['positions']), move)
            eval += create_mill(set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions']), move)
            
            if eval > max_eval:
                max_eval = eval
                best_ai_move = move
        return best_ai_move, best_piece_move
    elif phase == 'middlegame' or phase == 'lategame':
        for piece in ai_pieces:
            print('AI PIECES IN get AI', ai_pieces)
            for move in ai_valid_moves(piece, opponent_pieces_onboard, opponent_pieces):
                new_AI_pieces = set(ai_pieces_onboard.copy())
                new_AI_pieces.add(move)
            
                eval = minimax(new_AI_pieces, DEPTH_LIMIT, 0, opponent_pieces, 0)
                eval += block_opponent_mill(opponent_pieces, move)
                eval += create_mill(new_AI_pieces, move)
                
                if eval > max_eval:
                    max_eval = eval
                    best_ai_move = move
                    best_piece_move = piece
        return best_ai_move, best_piece_move
    return None

def make_move(position, piece, game):
    if game == 'opening':
        placed = VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['placed']
        piece_to_move = player_piece(placed, VAR.CURRENT_PLAYER, 'opening')
        # Implement logic to move the AI's piece to the specified position
        piece_to_move.move(position)
        VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'].add(piece_to_move.current_position)  # Update piece position in the dictionary
        VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['placed'] += 1  # Update the count of placed pieces
        VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['in_board'] -= 1  # Update the count of placed pieces
        for board_pos in board_positions:
            if board_pos.position == piece_to_move.current_position:
                board_pos.occupied = True
    elif game == 'middlegame':
        for position in VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions']:
            if position == piece:
                # update the current players positions in the dictionary
                VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'].remove(position)
                VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'].add(position)
        
        piece.move(position)
        
        for board_pos in board_positions:
            if board_pos.position == piece:
                board_pos.occupied = True
        VAR.BOARD_TO_DRAW = []
        check_mills(VAR.CURRENT_PLAYER)
        switch_player()
        
                
def minimax(ai_pieces, depth, ai_pieces_onhold, opponent_pieces, opponent_pieces_onhold):
    if VAR.GAME_PHASE == 'opening':
        if depth == 0 or ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
            return evaluate(ai_pieces, opponent_pieces)

        max_eval = float('-inf')
        available_moves = ai_checkAvailableMoves(ai_pieces, opponent_pieces, 'opening')
        for move in available_moves:
            new_ai_pieces = set(ai_pieces.copy())
            new_ai_pieces.add(move)
            new_ai_pieces_onhold = ai_pieces_onhold - 1
            eval = minimax(new_ai_pieces, depth - 1, new_ai_pieces_onhold, opponent_pieces, opponent_pieces_onhold)
            max_eval = max(max_eval, eval)
        return max_eval
    elif VAR.GAME_PHASE == 'middlegame':
        if depth == 0 or ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
            return evaluate(ai_pieces, opponent_pieces)

        max_eval = float('-inf')
        print('AI PIECES IN get AI', ai_pieces)
        for move in ai_valid_moves(ai_pieces, opponent_pieces, opponent_pieces):
            new_ai_pieces = set(ai_pieces.copy())
            new_ai_pieces.add(move)
            eval = minimax(new_ai_pieces, depth - 1, 0, opponent_pieces, 0)
            max_eval = max(max_eval, eval)
        return max_eval

def ai_valid_moves(piece, ai_pieces, opponent_pieces):
    clicked_piece = set()
    if isinstance(piece, tuple):  # If piece is a tuple (board position)
        clicked_piece = set(VAR.POSSIBLE_MOVES[piece])
    elif isinstance(piece, Pieces):  # If piece is an instance of Pieces class
        clicked_piece = set(VAR.POSSIBLE_MOVES[piece.current_position])
    opponents = set(opponent_pieces)
    valid_moves = clicked_piece - (set(ai_pieces) | opponents)
    return valid_moves

def ai_checkAvailableMoves(ai_pieces, opponent_pieces, game):
    available_moves = set()  # Initialize an empty set for available moves
    
    if game == 'opening':
        # Iterate through board positions to check for unoccupied positions
        for board_pos in board_positions:
            if not board_pos.occupied:
                available_moves.add(board_pos.position)
    elif game == 'middlegame':
        ai_moves = set()
        opponent_moves = set()
        
        print(ai_pieces)
        for piece in ai_pieces:
            ai_moves.update(VAR.POSSIBLE_MOVES[piece])
        
        for piece in opponent_pieces:
            print(piece)
            opponent_moves.update(VAR.POSSIBLE_MOVES[piece.current_position])
        
        available_moves = ai_moves - (opponent_moves | ai_pieces)
        
    return available_moves

def evaluate(ai_pieces, opponent_pieces):
    if VAR.GAME_PHASE == 'opening':
        piece_count_weight = 2
        mill_count_weight = 10
        mobility_weight = 2
        mode = 'opening'

    elif VAR.GAME_PHASE == 'middlegame':
        piece_count_weight = 7
        mill_count_weight = 10
        mobility_weight = 8
        mode = 'middlegame'

    elif VAR.GAME_PHASE == 'lategame':
        piece_count_weight = 4
        mill_count_weight = 10
        mobility_weight = 8
        mode = 'lategame'

    ai_piece_count = len(ai_pieces)
    ai_mills = count_mills(ai_pieces, 1)
    ai_mobility = len(ai_checkAvailableMoves(ai_pieces, opponent_pieces, mode))
    
    # Calculate the overall score
    ai_score = (piece_count_weight * ai_piece_count) + (mill_count_weight * ai_mills) + (mobility_weight * ai_mobility)
    return ai_score

def ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
    if opponent_pieces_onhold == 0:
        # Check pieces
        if len(opponent_pieces) <= 2:
            return True

        # Check moves
        if not ai_checkAvailableMoves(ai_pieces, opponent_pieces, 'middlegame'):
            return True
    
    return False

def block_opponent_mill(opponent_pieces, ai_move):
    for group in VAR.POSSIBLE_MILLS:
        if ai_move in group:
            # Check if adding AI's move completes a potential mill for the opponent
            count = 0
            for point in group:
                if point in opponent_pieces:
                    count += 1
            if count == 2:
                return 100  # Block opponent's mill
    return 0

def create_mill(ai_pieces, ai_move):
    for group in VAR.POSSIBLE_MILLS:
        if ai_move in group:
            # Check if adding AI's move completes a mill
            count = 0
            for point in group:
                if point in ai_pieces:
                    count += 1
            if count == 2:
                return 200  # AI makes a mill
    return 0

def count_mills(pieces, cmode):
    if cmode == 1:
        mill_count = 0
        for group in VAR.POSSIBLE_MILLS:
            count = 0
            for point in group:
                if point in pieces:
                    count += 1
                    if count == 3:
                        mill_count += 1
                else:
                    count = 0
        return mill_count
    
    if cmode == 2:
        mill_count = set()
        for group in VAR.POSSIBLE_MILLS:
            count = 0
            for point in group:
                if point in pieces:
                    count += 1
                    if count == 2:
                        mill_count.add(point)
                else:
                    count = 0
        return mill_count

    if cmode == 3:
        mill_count = set()
        for group in VAR.POSSIBLE_MILLS:
            count = 0
            for point in group:
                if point in pieces:
                    count += 1
                    if count == 2:
                        mill_count.add(group)
                else:
                    count = 0
        return mill_count


# Example usage:
# ai_move = get_ai_move(phase, curr_player)
# make_move(ai_move.piece, ai_move.position, ai_pieces, opponent_pieces)


# # Import statements here
# from copy import deepcopy

# # Constants
# DEPTH_LIMIT = 5
# BLOCKING_VALUE = 100
# MILL_VALUE = 200

# # Function definitions here

# def get_ai_move(phase, curr_player):
#     max_eval = float('-inf')
#     best_move = None
#     best_piece = None
    
#     # Function implementation here
#     other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
#     ai_pieces = player_piece(0, curr_player, 'middlegame')
#     opponent_pieces = player_piece(0, other_player, 'middlegame')
    
#     ai_pieces_onboard = set(VAR.PLAYER_DICT[curr_player]['positions'])
#     opponent_pieces_onboard = set(VAR.PLAYER_DICT[other_player]['positions'])
#     available_moves = ai_checkAvailableMoves(ai_pieces_onboard, opponent_pieces_onboard, 1)
    
#     if phase == 'opening':
#         for move in available_moves:
#             new_ai_pieces = set(ai_pieces.copy())
#             new_ai_pieces.add(move)
#             new_ai_pieces_onhold = VAR.PLAYER_DICT[curr_player]['num_pieces'] - 1

#             eval = minimax(new_ai_pieces, DEPTH_LIMIT,
#                             new_ai_pieces_onhold, set(VAR.PLAYER_DICT[other_player]['positions']),
#                             VAR.PLAYER_DICT[other_player]['placed'])
#             # Check if the move blocks opponent's mills
#             eval += block_opponent_mill(set(VAR.PLAYER_DICT[other_player]['positions']), move)
#             eval += make_mill(set(VAR.PLAYER_DICT[curr_player]['positions']), move)

#             if eval > max_eval:
#                 max_eval = eval
#                 best_move = move

#                 # Find the piece corresponding to the best move
#                 for piece in ai_pieces:
#                     if piece.current_position == best_move:
#                         best_piece = piece
#                         break

#         # Return both the best piece and the best move
#         return best_piece, best_move

# def make_move(piece, position, ai_pieces, opponent_pieces):
#     for board_pos in board_positions:
#         if piece. == board_pos.position:
#             board_pos.occupied = False
#             piece.move(position)
#             opponent_pieces.append(piece)
#             break

# def ai_checkAvailableMoves(ai_pieces, opponent_pieces, mode):
#     if mode == 1:
#         inter_points = set(VAR.board_piece_positions)
#         points_occupied = set(ai_pieces | opponent_pieces)
#         available_moves = inter_points - points_occupied
#         return available_moves
#     elif mode == 2:
#         your_moves = set()
#         opponent_moves = set()

#         for piece in ai_pieces:
#             your_moves.update(VAR.POSSIBLE_MOVES[piece])

#         for piece in opponent_pieces:
#             opponent_moves.update(VAR.POSSIBLE_MOVES[piece])
        
#         your_valid_moves = your_moves - (opponent_moves | ai_pieces)
#         return your_valid_moves

# def ai_checkPieceValidMoves(piece_clicked, ai_pieces, opponent_pieces):
#     clicked_piece_moves = set(VAR.POSSIBLE_MOVES[piece_clicked])

#     clicked_piece_valid_moves = clicked_piece_moves - (ai_pieces | opponent_pieces)
#     return clicked_piece_valid_moves

# def minimax(ai_pieces, depth, ai_pieces_onhold, opponent_pieces, opponent_pieces_onhold):
#     if VAR.GAME_PHASE == 'opening':
#         if depth == 0 or ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
#             return evaluate(ai_pieces, opponent_pieces)

#         max_eval = float('-inf')
#         for move in ai_checkAvailableMoves(ai_pieces, opponent_pieces, 1):
#             new_ai_pieces = set(ai_pieces.copy())
#             new_ai_pieces.add(move)
#             new_ai_pieces_onhold = ai_pieces_onhold - 1
#             eval = minimax(new_ai_pieces, depth - 1, new_ai_pieces_onhold, opponent_pieces, opponent_pieces_onhold)
#             max_eval = max(max_eval, eval)
#         return max_eval
#     elif VAR.GAME_PHASE == 'middlegame':
#         if depth == 0 or ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
#             return evaluate(ai_pieces, opponent_pieces)

#         max_eval = float('-inf')
#         for piece in ai_pieces:
#             for move in ai_checkPieceValidMoves(piece, ai_pieces, opponent_pieces):
#                 new_ai_pieces = set(ai_pieces.copy())
#                 new_ai_pieces.add(move)
#                 eval = minimax(new_ai_pieces, depth - 1, 0, opponent_pieces, 0)
#                 max_eval = max(max_eval, eval)
#         return max_eval
        
#     elif VAR.GAME_PHASE == 'lategame':
#         if depth == 0 or ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
#             return evaluate(ai_pieces, opponent_pieces)

#         max_eval = float('-inf')
#         for piece in ai_pieces:
#             for move in ai_checkAvailableMoves(ai_pieces, opponent_pieces, 1):
#                 new_ai_pieces = set(ai_pieces.copy())
#                 new_ai_pieces.add(move)
#                 eval = minimax(new_ai_pieces, depth - 1, 0, opponent_pieces, 0)
#                 max_eval = max(max_eval, eval)
#         return max_eval

# def ai_isCurrentPlayerWon(ai_pieces, opponent_pieces_onhold, opponent_pieces):
#     if opponent_pieces_onhold == 0:
#         # Check pieces
#         if len(opponent_pieces) <= 2:
#             return True

#         # Check moves
#         if not ai_checkAvailableMoves(opponent_pieces, ai_pieces, 2):
#             return True
    
#     return False

# def block_opponent_mill(opponent_pieces, ai_move):
#     for group in VAR.POSSIBLE_MILLS:
#         if ai_move in group:
#             # Check if adding AI's move completes a potential mill for the opponent
#             count = 0
#             for point in group:
#                 if point in opponent_pieces:
#                     count += 1
#             if count == 2:
#                 return 100  # Block opponent's mill
#     return 0

# def evaluate(ai_pieces, opponent_pieces):
#     # Assign weights to different factors
#     if VAR.GAME_PHASE == 'opening':
#         piece_count_weight = 2
#         mill_count_weight = 10
#         mobility_weight = 2
#         mode = 1

#     elif VAR.GAME_PHASE == 'middlegame':
#         piece_count_weight = 7
#         mill_count_weight = 10
#         mobility_weight = 8
#         mode = 2

#     elif VAR.GAME_PHASE == 'lategame':
#         piece_count_weight = 4
#         mill_count_weight = 10
#         mobility_weight = 8
#         mode = 1

#     ai_piece_count = len(ai_pieces)
#     ai_mills = count_mills(ai_pieces, 1)
#     ai_mobility = len(ai_checkAvailableMoves(ai_pieces, opponent_pieces, mode))
    
#     # Calculate the overall score
#     ai_score = (piece_count_weight * ai_piece_count) + (mill_count_weight * ai_mills) + (mobility_weight * ai_mobility)
#     return ai_score

# def count_mills(pieces, cmode):
#     if cmode == 1:
#         mill_count = 0
#         for group in VAR.POSSIBLE_MILLS:
#             count = 0
#             for point in group:
#                 if point in pieces:
#                     count += 1
#                     if count == 3:
#                         mill_count += 1
#                 else:
#                     count = 0
#         return mill_count
    
#     if cmode == 2:
#         mill_count = set()
#         for group in VAR.POSSIBLE_MILLS:
#             count = 0
#             for point in group:
#                 if point in pieces:
#                     count += 1
#                     if count == 2:
#                         mill_count.add(point)
#                 else:
#                     count = 0
#         return mill_count

#     if cmode == 3:
#         mill_count = set()
#         for group in VAR.POSSIBLE_MILLS:
#             count = 0
#             for point in group:
#                 if point in pieces:
#                     count += 1
#                     if count == 2:
#                         mill_count.add(group)
#                 else:
#                     count = 0
#         return mill_count

# def make_mill(ai_pieces, ai_move):
#     for group in VAR.POSSIBLE_MILLS:
#         if ai_move in group:
#             # Check if adding AI's move completes a mill
#             count = 0
#             for point in group:
#                 if point in ai_pieces:
#                     count += 1
#             if count == 2:
#                 return 200  # AI makes a mill
#     return 0
# ##


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
                elif VAR.GAME_STATE == 'winner':
                    handle_winner_state(False, mouse_pos)
            
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
        elif VAR.GAME_STATE == 'winner':
            handle_winner_state(True)
        
        pygame.display.update()
        clock.tick(VAR.FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()