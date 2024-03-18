#pip install nltk
import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

class WordChainGame:
    def __init__(self):
        self.word_chain = []
        self.players = []
        self.current_player_index = 0
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.min_letters = 3
        self.time_limit = 10  # seconds for the progress bar
        self.letter_limit = self.min_letters
        self.turn_counter = 0
        self.used_words = set()  # Set to track previously used words
        self.common_valid_words, self.all_valid_words = self.load_word_list()  # Load the English word list here


    def load_word_list(self):
        filename1 = 'common_english_words.txt' 
        filename2 = 'all_english_words.txt'
        word_set1 = set()  # Initialize an empty set to ensure we return a set no matter what
        word_set2 = set() # Initialize an empty set to ensure we return a set no matter what
        try:
            with open(filename1, 'r') as file:
                word_set1 = {word.strip().lower() for word in file}
            with open(filename2, 'r') as file:
                word_set2 = {word.strip().lower() for word in file}
        except FileNotFoundError:
            print(f"The file {filename1} or {filename2} was not found. Please make sure it's in the correct directory.")
        except Exception as e:
            print(f"An error occurred while loading the word list: {e}")
        return word_set1, word_set2  # Ensure we return a set, even if it's empty
            
            
    def add_player(self, player_name):
        self.players.append(player_name)

    def start_game(self):
        starting_word = self.get_random_word()
        self.word_chain = [starting_word]
        self.used_words.add(starting_word)  # Add the starting word to the used words set


    def process_turn(self, new_word):
        if self.is_valid_word(new_word) and len(new_word) >= self.letter_limit:
            self.word_chain.append(new_word)
            self.used_words.add(new_word)  # Add the new valid word to the used words set
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            self.turn_counter += 1
            if self.turn_counter % 5 == 0:
                self.letter_limit += 1
            return True, ""
        return False, f"Invalid word or word too short. {self.players[self.current_player_index]} loses!"

    def get_random_word(self):
        valid_starting_words = [word for word in self.common_valid_words if len(word) >= 4]
        #we want to start with a common word that people will recognize
        return random.choice(valid_starting_words)

    def is_valid_word(self, word):
        if (len(word) < self.min_letters or
            word[0] != self.word_chain[-1][-1] or
            word in self.used_words or
            (word.lower() not in self.all_valid_words and word.lower() not in self.common_valid_words)):  # Check if the word is in the valid words list
            #we want to have double checking just to be extra sure that the word is valid (since these are open source lists)
            return False
        return True
    

