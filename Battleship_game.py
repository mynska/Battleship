import random  # Import the random module for generating random numbers

# Constants
BOARD_SIZE = 10  # Size of the game board (10x10)
SHIP_SIZES = [5, 4, 3, 3, 2, 2, 1, 1]  # List of ship sizes to be placed on the board

# Initialize the boards
def create_board():
    # Function Definition:
    # def create_board(): defines a function named create_board that takes no parameters.
    
    # Board Creation:
    # [['O'] * BOARD_SIZE for _ in range(BOARD_SIZE)] creates a 2D list (a list of lists) using a list comprehension.
    # ['O'] * BOARD_SIZE creates a list containing BOARD_SIZE (which is 10) elements, all of which are 'O'. This represents a single row of the board.
    # The list comprehension [['O'] * BOARD_SIZE for _ in range(BOARD_SIZE)] repeats this row creation BOARD_SIZE times, resulting in a 10x10 grid.
    # The underscore _ is used as a throwaway variable since its value is not needed in the comprehension.
    # This 2D list is then returned as the initialized board.
    return [['O'] * BOARD_SIZE for _ in range(BOARD_SIZE)]

# Print the game board
def print_board(board):
    # Function Definition:
    # def print_board(board): defines a function named print_board that takes one parameter, board, which is the 2D list representing the game board.
    
    # Print Column Headers:
    # print("   A B C D E F G H I J") prints the column headers. The print statement includes three spaces followed by the letters A to J, which correspond to the columns of the board.
    print("   A B C D E F G H I J")
    
    # Print Rows:
    # for idx, row in enumerate(board): loops over each row of the board. The enumerate function is used to get both the index (idx) and the row itself (row).
    # idx is the index of the current row (ranging from 0 to 9).
    # row is the list of cells in the current row.
    for idx, row in enumerate(board):
        # Inside the loop:
        # print(f"{idx+1:2} " + " ".join(row)):
        # f"{idx+1:2} " creates a formatted string that includes the row number (idx+1) and ensures it is at least 2 characters wide (:2). This handles single-digit row numbers (1-9) properly, aligning them with double-digit row numbers (10).
        # " ".join(row) joins the elements of the row list into a single string, with each element separated by a space.
        # The combined string f"{idx+1:2} " + " ".join(row) represents the row number followed by the contents of the row, and this string is printed to the console.
        print(f"{idx+1:2} " + " ".join(row))

# Convert between board coordinates and indices
def coord_to_index(coord):
    try:
        # Convert coordinates (e.g., A5) to indices (e.g., (0, 4))
        column = ord(coord[0].upper()) - ord('A')  # Convert letter to column index
        row = int(coord[1:]) - 1  # Convert number to row index
        return row, column  # Return the row and column indices
    except:
        return -1, -1  # Return invalid indices if conversion fails

# Check if placement is valid
def is_valid_placement(board, ship_size, row, col, orientation):
    if orientation == 'H':  # If orientation is horizontal
        if col + ship_size > BOARD_SIZE:  # Check if ship fits horizontally
            return False
        for c in range(col, col + ship_size):
            if board[row][c] != 'O':  # Check if the cells are empty
                return False
            if not is_valid_surrounding(board, row, c):  # Check surrounding cells
                return False
    else:  # If orientation is vertical
        if row + ship_size > BOARD_SIZE:  # Check if ship fits vertically
            return False
        for r in range(row, row + ship_size):
            if board[r][col] != 'O':  # Check if the cells are empty
                return False
            if not is_valid_surrounding(board, r, col):  # Check surrounding cells
                return False
    return True  # Return True if placement is valid

# Check if the surrounding cells are empty
def is_valid_surrounding(board, row, col):
    for r in range(max(0, row-1), min(BOARD_SIZE, row+2)):
        for c in range(max(0, col-1), min(BOARD_SIZE, col+2)):
            if board[r][c] == 'S':  # If any surrounding cell has a ship
                return False  # Return False (invalid)
    return True  # Return True (valid)

