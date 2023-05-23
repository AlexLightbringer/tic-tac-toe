import socket


# Store steps of players
player1_steps = []
player2_steps = []

# Cross or zero
cross = "X"
zero = "O"

# Write win combination
win_combination = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]


# Display board
def print_board(cell):
    print("     ┆     ┆")
    print("  {}  |  {}  |  {}".format(cell[1], cell[2], cell[3]))
    print('_____┆_____┆_____')

    print("     ┆     ┆")
    print("  {}  |  {}  |  {}".format(cell[4], cell[5], cell[6]))
    print('_____┆_____┆_____')

    print("     ┆     ┆")
    print("  {}  ┆  {}  ┆  {}".format(cell[7], cell[8], cell[9]))
    print("     ┆     ┆")


# Process the game logic
def game(player1_socket, player2_socket):
    # Generate a board for the first time
    cell = [' ' for _ in range(10)]
    print_board(cell)

    # Start the game
    status = True
    while status:
        # Player 1's turn
        player1_socket.send(str(cell).encode())
        player1_move = player1_socket.recv(1024).decode()
        if player1_move.lower() == "stop":
            player1_socket.send(b"You interrupted the game. You lose!")
            player2_socket.send(b"Player 1 interrupted the game. You win!")
            break
        player1_move = int(player1_move)
        # Check if position is already in use
        while cell[player1_move] != ' ':
            player1_socket.send(b"Invalid move")
            player1_move = int(player1_socket.recv(1024).decode())
        # Store the player's move
        cell[player1_move] = cross
        player1_steps.append(player1_move)
        print_board(cell)

        # Check for a winning condition
        if check_win(player1_steps):
            player1_socket.send(b"You win!")
            player2_socket.send(b"Player 1 wins!")

            break
        # Check for a draw condition
        if check_draw():
            player1_socket.send(b"Draw!")
            player2_socket.send(b"Draw!")
            break

        # Player 2's turn
        player2_socket.send(str(cell).encode())
        player2_move = player2_socket.recv(1024).decode()
        if player2_move.lower() == "stop":
            player2_socket.send(b"Player 2 interrupted the game. You lose!")
            player1_socket.send(b"You interrupted the game. You win!")
            break
        player2_move = int(player2_move)
        # Check if position is already in use
        while cell[player2_move] != ' ':
            player2_socket.send(b"Invalid move")
            player2_move = int(player2_socket.recv(1024).decode())
        # Store the player's move
        cell[player2_move] = zero
        player2_steps.append(player2_move)
        print_board(cell)

        # Check for a winning condition
        if check_win(player2_steps):
            player2_socket.send(b"You win!")
            player1_socket.send(b"Player 2 wins!")
            break
        # Check for a draw condition
        if check_draw():
            player1_socket.send(b"Draw!")
            player2_socket.send(b"Draw!")
            break


# Check if there is a winning condition
def check_win(steps):
    for combination in win_combination:
        if all(move in steps for move in combination):
            return True
    return False


# Check if it is a draw
def check_draw():
    return len(player1_steps) + len(player2_steps) == 9


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port
host = 'localhost'
port = 12345

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(2)
print('Waiting for players...')

# Accept the first player's connection
player1_socket, player1_address = server_socket.accept()
print('Player 1 connected:', player1_address)

# Send a message to player 1 to initiate the game
player1_socket.send(b"Initiate game")

# Wait for player 1's confirmation
player1_confirmation = player1_socket.recv(1024).decode()

# Accept the second player's connection
player2_socket, player2_address = server_socket.accept()
print('Player 2 connected:', player2_address)

# Send a message to player 2 to initiate the game
player2_socket.send(b"Initiate game")

# Wait for player 2's confirmation
player2_confirmation = player2_socket.recv(1024).decode()

# Check if both players confirmed the game
if player1_confirmation.lower() == "confirm" and player2_confirmation.lower() == "confirm":
    print("Game started!")
    # Send a message to both players to start the game
    player1_socket.send(b"Start game")
    player2_socket.send(b"Start game")
    # Start the game
    game(player1_socket, player2_socket)
else:
    print("Game canceled.")

# Close the server socket
server_socket.close()


