import socket
import tkinter as tk

# Define the Tic-Tac-Toe game board
board = [' ' for _ in range(9)]

def print_board():
    print(board[0] + ' | ' + board[1] + ' | ' + board[2])
    print('--|---|--')
    print(board[3] + ' | ' + board[4] + ' | ' + board[5])
    print('--|---|--')
    print(board[6] + ' | ' + board[7] + ' | ' + board[8])

def check_win(player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def check_draw():
    return ' ' not in board

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"  # Replace with your server's IP address
port = 12345  # Choose an available port

# Bind the socket to the address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(2)  # Allow two players to connect

print("Waiting for players to connect...")

# Create a Tkinter window for the server
server_window = tk.Tk()
server_window.title("Tic-Tac-Toe Server")

# Function to update the server GUI
def update_server_gui():
    for i in range(9):
        buttons[i].config(text=board[i])
    if check_win('X'):
        result_label.config(text="Player X wins!")
    elif check_win('O'):
        result_label.config(text="Player O wins!")
    elif check_draw():
        result_label.config(text="It's a draw!")

# Create buttons for the server GUI
buttons = []
for i in range(9):
    button = tk.Button(server_window, text=' ', width=5, height=2, command=lambda i=i: handle_server_move(i))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

result_label = tk.Label(server_window, text="", width=20)
result_label.grid(row=3, column=0, columnspan=3)

# Accept player connections
player_sockets = []
player_symbols = ['X', 'O']

for _ in range(2):
    player, player_addr = server_socket.accept()
    print(f"Player {len(player_sockets) + 1} connected from {player_addr}")
    player.send(f"Player {player_symbols[len(player_sockets)]}".encode())
    player_sockets.append(player)

# Send the initial game board state to both clients
def send_board_to_clients():
    for player_socket in player_sockets:
        board_state = ''.join(board)
        player_socket.send(board_state.encode())

# Function to handle a move made by the server
def handle_server_move(move):
    if board[move] == ' ':
        board[move] = 'X' if current_player == 0 else 'O'
        update_server_gui()
        send_board_to_clients()

# Game loop
current_player = 0  # Index of the current player
while True:
    send_board_to_clients()  # Send the current board state to both clients
    server_window.update()  # Update the server GUI

    move = player_sockets[current_player].recv(1024).decode()
    
    try:
        move = int(move)
        if 1 <= move <= 9 and board[move - 1] == ' ':
            handle_server_move(move - 1)
        else:
            player_sockets[current_player].send("Invalid move. Try again.".encode())
            continue
    except ValueError:
        player_sockets[current_player].send("Invalid input. Enter a number from 1 to 9.".encode())
        continue
    
    # Check for a win or draw
    if check_win(player_symbols[current_player]):
        update_server_gui()
        player_sockets[current_player].send("Congratulations! You win!".encode())
        other_player = (current_player + 1) % 2
        player_sockets[other_player].send(" You lose. Better luck next time!".encode())
        break
    
    if check_draw():
        update_server_gui()
        for player_socket in player_sockets:
            player_socket.send("It's a draw!".encode())
        break
    
    # Switch 
    other_player=current_player
    current_player = (current_player + 1) % 2
    player_sockets[current_player].send("its your turn!".encode())
    player_sockets[other_player].send("its not your turn".encode())
    #server_window.title(f"Player {player_symbols[current_player]} ({player_symbols[current_player]})'s Turn")

# Close player sockets
for player_socket in player_sockets:
    player_socket.close()

# Close the server socket
server_socket.close()

# Run the Tkinter main loop for the server GUI
server_window.mainloop()
