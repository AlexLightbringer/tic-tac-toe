import socket


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


# Process the player's moves
def play_game():
    interrupted = False  # Track if the game was interrupted by a player
    while True:
        # Wait for the server's response with the updated board state or error message
        response = client_socket.recv(1024).decode()

        # Handle the server's response
        if response == "Invalid move":
            print("Invalid move. Please try again.")
        elif response == "You win!":
            print("Congratulations! You win!")
            print("""
                  /\_/\\
                 ( o.o )
                > ^  ^ <   
            """)
            print("    🎂🎉 Happy Cat Party! 🎉🎂")
            break
        elif response == "Player 1 wins!":
            print("Player 1 wins!")
            break
        elif response == "Player 2 wins!":
            print("Player 2 wins!")
            break
        elif response == "Draw!":
            print("It's a draw!")
            break
        elif "interrupted the game" in response:
            if "Player 1" in response:
                print("Player 1 interrupted the game. You win!")
            else:
                print("Player 2 interrupted the game. You win!")
            interrupted = True
            break
        else:
            # Update the board
            cell = eval(response)
            print_board(cell)

        # Player's turn
        move = input("Please make your move (Type 'stop' to quit): ")
        if move.lower() == "stop":
            if interrupted:
                print("You interrupted the game. You lose!")
            else:
                print("You interrupted the game. You lose!")
            client_socket.send(move.encode())
            break
        client_socket.send(move.encode())

    client_socket.close()


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 12345)

# Connect to the server
client_socket.connect(server_address)

# Receive the initial message from the server
message = client_socket.recv(1024).decode()
print(message)

# Check if the player wants to initiate the game
if message == "Initiate game":
    confirmation = input("Do you want to start the game? (Type 'confirm' to start): ")
    client_socket.send(confirmation.encode())

    # Wait for the server's response
    response = client_socket.recv(1024).decode()

    # Check if the game started or canceled
    if response == "Start game":
        print("Game started!")
        # Start the game
        play_game()
    else:
        print("Game canceled.")
else:
    print("Game canceled.")