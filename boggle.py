import tkinter as tk
import boggle_board_randomizer
from random import choice
from boggle_logic import BoggleLogic
import pygame
from pygame import mixer

BOARD_SIZE = boggle_board_randomizer.BOARD_SIZE
BACKGROUND_COLOR = 'snow'
FG_BUTTON_COLORS = ["PaleTurquoise3", "LightPink3", "LightGoldenRod3", "LightSalmon3"]
BG_BUTTON_COLOR = "white"
BUTTON_STYLE = {"font": ("Helvetica", 30, "bold"), "bg": BG_BUTTON_COLOR, "relief": tk.RAISED}
PRESSED_BUTTON_COLOR = "seagreen2"


class BoggleGUI:
    """
    This class is responsible for the graphical display of the game
    """
    def __init__(self):
        """
        Creates a graphic object that contains basic display features to start the game
        """
        self.root = tk.Tk()
        self.root.title("Boggle")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.computer_img = tk.PhotoImage(file="images_music/mac_background.png")
        self.winner_img = tk.PhotoImage(file="images_music/funny-Winner-Memes .png")
        self.button_img = tk.PhotoImage(file="images_music/keyboard_key_empty.png")
        self.boggle_img = tk.PhotoImage(file="images_music/booglepic.png")
        self.start_img = tk.PhotoImage(file="images_music/keyboard_enter.png")
        self.retry_button_img = tk.PhotoImage(file="images_music/retry_button.png")
        self.instructions_img = tk.PhotoImage(file="images_music/instructions.png")
        pygame.mixer.init()
        mixer.music.load("images_music/Madonna - 4 Minutes.wav")
        mixer.music.play(-1)
        self.initialize_game()

    def initialize_game(self):
        """
        Initializes the game login screen
        """
        self.temp_frame = tk.Frame(self.root, bd=10, bg=BACKGROUND_COLOR, cursor="hand2")
        self.temp_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.computer_label = tk.Label(self.temp_frame, bd=0, image=self.computer_img)
        self.computer_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.start_label = tk.Label(self.computer_label, bg=BACKGROUND_COLOR, bd=0, image=self.boggle_img)
        self.start_label.place(x=50, y=70)
        self.start_button = tk.Button(self.computer_label, text="START", image=self.start_img, compound="center",
                                      width=122, height=60, command=self.instructions_window, bd=0,
                                      font=('Courier', 20, 'bold'))
        self.start_button.place(x=180, y=245)

    def instructions_window(self):

        self.start_button.place_forget()
        self.start_label.place_forget()
        self.instructions_label = tk.Label(self.computer_label, bg=BACKGROUND_COLOR, bd=0, image=self.instructions_img,
                                           width=450, height=191)
        self.instructions_label.place(x=25, y=70, height=240, width=430)
        self.continue_button = tk.Button(self.computer_label, text="continue", image=self.start_img, compound="center",
                                         width=122, height=60, command=self.start_game, bd=0,
                                         font=('Courier', 17, 'bold'))
        self.continue_button.place(x=330, y=400)
        self.root.after(1000, self.update_logic)

    def update_logic(self):
        self.logic = BoggleLogic()
        self.board = boggle_board_randomizer.randomize_board()
        self.logic.game_board = self.board
        self.logic.final_words = self.logic.get_all_words()

    def run(self):
        """
        Starts a new game loop
        """
        self.root.mainloop()

    def show_score(self, score=0):
        """
        Shows current score of the player
        :param score: current score
        """
        self.score_label.configure(text=str(score))

    def start_game(self):
        """
        Initializes the game board and starts the time countdown
        """
        self.temp_frame.pack_forget()
        self.create_main_window()
        self.dragging = False
        self.pressed_buttons = []
        self.current_word = ""
        self.ind = 1
        self.win = False
        self.show_score()
        self.countdown(180)

    def create_main_window(self):
        """
        Creates the main window of the game.
        Other internal windows are linked to this window
        """
        self.main_frame = tk.Frame(self.root, bg="white", cursor="hand2")
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.create_upper_frame()
        self.create_middle_frame()
        self.create_lower_frame()

    def create_upper_frame(self):
        """
        Creates the upper frame, responsible for displaying the running clock,
        selected word and messages during the game
        """
        self.upper_frame = tk.Frame(self.main_frame, bg="grey38")
        self.upper_frame.place(x=0, y=0, height=100, width=500)
        self.timer_label = tk.Label(self.upper_frame, fg="red", bg="black")
        self.timer_label.place(x=0, y=40, height=60, width=100)
        self.display_var = tk.StringVar()
        self.display_label = tk.Label(self.upper_frame, text="", font=("Courier", 22, "bold"), bg="white", bd=5,
                                      highlightthickness=10, compound="center",
                                      textvariable=self.display_var, relief="ridge")
        self.display_label.place(x=195, y=40, height=60, width=300)
        self.display_var.set("")
        self.score_label = tk.Label(self.upper_frame, font=("Courier", 30, "bold"), text="", bd=5)
        self.score_label.place(x=100, y=40, height=60, width=95)
        self.message_var = tk.StringVar()
        self.message_label = tk.Label(self.upper_frame, bg="grey38", fg="white", font=("Courier", 20, "bold"),
                                      compound="center", textvariable=self.message_var)
        self.message_label.place(x=0, y=0, height=40, width=500)

    def create_middle_frame(self):
        """
        Creates the middle frame in which the letter board is displayed
        """
        self.middle_frame = tk.Frame(self.main_frame)
        self.middle_frame.place(x=100, y=100, height=400, width=400)
        self._create_buttons_in_middle_frame()
        self.middle_frame.bind("<Leave>", lambda event: self.delete_word(self.pressed_buttons))

    def create_lower_frame(self):
        """
        Creates the side frame responsible for displaying words that have already been guessed
        """
        self.word_box_var = tk.StringVar()
        self.lower_frame = tk.Frame(self.main_frame, height=100)
        self.lower_frame.place(x=0, y=100, height=400, width=100)
        scrollx = tk.Scrollbar(self.lower_frame, orient="horizontal")
        scrolly = tk.Scrollbar(self.lower_frame, orient="vertical")
        self.words_box = tk.Listbox(self.lower_frame, fg="white", bd=5, font=("Courier", 11, "bold"),
                                    yscrollcommand=scrolly.set, xscrollcommand=scrollx.set, bg="grey38")
        scrolly.pack(side="top", fill="x")
        scrollx.pack(side="bottom", fill="x")
        self.words_box.pack(expand=True, fill="both")
        scrollx.config(command=self.words_box.xview)
        scrolly.config(command=self.words_box.yview)

    def game_over(self):
        """
        Creates a game over window, which displays the score and allows the player to play again
        """
        self.main_frame.pack_forget()
        self.temp_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, cursor="hand2")
        self.temp_frame.place(x=0, y=0, height=500, width=500)
        if self.win:
            self.winner_labal = tk.Label(self.temp_frame, bd=0, image=self.winner_img)

            self.winner_labal.place(x=0, y=0, height=500, width=500)
            self.game_over_img = tk.PhotoImage(file="images_music/google_game_over.png")
            self.final_score_label = tk.Label(self.winner_labal, text=f"SCORE:\n{self.logic.score}",
                                              image=self.start_img,
                                              compound="center", bd=0, font=('Courier', 15, 'bold'))
            self.final_score_label.place(x=372, y=250, height=60, width=122)
            self.retry_button = tk.Button(self.winner_labal, image=self.retry_button_img, compound="center",
                                          command=self.start_game,
                                          font=('Microsoft Sans Serif', 24, 'bold'))
            self.retry_button.place(x=402, y=180, height=50, width=57)
        else:
            self.computer_label = tk.Label(self.temp_frame, bd=0, image=self.computer_img)
            self.computer_label.place(x=0, y=0, height=500, width=500)
            self.computer_label.bind("<Button-1>", lambda event: print(event.x, event.y))
            self.game_over_img = tk.PhotoImage(file="images_music/google_game_over.png")
            self.game_over_label = tk.Label(self.computer_label, bg=BACKGROUND_COLOR, bd=0, image=self.game_over_img)
            self.game_over_label.place(x=35, y=70, height=255, width=440)
            self.final_score_label = tk.Label(self.computer_label, text=f"SCORE:\n{self.logic.score}",
                                              image=self.start_img, compound="center", bd=0,
                                              font=('Courier', 15, 'bold'))
            self.final_score_label.place(x=192, y=250, height=60, width=122)
            self.retry_button = tk.Button(self.computer_label, image=self.retry_button_img, compound="center",
                                          command=self.start_game,
                                          font=('Microsoft Sans Serif', 24, 'bold'))
            self.retry_button.place(x=222, y=160, height=50, width=57)
        self.root.after(1000, self.update_logic)

    def countdown(self, remaining=None):
        """
        This function initializes time at the beginning of the game and counts down 3 minutes.
        When out of time game is over.
        :param remaining: remaining seconds till end of the game
        """
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.game_over()
        else:
            minutes = str(self.remaining // 60)
            seconds = self.remaining % 60
            if 0 <= seconds <= 9:
                seconds = "0" + str(seconds)
            self.timer_label.configure(text=minutes + ":" + str(seconds), font=("Courier", 20, "bold"), bd=5)
            self.remaining = self.remaining - 1
            self.root.after(1000, self.countdown)

    def _create_buttons_in_middle_frame(self):
        """
        This function places the buttons on the middle frame
        """
        for i in range(BOARD_SIZE):
            tk.Grid.columnconfigure(self.middle_frame, i, weight=1)

        for i in range(BOARD_SIZE):
            tk.Grid.rowconfigure(self.middle_frame, i, weight=1)

        for r, row in enumerate(self.board):
            for c, letter in enumerate(row):
                self.make_button(letter, r, c)

    def make_button(self, letter: str, row: int, col: int):
        """
        This function creates the middle frame buttons
        :param letter: letter to display on button
        :param row: row of letter in board game
        :param col: col of letter in board game
        """
        button = tk.Button(self.middle_frame, text=letter, width=1, height=1, fg="black", image=self.button_img,
                           compound="center", **BUTTON_STYLE)
        button.grid(row=row, column=col, sticky=tk.NSEW, pady=5, padx=5)
        button.bind("<Enter>", lambda event: self.on_enter(button))
        button.bind("<Leave>", lambda event: self.on_leave(button))
        button.bind("<ButtonPress-1>", lambda event: self.key_pressed(button))

    def on_enter(self, button):
        """
        This function is responsible for actions to be performed when a button is pressed
        :param button: button entered
        """
        self.message_var.set("")
        if self.dragging:
            if button["relief"] != "sunken" and len(self.pressed_buttons) > 0:
                prev_button = self.pressed_buttons[len(self.pressed_buttons)-1]
                if self.legal_move(prev_button, button) and prev_button != button:
                    button.configure(relief="sunken", fg=PRESSED_BUTTON_COLOR)
                    self.pressed_buttons.append(button)
                    self.current_word += button["text"]
                    self.display_var.set(self.current_word)
            else:
                if len(self.pressed_buttons) > 1:
                    previous_button = self.pressed_buttons[len(self.pressed_buttons)-2]
                elif len(self.pressed_buttons) == 1:
                    previous_button = self.pressed_buttons[len(self.pressed_buttons)-1]
                if len(self.pressed_buttons) > 0 and previous_button == button:
                    last_button = self.pressed_buttons.pop(len(self.pressed_buttons)-1)
                    self.current_word = self.current_word[:len(self.current_word)-len(last_button["text"])]
                    self.display_var.set(self.current_word)
                    last_button.configure(relief="raised", fg="black")

        else:
            button.configure(relief="raised", fg=choice(FG_BUTTON_COLORS))

    def on_leave(self, button):
        """
        This function is responsible for actions to be performed when a button is released,
        dragging begins
        :param button: released button
        """
        if self.dragging:
            if button["relief"] == "sunken":
                button.configure(relief="sunken", fg=PRESSED_BUTTON_COLOR)
            else:
                if len(self.pressed_buttons) > 0 and button == self.pressed_buttons[0]:
                    button.configure(relief="sunken", fg=PRESSED_BUTTON_COLOR)
        else:
            button.configure(relief="raised", fg="black")

    def key_pressed(self, button):
        """
        This function is responsible for displaying "push a button" effect
        :param button: pressed button
        """
        if self.dragging:
            self.dragging = False
        else:
            self.dragging = True
        self.simulate_button_press(button)

    def simulate_button_press(self, button) -> None:
        """
        Makes a button light up as if it is pressed, and then returns to normal
        :param button: pressed button
        """
        if self.dragging:
            self.current_word += button["text"]
            self.display_var.set(self.current_word)
            button.configure(relief="sunken", fg=PRESSED_BUTTON_COLOR)
            self.pressed_buttons.append(button)
        else:
            button.configure(relief="raised", fg="black")
            self.print_message()

    def delete_word(self, pressed_buttons_lst):
        """
        This function deletes the word displayed when the selection ends
        :param pressed_buttons_lst:
        :return: word chosen so far
        """
        self.current_word = ""
        self.display_var.set(self.current_word)
        self.dragging = False
        for button in pressed_buttons_lst:
            button.configure(relief="raised", fg="black")
        self.pressed_buttons.clear()

    def print_message(self):
        """
        This function makes an appropriate message to the player, during the game
        """
        self.logic.current_word = self.current_word
        self.logic.path_length = len(self.pressed_buttons)
        result = self.logic.check_current_word()
        if result == 0:
            self.message = "THE WORD DOESN'T EXIST!"
            self.delete_word(self.pressed_buttons)
            self.display_message()

        elif result == 1:
            self.message = "ALREADY FOUND THIS WORD..."
            self.delete_word(self.pressed_buttons)
            self.display_message()

        elif result == 2:
            self.message = "GOOD ONE!"
            self.logic.used_words.add(self.logic.current_word)
            self.show_score(self.logic.score)
            if self.logic.win():
                self.win = True
                self.game_over()
            self.display_current_word()
            self.delete_word(self.pressed_buttons)
            self.display_message()

    @staticmethod
    def legal_move(prev_button, button):
        """
        This function defines possible moves to select a word on the board according to the rules of the game,
        and limits the player accordingly
        :param prev_button: previous selected button
        :param button: current selected button
        :return: True if move is legal
                 False otherwise
        """
        prev_row = prev_button.grid_info()["row"]
        cur_row = button.grid_info()["row"]
        prev_col = prev_button.grid_info()["column"]
        cur_col = button.grid_info()["column"]
        row_distance = prev_row - cur_row
        col_distance = prev_col - cur_col
        if abs(row_distance) <= 1 and abs(col_distance) <= 1:
            return True
        else:
            return False

    def display_message(self, count=0):
        """
        This function displays the message for a limited time
        :param count: indicator for tome passed
        :return: None
        """
        if count > 0:
            return
        self.message_var.set(self.message)
        count += 1
        self.root.after(100, self.display_message(count))

    def display_current_word(self):
        """
        This function updates and displays the currently selected word
        """
        self.words_box.insert(self.ind, self.current_word)
        self.ind += 1


if __name__ == "__main__":
    gui = BoggleGUI()
    gui.run()
