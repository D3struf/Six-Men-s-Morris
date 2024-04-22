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

def text_display(text, font_color, position):
    def text_font(size):
        if VAR.GAME_PHASE == 'winner': size = 45
        return pygame.font.SysFont('comicsansms', size)
    
    font = text_font(32)
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
                print(f"MILL: {player} | ", VAR.PLAYER_DICT[player]['previous_mill'])
                VAR.PLAYER_DICT[player]['previous_mill'].update(mills)
                VAR.PLAYER_DICT[player]['mill_formed'] = mills
                VAR.IS_MILL = True
                print(f"MILL: {player} | ", VAR.PLAYER_DICT[player]['previous_mill'])
                
        else: VAR.CIRCLES_TO_DRAW = []  # Clear circles to draw if no mill is formed

def remove_piece(player, game):
    if player == 'Player':
        # pieces = white_pieces if VAR.PLAYER_PIECE == "white" else black_pieces
        opponent_pieces = black_pieces if VAR.PLAYER_PIECE == "white" else white_pieces
    else:
        # pieces = black_pieces if VAR.PLAYER_PIECE == "black" else white_pieces
        opponent_pieces = black_pieces if VAR.PLAYER_PIECE == "black" else white_pieces
    
    # get possible pieces to be removed
    player_positions = set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['positions'])
    prev_mill = set(VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]['previous_mill'])
    
    if VAR.IS_MILL:
        possible_pieces_to_remove = player_positions - prev_mill
    else:
        possible_pieces_to_remove = player_positions
    
    VAR.CIRCLES_TO_DRAW = [position for position in possible_pieces_to_remove]
    print('circles to draw', VAR.CIRCLES_TO_DRAW)
    
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
                                VAR.PLAYER_DICT[player]['mill_formed'] = set()
                                print('REMOVED', VAR.PLAYER_DICT)
                                # VAR.IS_MILL = False
                                return
                            break
                        # if removed:
                        #     break
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

def check_mill_deformed(player):
    print("other Player: ", VAR.PLAYER_DICT[player]['positions'])
    mill = VAR.PLAYER_DICT[player]['positions']
    for possible_mill in VAR.POSSIBLE_MILLS:
        mills = set(possible_mill)
        if mills.issubset(mill) and mills.issubset(VAR.PLAYER_DICT[player]['previous_mill']):
            print("mills: ", mills)
            y = VAR.PLAYER_DICT[player]['previous_mill'].difference(mills)
            VAR.PLAYER_DICT[player]['previous_mill'].difference_update(y)
    print("CHECK MILL DEFORMED: ", VAR.PLAYER_DICT[player]['previous_mill'])

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
    #     other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
    #     remove_piece(other_player, 'middlegame')

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

def check_winner():
    if VAR.PLAYER_DICT[VAR.CURRENT_PLAYER]["num_pieces"] == 2:
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
        if VAR.GAME_PHASE == 'middlegame':
            for boards_pos in board_positions:
                boards_pos.draw_circle(screen, 'darkgray')
            for position in VAR.BOARD_TO_DRAW:
                pygame.draw.circle(screen, "RED", position, 14, width=4)
            for piece in white_pieces + black_pieces:
                piece.draw(screen)
            text = f'{VAR.CURRENT_PLAYER}: Move your piece'
        if VAR.GAME_PHASE == 'lategame':
            for boards_pos in board_positions:
                boards_pos.draw_circle(screen, 'darkgray')
            for position in VAR.BOARD_TO_DRAW:
                pygame.draw.circle(screen, "RED", position, 14, width=4)
            for piece in white_pieces + black_pieces:
                piece.draw(screen)
            text = f'{VAR.CURRENT_PLAYER}: Move your piece'
        if VAR.IS_MILL:
            other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
            text = f'{other_player}: Select opponent piece to remove'
            for position in VAR.CIRCLES_TO_DRAW:
                pygame.draw.circle(screen, "RED", position, 32, width=3)
        text_display(text, 'black', (400, 30))
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
                if check_winner():
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
                if check_winner():
                    print('winner', other_player)
                    VAR.GAME_STATE = 'winner'

def handle_winner_state(handle, mouse_pos=None):
    if handle:
        other_player = 'Player' if VAR.CURRENT_PLAYER == 'AI' else 'AI'
        screen.blit(surface, (0,0))
        # winner_overlay.draw(screen)
        text_display(f'WINNER: {other_player}', 'gold', VAR.CENTER)
        play_again_button.draw(screen)
        exit_button.draw(screen)
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