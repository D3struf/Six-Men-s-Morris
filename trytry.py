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
PLAYER_DICT = {
    'player1': {
        'num_pieces': 6,
        'placed': 0,
        'positions': {(398, 501), (197, 501), (600, 501), (297, 298)},
        'mill_formed': set(),
        'previous_mill': set()
    },
    'ai': {
        'num_pieces': 6,
        'placed': 0,
        'positions': set(),
        'mill_formed': set(),
        'previous_mill': set()
    }
}

# mill = (PLAYER_DICT['player1']['positions'])
# for possible_mill in POSSIBLE_MILLS:
#         if len(mill) >= 3:
#             if all(piece_positions in possible_mill for piece_positions in mill):
#                 print("MILL!!!!")

# Reset the values
for players, data in PLAYER_DICT.items():
    data['num_pieces'] = 6
    data['placed'] = 0
    data['positions'] = set()
    data['previous_mill'] = set()
    data['mill_formed'] = set()
    
print(PLAYER_DICT)