class WordChainGameGUI:
    def __init__(self, master):
        self.master = master
        self.game = WordChainGame()
        self.master.title("Word Chain Game")
        self.timer_update_interval = 100  # milliseconds to update the timer
        self.computer_response_base_time = 0.1  # Base response time for computer in seconds
        self.computer_response_time_increment = 0.3  # Time increment per turn
        self.setup_player_selection_screen()

    def setup_start_screen(self):
        self.start_frame = tk.Frame(self.master)
        self.start_frame.pack(fill=tk.BOTH, expand=True)

        self.start_label = tk.Label(self.start_frame, text="Game tarting in 5 seconds...", font=("Helvetica", 24))
        self.start_label.pack(pady=20)

        self.countdown(5)

    def countdown(self, count):
        if count > 0:
            self.start_label.config(text=f"Game starting in {count} seconds...")
            self.master.after(1000, self.countdown, count - 1)
        else:
            self.start_frame.destroy()
            self.setup_widgets()
            self.start_game()
            
    def setup_player_selection_screen(self):
        self.player_selection_frame = tk.Frame(self.master)
        self.player_selection_frame.pack(fill=tk.BOTH, expand=True)

        # Label and option menu for selecting the number of players
        self.lbl_select_players = tk.Label(self.player_selection_frame, text="Select the number of players (2-10):", font=("Helvetica", 16))
        self.lbl_select_players.pack(pady=10)

        self.selected_num_players = tk.IntVar(value=2)  # Default to 2 players
        self.player_options = [str(num) for num in range(2, 11)]  # Options for 2 to 10 players
        self.opt_menu_players = tk.OptionMenu(self.player_selection_frame, self.selected_num_players, *self.player_options)
        self.opt_menu_players.pack(pady=20)

        # Game mode selection (Player vs. Player or Player vs. Computer)
        tk.Label(self.player_selection_frame, text="Game Mode:", font=("Helvetica", 16)).pack(pady=(5, 0))
        self.game_mode = tk.StringVar(value="PvP")  # Default game mode to Player vs. Player
        self.game_modes = ["PvP", "PvC"]  # PvP: Player vs. Player, PvC: Player vs. Computer
        game_mode_option_menu = tk.OptionMenu(self.player_selection_frame, self.game_mode, *self.game_modes)
        game_mode_option_menu.pack(pady=10)

        # Submit button to proceed based on selections
        self.btn_start = tk.Button(self.player_selection_frame, text="Start Game", command=self.handle_player_selection)
        self.btn_start.pack(pady=10)

        # Trace on game_mode variable to enable/disable player selection based on the game mode
        self.game_mode.trace("w", self.update_player_selection_status)

    def update_player_selection_status(self, *args):
        if self.game_mode.get() == "PvC":
            self.opt_menu_players.configure(state="disabled")
            self.lbl_select_players.configure(fg="grey")  # Optional: change label color to indicate disabled state
        else:
            self.opt_menu_players.configure(state="normal")
            self.lbl_select_players.configure(fg="white")  # Optional: revert label color

    def handle_player_selection(self):
        self.num_players = self.selected_num_players.get() if self.game_mode.get() == "PvP" else 1
        self.player_selection_frame.destroy()
        self.setup_start_screen()

    def setup_widgets(self):
        self.lbl_info = tk.Label(self.master, text="Welcome to the Word Chain Game!", font=("Helvetica", 17))
        self.lbl_info.pack(pady=10)

        self.lbl_current_word = tk.Label(self.master, text="Starting word: ", font=("Helvetica", 17))
        self.lbl_current_word.pack(pady=5)

        self.lbl_min_letters = tk.Label(self.master, text="Minimum letters required: 3", font=("Helvetica", 17))
        self.lbl_min_letters.pack(pady=(0, 5))

        self.entry_word = tk.Entry(self.master, font=("Helvetica", 12))
        self.entry_word.pack(pady=5)
        self.entry_word.bind("<Return>", self.submit_word)  # Bind the Enter key to submit_word

        self.btn_submit = tk.Button(self.master, text="Submit", command=self.submit_word)
        self.btn_submit.pack(pady=5)

        self.lbl_timer = tk.Label(self.master, text="Time left:", font=("Helvetica", 15))
        self.lbl_timer.pack(pady=(10, 0))

        self.progress_bar = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=5)

        self.lbl_status = tk.Label(self.master, text="", font=("Helvetica", 12))
        self.lbl_status.pack(pady=5)

    def start_game(self):
        self.game.players.clear()  # Clear the players list in case there is any residual data
        # Add the selected number of players
        # Adjust based on game mode
        if self.game_mode.get() == "PvP":
            for player_num in range(1, self.num_players + 1):
                self.game.add_player(f"Player {player_num}")
        else:
            self.game.add_player("Player 1")
            self.game.add_player("Computer")
        self.game.start_game()
        self.update_ui()

    def update_ui(self):
        current_player = self.game.players[self.game.current_player_index]
        self.lbl_current_word.config(text=f"Starting word: {self.game.word_chain[-1]}")
        self.lbl_info.config(text=f"{current_player}'s turn. Enter a word starting with '{self.game.word_chain[-1][-1]}':")
        self.lbl_min_letters.config(text=f"Minimum letters required: {self.game.letter_limit}")
        self.start_time = time.time()
        self.entry_word.focus()
        self.start_timer()
        if self.game_mode.get() == "PvC" and self.game.players[self.game.current_player_index] == "Computer":
            self.master.after(int(self.computer_response_base_time * 1000), self.computer_turn)
            
    def computer_turn(self):
        # Logic for the computer to pick a word
        last_word = self.game.word_chain[-1]
        possible_words = [word for word in self.game.common_valid_words if word.startswith(last_word[-1]) and word not in self.game.used_words]
        if possible_words:
            chosen_word = random.choice(possible_words)
            self.game.process_turn(chosen_word)
            self.computer_response_base_time += self.computer_response_time_increment  # Increment response time
            self.update_ui()
        else:
            # Handle situation where computer can't find a word
            messagebox.showinfo("Game Over", "Computer can't find a valid word. You win!")
            self.master.destroy()

    def start_timer(self):
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = self.game.time_limit
        self.update_timer()

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.game.time_limit:
            self.progress_bar['value'] = elapsed_time
            self.master.after(self.timer_update_interval, self.update_timer)
        else:
            self.progress_bar['value'] = self.game.time_limit
            messagebox.showinfo("Time's up!", f"You took too long. {self.game.players[self.game.current_player_index]} loses!")
            self.master.destroy()

    def submit_word(self, event=None):  # Add event=None to handle the keyboard event
        self.master.after_cancel(self.update_timer)  # Stop the timer
        new_word = self.entry_word.get().strip().lower()
        self.entry_word.delete(0, 'end')

        valid, message = self.game.process_turn(new_word)

        if valid:
            self.update_ui()
        else:
            messagebox.showinfo("Game Over", message)
            self.master.destroy()

def main():
    root = tk.Tk()
    app = WordChainGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
