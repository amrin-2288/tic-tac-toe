import socket
import tkinter as tk

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"  # Replace with your server's IP address
port = 12345  # Use the same port as the server

client_socket.connect((host, port))

player_info = client_socket.recv(1024).decode()

player_msg=client_socket.recv(1024).decode()


# Create a Tkinter window for the client
client_window = tk.Tk()
client_window.title(player_info)

# Function to update the client GUI
def update_client_gui(board_state):
    for i in range(9):
        buttons[i].config(text=board_state[i])
    #result_label.config(text=player_msg)
    
# Function to handle a move made by the client
def handle_client_move(move):
    client_socket.send(str(move).encode())

# Create buttons for the client GUI
buttons = []
for i in range(9):
    button = tk.Button(client_window, text=' ', width=5, height=2, command=lambda i=i: handle_client_move(i + 1))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

# Function to receive and process messages from the server
def receive_from_server():
    while True:
        #player_msg=client_socket.recv(1024).decode()
        #result_label.config(text=player_msg)
        #message1=player_msg
        #if message1.startswith("its your turn!") or message1.startswith("its not your turn!"):
           #result_label.config(text=message1) 
        message = client_socket.recv(1024).decode()
        if message.startswith("Congratulations") or message.startswith(" You lose") or message.startswith("It's a draw!") :
            result_label.config(text=message)
            for button in buttons:
                button.config(state=tk.DISABLED)
            break
        elif message.startswith("its your turn!") or message.startswith("its not your turn") or message.startswith("Invalid move"):
            result_label.config(text=message)
        else:
            update_client_gui(message)
        client_window.title(player_info)

# Start a thread to receive messages from the server
import threading
receive_thread = threading.Thread(target=receive_from_server)
receive_thread.start()

result_label = tk.Label(client_window, text="", width=23)
result_label.grid(row=3, column=0, columnspan=3)

# Run the Tkinter main loop for the client GUI
client_window.mainloop()
