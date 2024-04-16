"""
Global Variables
"""
# Constants
HEIGHT = 600
WIDTH = 800
CENTER = (WIDTH*0.5, HEIGHT*0.5)
ICON_HEIGHT = 84
ICON_WEIGHT = 84
LIGHTGRAY = "#D9D9D9"
GITHUB_URL = "https://github.com/D3struf/Six-Men-s-Morris.git"

background_path = "./assets/background.gif"
instruction1_path = "./assets/instruction1.png"
instruction2_path = "./assets/instruction2.png"
board_path = "./assets/board.png"
pauseOver_path = "./assets/icons8-pause.png"
white_piece_path = "./assets/icons8-circle-64.png"
black_piece_path = "./assets/icons8-circle-64 (1).png"
play_path = "./assets/icons8-play-128.png"
back_path = "./assets/icons8-rewind-64.png"
next_path = "./assets/icons8-forward-64.png"
start_path = "./assets/start_button.png"
pause_path = "./assets/icons8-pause-64.png"
play_again_path = "./assets/icons8-play-80.png"
restart_path = "./assets/icons8-restart-80.png"
exit_path = "./assets/icons8-exit-80.png"
github_path = "./assets/icons8-github-64.png"

# Game States
GAME_STATE = 'home'
CURRENT_PLAYER = 'player1'
check_mill = False

BOARD_MATRIX = [[3, 0, 3, 0, 3,],
                [0, 3, 3, 3, 0],
                [3, 3, 0, 3, 3],
                [0, 3, 3, 3, 0],
                [3, 0, 3, 0, 3,]]

PLAYERS_POSITION = {
    "player1": [],
    "player2": [],
}
PLAYERS_MILL_FORMATION = {
    "player1": [],
    "player2": [],
}
PLAYERS_PREVIOUS_MILL = {
    "player1": [],
    "player2": [],
}

board_piece_positions = [
    (197, 97), (398, 97), (600, 97), 
    (297, 196), (398, 196), (499, 196), 
    (197, 298), (297, 298),(499, 298), (600, 298), 
    (297, 400), (398, 400), (499, 400), 
    (197, 501), (398, 501), (600, 501)
]

POSSIBLE_MOVES = {
    # first level moves
    (197, 97): [(398, 97), (197, 298)], 
    (398, 97): [(197, 97), (600, 97), (398, 196)],
    (600, 97): [(398, 97), (600, 298)],
    
    # second level moves
    (297, 196): [(398, 196), (297, 298)],
    (398, 196): [(297, 196), (499, 196), (398, 97)],
    (499, 196): [(398, 196), (499, 298)],
    
    # third level moves
    (197, 298): [(197, 97), (197, 501), (297, 298)],
    (297, 298): [(297, 196), (297, 400), (197, 298)],
    (499, 298): [(499, 196), (499, 400), (600, 298)],
    (600, 298): [(499, 298), (600, 97), (600, 501)],
    
    # fourth level moves
    (297, 400): [(398, 400), (297, 298)],
    (398, 400): [(297, 400), (499, 400), (398, 501)],
    (499, 400): [(398, 400), (499, 298)],
    
    # fifth level moves
    (197, 501): [(197, 298), (398, 501)],
    (398, 501): [(197, 501), (600, 501), (398, 400)],
    (600, 501): [(398, 501), (600, 298)]
}

POSSIBLE_MILLS = {
    # Horizontal
    ((197, 97), (398, 97), (600, 97)): None,
    ((297, 196), (398, 196), (499, 196)): None,
    ((297, 400), (398, 400), (499, 400)): None,
    ((197, 501), (398, 501), (600, 501)): None,
    
    # Vertical
    ((197, 97), (197, 298), (197, 501)): None,
    ((297, 196), (297, 298), (297, 400)): None,
    ((499, 196), (499, 298), (499, 400),): None,
    ((600, 97), (600, 298), (600, 501)): None
}