# Place the ship on the board
def place_ship(board, ship_size, is_user):
    placed = False  # Initialize placed flag as False
    while not placed:
        if is_user:  # If user is placing the ship
            coord = input(f"Enter the starting coordinate for your {ship_size}-unit ship (e.g., A5): ")
            row, col = coord_to_index(coord)  # Convert coordinates to indices
            if row == -1 or col == -1 or not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
                print("Invalid input. Try again.")  # Print error message for invalid input
                continue  # Continue the loop for another attempt
            
            if ship_size == 1:
                orientation = 'H'  # Orientation doesn't matter for single-unit ships
            else:
                orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()
        else:  # If computer is placing the ship
            row = random.randint(0, BOARD_SIZE - 1)  # Random row index
            col = random.randint(0, BOARD_SIZE - 1)  # Random column index
            orientation = random.choice(['H', 'V'])  # Random orientation

        if orientation in ['H', 'V'] and is_valid_placement(board, ship_size, row, col, orientation):
            if orientation == 'H':  # Place ship horizontally
                for c in range(col, col + ship_size):
                    board[row][c] = 'S'  # Mark ship cells with 'S'
            else:  # Place ship vertically
                for r in range(row, row + ship_size):
                    board[r][col] = 'S'  # Mark ship cells with 'S'
            placed = True  # Set placed flag to True
        else:
            if is_user:
                print("Invalid placement. Try again.")  # Print error message for invalid placement

# Check if all parts of the ship are hit
def is_ship_sunk(board, row, col):
    for r in range(max(0, row-1), min(BOARD_SIZE, row+2)):
        for c in range(max(0, col-1), min(BOARD_SIZE, col+2)):
            if board[r][c] == 'S':  # If any part of the ship is still intact
                return False  # Return False (not sunk)
    return True  # Return True (sunk)

# Check the user's guess
def check_guess(board, row, col):
    if board[row][col] == 'S':  # If guess hits a ship
        board[row][col] = 'X'  # Mark the hit
        if is_ship_sunk(board, row, col):
            print("Hit and sunk!")  # Print sunk message
        else:
            print("Hit!")  # Print hit message
        return True  # Return True (hit)
    elif board[row][col] == 'O':  # If guess misses
        board[row][col] = '-'  # Mark the miss
        print("Miss!")  # Print miss message
    elif board[row][col] in ['X', '-']:  # If cell was already guessed
        print("Already guessed.")  # Print already guessed message
    return False  # Return False (miss)

# Generate adjacent positions for guessing
def generate_adjacent_positions(row, col):
    positions = []
    if row > 0:
        positions.append((row-1, col))  # Add position above
    if row < BOARD_SIZE - 1:
        positions.append((row+1, col))  # Add position below
    if col > 0:
        positions.append((row, col-1))  # Add position to the left
    if col < BOARD_SIZE - 1:
        positions.append((row, col+1))  # Add position to the right
    return positions  # Return list of adjacent positions

# Get the computer's guess
def get_computer_guess(computer_guess_board, last_hits, orientation):
    if last_hits:  # If there are previous hits
        if orientation:  # If orientation is determined
            potential_targets = []
            for hit in last_hits:
                if orientation == 'H':  # If horizontal, guess left and right
                    potential_targets.extend([(hit[0], hit[1] - 1), (hit[0], hit[1] + 1)])
                else:  # If vertical, guess up and down
                    potential_targets.extend([(hit[0] - 1, hit[1]), (hit[0] + 1, hit[1])])
            random.shuffle(potential_targets)  # Shuffle potential targets
            for target in potential_targets:
                if 0 <= target[0] < BOARD_SIZE and 0 <= target[1] < BOARD_SIZE and computer_guess_board[target[0]][target[1]] == 'O':
                    return target  # Return valid target
        else:
            random.shuffle(last_hits)  # Shuffle last hits
            for hit in last_hits:
                potential_targets = generate_adjacent_positions(*hit)
                random.shuffle(potential_targets)  # Shuffle potential targets
                for target in potential_targets:
                    if computer_guess_board[target[0]][target[1]] == 'O':
                        return target  # Return valid target
    while True:
        row = random.randint(0, BOARD_SIZE - 1)  # Random row guess
        col = random.randint(0, BOARD_SIZE - 1)  # Random column guess
        if computer_guess_board[row][col] == 'O':
            return (row, col)  # Return valid guess

