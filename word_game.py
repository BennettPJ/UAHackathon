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
        self.valid_words = self.load_word_list()  # Load the English word list here


    def load_word_list(self):
        filename = 'english_words.txt'  # Adjust if your file is located differently
        word_set = set()  # Initialize an empty set to ensure we return a set no matter what
        try:
            with open(filename, 'r') as file:
                word_set = {word.strip().lower() for word in file}
        except FileNotFoundError:
            print(f"The file {filename} was not found. Please make sure it's in the correct directory.")
        except Exception as e:
            print(f"An error occurred while loading the word list: {e}")
        return word_set  # Ensure we return a set, even if it's empty
            
            
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
        valid_starting_words = [word for word in self.valid_words if len(word) >= 4]
        return random.choice(valid_starting_words)

    def is_valid_word(self, word):
        if (len(word) < self.min_letters or
            word[0] != self.word_chain[-1][-1] or
            word in self.used_words or
            word.lower() not in self.valid_words):  # Check if the word is in the valid words list
            return False
        return True
    

class WordChainGameGUI:
    def __init__(self, master):
        self.master = master
        self.game = WordChainGame()
        self.master.title("Word Chain Game")
        self.timer_update_interval = 100  # milliseconds to update the timer
        self.setup_widgets()
        self.start_game()

    def setup_widgets(self):
        self.lbl_info = tk.Label(self.master, text="Welcome to the Word Chain Game!", font=("Helvetica", 14))
        self.lbl_info.pack(pady=10)

        self.lbl_current_word = tk.Label(self.master, text="Starting word: ", font=("Helvetica", 12))
        self.lbl_current_word.pack(pady=5)

        self.lbl_min_letters = tk.Label(self.master, text="Minimum letters required: 3", font=("Helvetica", 12))
        self.lbl_min_letters.pack(pady=(0, 5))

        self.entry_word = tk.Entry(self.master, font=("Helvetica", 12))
        self.entry_word.pack(pady=5)
        self.entry_word.bind("<Return>", self.submit_word)  # Bind the Enter key to submit_word

        self.btn_submit = tk.Button(self.master, text="Submit", command=self.submit_word)
        self.btn_submit.pack(pady=5)

        self.lbl_timer = tk.Label(self.master, text="Time left:", font=("Helvetica", 12))
        self.lbl_timer.pack(pady=(10, 0))

        self.progress_bar = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=5)

        self.lbl_status = tk.Label(self.master, text="", font=("Helvetica", 12))
        self.lbl_status.pack(pady=5)

    def start_game(self):
        self.game.add_player("Player 1")
        self.game.add_player("Player 2")
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
