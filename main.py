
import tkinter as tk
from PIL import ImageTk, Image
import random
import time

def create_board(rows, cols, num_mines):
    # Create an empty board of specified size
    board = [[0] * cols for _ in range(rows)]
    mine_locations = random.sample(range(rows * cols), num_mines)

    # Place mines randomly on the board
    for loc in mine_locations:
        row = loc // cols
        col = loc % cols
        board[row][col] = '*'

        # Update the count for adjacent cells
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < rows and 0 <= c < cols and board[r][c] != '*':
                    board[r][c] += 1

    return board

def reveal_cell(row, col, event=None):
    # Handle cell reveal
    if event and event.num == 2:  # Middle click
        return

    if board[row][col] == '*':
        # Display mine and end the game if a mine is clicked
        button_grid[row][col].config(text='*', bg='red')
        game_over()
    else:
        # Display the count of adjacent mines and disable the button
        count = board[row][col]
        button_grid[row][col].config(text=count, bg='light gray')
        button_grid[row][col].config(state='disabled')
        check_game_over()

def toggle_flag(row, col):
    # Handle toggling of flag on right-click
    if button_grid[row][col]['state'] != 'disabled':
        current_text = button_grid[row][col]['text']
        if current_text == '':
            # Add flag image and 'F' text to the button
            button_grid[row][col].config(image=flag_image, text='F', compound='center')
        elif current_text == 'F':
            # Remove flag image and 'F' text from the button
            button_grid[row][col].config(image='', text='', compound='center', fg=root['bg'])
        else:
            # Remove flag image but keep the count text on the button
            button_grid[row][col].config(image='', text=current_text, compound='center', fg=root['bg'])
        button_grid[row][col].update_idletasks()
        check_game_over()

def game_over():
    # Disable all buttons and display game over message
    for row in button_grid:
        for button in row:
            button.config(state='disabled')

    message_label.config(text="Game Over", fg='red', font=('Arial', 24, 'bold'))
    restart_button.config(text="Try Again")

def check_game_over():
    # Check if the game is over
    revealed_cells = 0
    flagged_cells = 0
    total_cells = rows * cols

    # Count the number of revealed and flagged cells
    for row in button_grid:
        for button in row:
            if button['state'] == 'disabled':
                revealed_cells += 1
            if button['text'] == 'F':
                flagged_cells += 1

    # Check if all non-mine cells are revealed and all mines are flagged
    if revealed_cells + flagged_cells == total_cells:
        if flagged_cells == num_mines:
            # Player won the game
            message_label.config(text="Congratulations!", fg='green', font=('Arial', 24, 'bold'))
            restart_button.config(text="Try Again")
        else:
            # Player missed some mines
            message_label.config(text="Oops! You missed some mines", fg='red', font=('Arial', 24, 'bold'))
            restart_button.config(text="Try Again")
    else:
        # Reset the message and restart button
        message_label.config(text="")
        restart_button.config(text="Restart")

def create_buttons():
    # Create buttons for each cell on the board
    button_grid = []
    for r in range(rows):
        button_row = []
        for c in range(cols):
            button_frame = tk.Frame(root, width=50, height=50, bg='white', bd=1, relief='raised')
            button_frame.grid(row=r+2, column=c, padx=2, pady=2)
            button_frame.grid_propagate(False)
            button_frame.columnconfigure(0, weight=1)
            button_frame.rowconfigure(0, weight=1)

            button = tk.Button(
                button_frame,
                width=6,
                height=3,
                font=('Arial', 12, 'bold'),
                relief='flat',
                bg='#e0e0e0',
                activebackground='#d0d0d0',
                command=lambda r=r, c=c: reveal_cell(r, c)
            )
            button.grid(row=0, column=0, sticky="nsew")
            button.bind("<Button-2>", lambda event, r=r, c=c: reveal_cell(r, c, event))  # Middle click
            button.bind("<Button-3>", lambda event, r=r, c=c: toggle_flag(r, c))  # Right click
            button_row.append(button)
        button_grid.append(button_row)
    return button_grid

def reset_game():
    # Reset the game state and start a new game
    global board, button_grid, start_time
    for row in button_grid:
        for button in row:
            button.grid_forget()

    button_grid = create_buttons()

    board = create_board(rows, cols, num_mines)
    start_time = time.time()
    update_timer()
    message_label.config(text="")
    restart_button.config(text="Restart")
    reveal_button.config(text="Reveal Mines")

def update_timer():
    # Update the timer label every second
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(100 - elapsed_time, 0)
    timer_label.config(text=f"Time: {remaining_time} seconds")

    if remaining_time <= 0:
        # End the game if the time runs out
        game_over()
    else:
        root.after(1000, update_timer)

def reveal_all_answers():
    # Reveal or hide all mines on the board
    global answers_revealed
    if not answers_revealed:
        # Reveal all mines
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == '*':
                    button_grid[row][col].config(text='*', bg='red')
        reveal_button.config(text="Hide Mines")
    else:
        # Hide all mines
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == '*':
                    button_grid[row][col].config(text='', bg='#e0e0e0')
        reveal_button.config(text="Reveal Mines")

    answers_revealed = not answers_revealed
  
def main():
    # Initialize the game
    global root, rows, cols, num_mines, board, button_grid, message_label, restart_button, reveal_button, flag_image, timer_label, start_time, answers_revealed
    
    # Create the main window
    root = tk.Tk()
    root.title("Minesweeper")
    root.geometry("400x500")
    root.configure(bg='white')

    # Set the default game difficulty
    rows, cols, num_mines = 8, 8, 10

    # Create the timer frame
    timer_frame = tk.Frame(root, bd=2, relief='ridge', bg='white')
    timer_frame.grid(row=0, column=0, columnspan=cols, pady=10, sticky='ew')

    # Create the timer label
    timer_label = tk.Label(timer_frame, text="Time: 0 seconds", font=('Arial', 12, 'bold'), bg='white')
    timer_label.pack(side='left')

    # Create the message label
    message_label = tk.Label(root, text="You have 90 seconds to complete it", font=('Arial', 12), bg='white')
    message_label.grid(row=1, column=0, columnspan=cols, pady=(0, 5))

    # Create the restart button
    restart_button = tk.Button(root, text="Restart", command=reset_game, bg='#e0e0e0', activebackground='#d0d0d0')
    restart_button.grid(row=2, column=cols, pady=(10, 5), padx=10, sticky='e')

    # Create the reveal button
    reveal_button = tk.Button(root, text="Reveal Mines", command=reveal_all_answers, bg='#e0e0e0', activebackground='#d0d0d0')
    reveal_button.grid(row=3, column=cols, columnspan=cols, pady=(10, 5), padx=10)

    # Create the grid of buttons
    button_grid = create_buttons()

    # Load the flag image
    flag_image = ImageTk.PhotoImage(Image.open("flag.png").resize((30, 30)))

    # Initialize the variable to track if answers are revealed
    answers_revealed = False

    # Start a new game
    reset_game()

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()