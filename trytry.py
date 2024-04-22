# PLAYER_DICT = {
#     'player1': {
#         'num_pieces': 6,
#         'placed': 0,
#         'positions': set(),
#         'mill_formed': set(),
#         'previous_mill': set()
#     },
#     'player2': {
#         'num_pieces': 6,
#         'placed': 0,
#         'positions': set(),
#         'mill_formed': set(),
#         'previous_mill': set()
#     }
# }

# PLAYER_DICT['player1']['positions'].add((10,10))
# mill = ((10,10),(20,20),(30,30))

# print(PLAYER_DICT['player1']['positions'])
# print(PLAYER_DICT['player1']['positions'].clear())

# for player, data in PLAYER_DICT.items():
#     print(f"Player: {player}")
#     for key, value in data.items():
#         print(f"Key: {key}: \nValue: {value}")
#     print()  # Add a newline for clarity between players

# # iterate through the positions in the mill_formed
# for mill in PLAYER_DICT['player1']['mill_formed']:
#     for pos in mill:
#         print(f"Pos: {pos}")
        
# # conditional: same for previous_mill
# if mill in PLAYER_DICT['player1']['mill_formed']:
#     print(f"Player 1 same")

# length = 10
# if length == PLAYER_DICT['player1']['num_pieces'] + PLAYER_DICT['player2']['num_pieces']:
#     print("same length")


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

# PLAYER_DICT = {
#     'player1': {
#         'num_pieces': 6,
#         'placed': 0,
#         'positions': {(297, 196), (499, 196), (398, 196)},
#         'mill_formed': set(),
#         'previous_mill': set(),
#     },
#     'ai': {
#         'num_pieces': 6,
#         'placed': 0,
#         'positions': set(),
#         'mill_formed': set(),
#         'previous_mill': set()
#     }
# }

# mill = (PLAYER_DICT['player1']['positions'])
# for possible_mill in POSSIBLE_MILLS:
#         if len(mill) >= 3:
#             if all(piece_positions in possible_mill for piece_positions in mill):
#                 print("MILL!!!!")

# Reset the values
# for players, data in PLAYER_DICT.items():
#     data['num_pieces'] = 6
#     data['placed'] = 0
#     data['positions'] = set()
#     data['previous_mill'] = set()
#     data['mill_formed'] = set()
    
# print(PLAYER_DICT)
board_piece_positions = [
    (197, 97), (398, 97), (600, 97), 
    (297, 196), (398, 196), (499, 196), 
    (197, 298), (297, 298),(499, 298), (600, 298), 
    (297, 400), (398, 400), (499, 400), 
    (197, 501), (398, 501), (600, 501)
]
pieces1 = {(600, 97), (398, 501), (600, 298), (600, 501)}
pieces2 = {(499, 196), (499, 298), (499, 400)}

# occupied = set(pieces1 | pieces2)
# print(set(board_piece_positions) - occupied)
# mill = (PLAYER_DICT['player1']['positions'])
# for possible_mill in`` POSSIBLE_MILLS:
#     mills = set(possible_mill)
#     if len(pieces1) >= 3 and mills.issubset(mill):
#         print("first if")
#         if not mills.issubset(PLAYER_DICT['player1']['previous_mill']):
#             print("wala sa loob ng previous mill")
#             PLAYER_DICT["player1"]['previous_mill'].update(mills)
#             PLAYER_DICT["player1"]['mill_formed'] = mills
#         else: print("nasa loob ng previous mill")
        
# print(PLAYER_DICT['player1']['mill_formed'])
# print(PLAYER_DICT['player1']['previous_mill'])

# if pieces2 == PLAYER_DICT['ai']['mill_formed']:
#     print("MILL")
# else:
#     print("NAHHH")

# player_positions = PLAYER_DICT['player1']['positions']
# prev_mill = PLAYER_DICT['player1']['mill_formed']
# mill = {(499, 196), (499, 298), (499, 400)}
# mills = {(398, 501), (600, 298), (600, 501)}
# y = {(297, 400), (398, 400), (499, 400)}
# possible_pieces_to_remove = player_positions - prev_mill  
# # print(possible_pieces_to_remove)
# print(PLAYER_DICT['player1']['mill_formed'])
# PLAYER_DICT['player1']['mill_formed'].clear()
# PLAYER_DICT['player1']['mill_formed'].update(mill)
# PLAYER_DICT['player1']['previous_mill'].update(y)
# # print(PLAYER_DICT['player1'])
# x = mill.symmetric_difference_update(y)
# print(x)
# PLAYER_DICT['player1']['previous_mill'].update(x)
# PLAYER_DICT['player1']['mill_formed']
# print(PLAYER_DICT['player1'])

# l = ['1', '2', '3','4', '5','6']
# import random
# str = ''
# for i in range(7):
#     str += random.choice(l)
# print(str)

# f = lambda x, y: x * y
# print(f(3,3))


# # function doc
# def add(x, y):
#     """return the sum of x and y

#     Args:
#         x (int): any integer
#         y (int): any integer
#     """
#     return x + y

# print(add.__doc__)

PLAYER_DICT = {
    'player1': {
        'num_pieces': 6,
        'placed': 0,
        'positions': {(297, 196), (499, 196), (398, 196), (499, 298), (398, 400)},
        'mill_formed': set(),
        'previous_mill': {(398, 196), (499, 298), (297, 196), (499, 196), (499, 400)},
    },
}

# mills = PLAYER_DICT['player1']['positions']
# y = PLAYER_DICT['player1']['previous_mill'].difference(mills) 
# PLAYER_DICT['player1']['previous_mill'].difference_update(y)
# print(PLAYER_DICT['player1']['previous_mill'])

# mill = PLAYER_DICT['player1']['positions']
# for possible_mill in POSSIBLE_MILLS:
#     mills = set(possible_mill)
#     if mills.issubset(mill) and mills.issubset(PLAYER_DICT['player1']['previous_mill']):
#         print("mills: ", mills)
#         y = PLAYER_DICT['player1']['previous_mill'].difference(mills) 
#         print(y)
#         PLAYER_DICT['player1']['previous_mill'].intersection_update(y)
# print("CHECK MILL DEFORMED: ", PLAYER_DICT['player1']['previous_mill'])

# SELECTED_PIECE = (297, 196)
# selected_piece = SELECTED_PIECE
# new_pos = (499, 298)
# for position in PLAYER_DICT['player1']['positions']:
#     selected_piece = SELECTED_PIECE
#     if position == selected_piece:
#         # update the current players positions in the dictionary
#         PLAYER_DICT['player1']['positions'].remove(position)
#         print(PLAYER_DICT['player1']['positions'])
#         PLAYER_DICT['player1']['positions'].add(new_pos)
#         print(PLAYER_DICT['player1']['positions'])
        
# print(PLAYER_DICT['player1']['positions'])

# import pygame
# print(pygame.font.get_fonts())