# Tic-Tac-Toe Multiplayer Game

This is a implementation of a Tic-Tac-Toe game where two players can play against each other over a network. The game is played using a client-server architecture, and communication between the players is facilitated through sockets.

## Files

### `client.py`

This file contains the client-side code responsible for handling the user interface and interaction with the server. The player can make moves, and the game state is continuously updated based on the server's responses.

### `server.py`

This file contains the server-side code that manages the game logic and coordinates the interaction between the two players. The server handles the initialization, confirmation, and execution of the game.

## How to Run

1. Run the `server.py` file on a machine that is accessible to both players. Make sure to set the correct host and port.

    ```bash
    python server.py
    ```

2. Run the `client.py` file on each player's machine. The client will prompt the players to confirm if they want to start the game.

    ```bash
    python client.py
    ```

3. Follow the instructions provided by the client to make moves during the game. Players take turns making moves until the game is won, drawn, or interrupted.

## Game Rules

- The game is a classic Tic-Tac-Toe played on a 3x3 board.
- Players take turns to place their symbol ('X' or 'O') on an empty cell.
- The first player to get three of their symbols in a row (horizontally, vertically, or diagonally) wins.
- The game ends in a draw if all cells are filled, and no player has won.
- Players can interrupt the game at any time by typing 'stop'.

## Notes

- The communication between the client and server is based on simple string messages.
- The server communicates the current state of the board and game outcomes to the clients.
- Players can interrupt the game, and the appropriate messages are sent to both players.
