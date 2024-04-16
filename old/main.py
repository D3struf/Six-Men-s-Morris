"""
    AI Part of the Six Men's Morris
    
    Possible AI to use:
        Monte Carlo Tree Search (MCTS) - simulation method
        A* Search Algorithm - Heuristic approach 
"""
def print_board(board_matrix):
    print(" ---------------")
    for row in board_matrix:
        print(" | ", end=" ")
        for value in row:
            if value == 1:
                print("▢", end=" ")
            else:
                print(" ", end=" ")
        print(" | ")
    print(" ---------------")

print("AI: ▣ \nPlayer: ◉")
board_matrix = [[1, 0, 1, 0, 1,],
                [0, 1, 1, 1, 0],
                [1, 1, 0, 1, 1],
                [0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1,]]
print_board(board_matrix)