import pygame

# Constants
FPS = 60
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH*0.5, HEIGHT*0.5)

# Paths
ICON_PATH = './assets/icon.png'
BACKGROUNDGIF_PATH = "./assets/background.gif"
BACKGROUND_PATH = "./assets/background.png"
INSTRUCTION1_PATH = "./assets/instruction1.png"
INSTRUCTION2_PATH = "./assets/instruction2.png"
BOARD_PATH = "./assets/board.png"
PAUSEOVER_PATH = "./assets/icons8-pause.png"
WHITEPIECE_PATH = "./assets/icons8-circle-64.png"
BLACKPIECE_PATH = "./assets/icons8-circle-64 (1).png"
PLAY_PATH = "./assets/icons8-play-128.png"
BACK_PATH = "./assets/icons8-rewind-64.png"
NEXT_PATH = "./assets/icons8-forward-64.png"
START_PATH = "./assets/start_button.png"
PAUSE_PATH = "./assets/icons8-pause-64.png"
PLAYAGAIN_PATH = "./assets/icons8-play-80.png"
RESTART_PATH = "./assets/icons8-restart-80.png"
EXIT_PATH = "./assets/icons8-exit-80.png"
GITHUB_PATH = "./assets/icons8-github-64.png"
GITHUB_URL = "https://github.com/D3struf/Six-Men-s-Morris.git"

# Colors
LIGHTGRAY = "#D9D9D9"
HOVER = '#92140C'

# Game States
GAME_PHASE = 'opening'
GAME_STATE = 'home'
CURRENT_PLAYER = 'player1'
PLAYER_PIECE = ''

# Load images
ICON = pygame.image.load(ICON_PATH)

board_piece_positions = [
    (197, 97), (398, 97), (600, 97), 
    (297, 196), (398, 196), (499, 196), 
    (197, 298), (297, 298),(499, 298), (600, 298), 
    (297, 400), (398, 400), (499, 400), 
    (197, 501), (398, 501), (600, 501)
]