# Mark surrounding cells after sinking a ship
def mark_surrounding_cells(board, row, col):
    for r in range(max(0, row-1), min(BOARD_SIZE, row+2)):
        for c in range(max(0, col-1), min(BOARD_SIZE, col+2)):
            if board[r][c] == 'O':
                board[r][c] = '-'  # Mark surrounding water cells to avoid

# Main game function
def main():
    while True:  # Loop for replayability
        print("Welcome to Battleship!")
        print("Game Rules:")
        print("1. The game board is a 10x10 grid. Each cell is identified by a letter (A-J) and a number (1-10).")
        print("2. You will place your ships on your board, and the computer will place its ships on its board.")
        print("3. The ships are of different sizes: one 5-unit, one 4-unit, two 3-unit, two 2-unit, and two 1-unit ships.")
        print("4. Ships cannot touch each other, not even diagonally.")
        print("5. On your turn, you will guess a coordinate to attack. If you hit a ship, you get another turn. If you miss, it's the computer's turn.")
        print("6. The first player to sink all the opponent's ships wins.")
        print("Let's start!")

        user_board = create_board()  # Create the user's board
        computer_board = create_board()  # Create the computer's board
        user_guess_board = create_board()  # Create the user's guess board
        computer_guess_board = create_board()  # Create the computer's guess board

        print("Place your ships on the board.")
        for size in SHIP_SIZES:
            print_board(user_board)  # Display the user's board
            place_ship(user_board, size, is_user=True)  # User places ships

        for size in SHIP_SIZES:
            place_ship(computer_board, size, is_user=False)  # Computer places ships

        game_over = False  # Initialize game over flag
        last_hits = []  # List to track the last hits by the computer
        orientation = None  # Variable to track ship orientation

        while not game_over:
            print("Your board:")
            print_board(user_board)  # Display the user's board
            print("\nYour guesses:")
            print_board(user_guess_board)  # Display the user's guess board

            user_turn = True  # User's turn
            while user_turn:
                guess = input("Enter your guess (e.g., A5): ")  # Get user's guess
                row, col = coord_to_index(guess)  # Convert coordinates to indices
                if row == -1 or col == -1 or not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE) or user_guess_board[row][col] != 'O':
                    print("Invalid guess. Try again.")  # Print error for invalid guess
                    continue  # Continue loop for another attempt
                if check_guess(computer_board, row, col):
                    user_guess_board[row][col] = 'X'  # Mark hit
                    if all(cell != 'S' for row in computer_board for cell in row):
                        print("You win! All enemy ships have been sunk.")  # User wins
                        game_over = True  # Set game over flag
                        break
                else:
                    user_guess_board[row][col] = '-'  # Mark miss
                    user_turn = False  # End user's turn

                print("\nYour guesses:")
                print_board(user_guess_board)  # Display the user's guess board

            if game_over:
                break  # Exit the game loop if game is over

            computer_turn = True  # Computer's turn
            while computer_turn:
                row, col = get_computer_guess(computer_guess_board, last_hits, orientation)
                print(f"Computer guesses: {chr(col + ord('A'))}{row + 1}")  # Print computer's guess
                if check_guess(user_board, row, col):
                    computer_guess_board[row][col] = 'X'  # Mark hit
                    if is_ship_sunk(user_board, row, col):
                        last_hits = []  # Clear last hits
                        orientation = None  # Reset orientation
                        mark_surrounding_cells(computer_guess_board, row, col)  # Mark surrounding cells
                    else:
                        if last_hits:
                            if last_hits[0][0] == row:
                                orientation = 'H'  # Set orientation to horizontal
                            else:
                                orientation = 'V'  # Set orientation to vertical
                        last_hits.append((row, col))  # Add to last hits
                    if all(cell != 'S' for row in user_board for cell in row):
                        print("Computer wins! All your ships have been sunk.")  # Computer wins
                        game_over = True  # Set game over flag
                        break
                else:
                    computer_guess_board[row][col] = '-'  # Mark miss
                    last_hits = []  # Clear last hits
                    orientation = None  # Reset orientation
                    computer_turn = False  # End computer's turn

                print("Your board:")
                print_board(user_board)  # Display the user's board

        play_again = input("Do you want to play again? (yes/no): ").lower()  # Ask to play again
        if play_again != 'yes':
            break  # Exit the game loop if user doesn't want to play again

if __name__ == "__main__":
    main()  # Run the main game function

