import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import random
import time
import json

def open_archive():
    try:
        with open('archive.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        data = []
        return data


def add_record(name, time, score):
    new_record = { 
        "name": name,
        "time": time,
        "score": score
    }
    archive = open_archive()
    archive.append(new_record)
    with open('archive.json', 'w') as file:
        json.dump(archive, file, indent=4)

def archive_print(width=60):
    records = open_archive()
    output = ""
    separator = "="*width + "\n"
    for rec in records:
        output += f"Name: {rec['name']}\n"
        output += f"Score: {rec['score']}\n"
        output += f"Time: {rec['time']}sec\n"
        output += separator
    return output


def read_high_score():
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read().strip())
            return high_score
    except FileNotFoundError:
        return None #nothing to return
    except ValueError:
        return None #non numeric value check
    
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

def center_wind(root, width=500, height=300):
    topX = (root.winfo_screenwidth() - width) // 2
    topY = (root.winfo_screenheight() - height) //2
    root.geometry(f"{width}x{height}+{topX}+{topY}")

class Game():
    def __init__(self, root):
        self.root = root
        self.root.title("Game")
        center_wind(root,500,400)
        #root.configure(bg="red")

        self.randon_int = None
        self.count = 0
        self.start_time = None
        self.player_name = None
        self.player_turn = 0
        self.player_board = [["" for _ in range(3)] for _ in range(3)]

        # Frames
        self.main_menu_frame = tk.Frame(root)
        self.game_frame = tk.Frame(root)
        self.history_frame = tk.Frame(root)
        self.tic_frame = tk.Frame(root)

        self.create_mane_menu()
        self.create_game_scr()
        self.create_history_scr()
        self.create_tic_scr()

        self.main_menu_frame.pack()

    def create_mane_menu(self):
        tk.Label(self.main_menu_frame, text="Welcome!").pack(pady=20)
        tk.Button(self.main_menu_frame, text="Play numbers", command=self.show_game).pack(pady=(0, 20))
        tk.Button(self.main_menu_frame, text="History", command=self.show_history).pack(pady=(0, 20))
        tk.Button(self.main_menu_frame, text="Play tic-tac-toe", command=self.show_tic_game).pack()

    def create_history_scr(self):
        self.name_Label = tk.Label(self.history_frame, text="History")
        self.name_Label.pack()

        self.score_text = scrolledtext.ScrolledText(self.history_frame,width=50, height=20, state='disabled')
        self.score_text.pack()

        self.exit_Button = tk.Button(self.history_frame, text="Back", command=lambda: self.back_main_menu(self.history_frame)).pack()
        
        
    def create_game_scr(self):
        self.name_Label = tk.Label(self.game_frame, text="Enter your name:")
        self.name_Label.pack()

        self.name_entry = tk.Entry(self.game_frame)
        self.name_entry.pack()

        self.start_button = tk.Button(self.game_frame, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.info_label = tk.Label(self.game_frame, text="")
        self.info_label.pack()

        self.guess_entry = tk.Entry(self.game_frame)
        self.guess_entry.pack()
        self.guess_entry.config(state='disabled')

        self.guess_button = tk.Button(self.game_frame, text="Guess", command=self.make_guess)
        self.guess_button.pack()
        self.guess_button.config(state='disabled')

        self.result_label = tk.Label(self.game_frame, text="")
        self.result_label.pack()

        self.back_button = tk.Button(self.game_frame, text="Back", command=lambda: self.back_main_menu(self.game_frame))
        self.back_button.pack()

        self.name_entry.bind("<Return>", lambda event: self.start_game())
        self.guess_entry.bind("<Return>", lambda event: self.make_guess())

    def create_tic_scr(self):
        self.info_label = tk.Label(self.tic_frame, text="")
        self.info_label.pack()

        self.canvas = tk.Canvas(self.tic_frame, width=300,height=300)
        self.canvas.pack()

        self.canvas.create_line(100, 0, 100, 300, width=2)
        self.canvas.create_line(200, 0, 200, 300, width=2)
        self.canvas.create_line(0, 100, 300, 100, width=2)
        self.canvas.create_line(0, 200, 300, 200, width=2)

        self.canvas.bind("<Button-1>", self.handle_click)

        self.back_button = tk.Button(self.tic_frame, text="Back", command=lambda: self.back_main_menu(self.tic_frame))
        self.back_button.pack()

    def show_game(self):
        self.main_menu_frame.pack_forget()
        self.game_frame.pack()

    def show_history(self):
        self.main_menu_frame.pack_forget()
        self.score_text.config(state="normal")
        self.score_text.delete('1.0', tk.END)
        self.score_text.insert(tk.END, archive_print(50))
        self.history_frame.pack() #change here
        self.score_text.config(state="disabled")

    def show_tic_game(self):
        self.main_menu_frame.pack_forget()
        self.tic_frame.pack()


    def back_main_menu(self, frame):
        frame.pack_forget()
        self.main_menu_frame.pack()

       

    def handle_click(self, event):
            row = event.y // 100 
            col = event.x // 100 

            if self.player_board[row][col] != "":
                return
            
            y = row * 100 + 50
            x = col * 100 + 50
            
            if self.player_turn == 0:
                self.canvas.create_text(x, y, text="X", font=("Arial", 48))
                self.player_board[row][col] = 1
                self.player_turn = 1
            else:
                radius = 20
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, width=6)
                self.player_board[row][col] = 0
                self.player_turn = 0
            if self.cheak_tic_winner(row,col):
                messagebox.showinfo("Game over", f"Player {self.player_board[row][col]} wins!")


    def cheak_tic_winner(self,row,col):
        table = self.player_board
        player = table[row][col]

        if all(cell == player for cell in table[row]):
            return True
        if all(table[r][col] == player for r in range(3)):
            return True
        if row==col and all(table[i][i] == player for i in range(3)):
            return True
        if row+col==2 and all(table[i][2-i] == player for i in range(3)):
            return True
        return False


    
    def start_game(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showwarning("Warning", "Please enter your name.")
            return
        self.random_int = random.randint(1,15)
        self.count = 0
        self.start_time = time.time()
        self.info_label.config(text="Guess a number between 1 and 15")
        self.guess_entry.config(state='normal')
        self.guess_button.config(state='normal')
        self.result_label.config(text="")
        self.guess_entry.focus_set()
        #self.guess_entry.bind("<Return>", lambda event: self.make_guess())
        

    def make_guess(self):
            try:
                user_guess = int(self.guess_entry.get())
            except ValueError:
                self.result_label.config(text="Please enter a valid number")
            if user_guess < 1 or user_guess > 15:
                self.result_label.config(text="Number must be between 1 and 15")
                self.guess_entry.delete(0, tk.END)
                return
            self.guess_entry.delete(0, tk.END)
            self.count+=1
            if user_guess>self.random_int:
                self.result_label.config(text="Aim lower")
            elif user_guess<self.random_int:
                self.result_label.config(text="Aim higher")
            else:
                final_time = round(time.time() - self.start_time, 2)
                add_record(self.player_name, str(final_time), str(self.count))
                high_score = read_high_score()
                msg = f"You won in {self.count} guesses!\nTime taken: {final_time} sec"

                if high_score is None or self.count < high_score: 
                    save_high_score(self.count)
                    msg += "\nNew High Score!"

                messagebox.showinfo("Game Over", msg)
                self.reset_game()
                self.back_main_menu(self.game_frame)    
                
    def reset_game(self):
            self.info_label.config(text="Game finished. Start again if you want.")
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.config(state='disabled')
            self.guess_button.config(state='disabled')    
            

# Setup
root = tk.Tk()            # Create the window
app = Game(root)     # Fill it with buttons, labels, logic

root.mainloop()           # Run the app

