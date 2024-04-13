board_matrix = [[1, 0, 1, 0, 1],
                [0, 1, 1, 1, 0],
                [1, 1, 0, 1, 1],
                [0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1]]

def print_board(board_matrix):
    print(" ---------------")
    for row in board_matrix:
        print(" | ", end=" ")
        for value in row:
            if value == 1:
                print("▢", end=" ")
            elif value == 2:
                print("▣", end=" ")
            elif value == 3:
                print("◉", end=" ")
            else:
                print(" ", end=" ")
        print(" | ")
    print(" ---------------")

def get_position():
    while True:
        try:
            row = int(input("Enter the row number (0-4): "))
            col = int(input("Enter the column number (0-4): "))
            if 0 <= row < 5 and 0 <= col < 5:
                return row, col
            else:
                print("Invalid row or column number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def make_move(board_matrix, row, col, player):
    while True:
        if board_matrix[row][col] != 1:
            print("Position is not empty. Please try again.")
            return False
        
        if player == "player":
            board_matrix[row][col] = 2  # Replace with player symbol (▣)
            break
        elif player == "ai":
            board_matrix[row][col] = 3  # Replace with AI symbol (◉)
            break
    return True

def main():
    player = "player"  # Start with the player's turn

    while True:
        print_board(board_matrix)
        row, col = get_position()
        switch_player = make_move(board_matrix, row, col, player)

        # Switch to the other player
        if switch_player:
            if player == "player":
                player = "ai"
            else:
                player = "player"

if __name__ == "__main__":
    main()