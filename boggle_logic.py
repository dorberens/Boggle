import ex12_utils
with open("boggle_dict.txt") as file:
    words_lst = [line.strip() for line in file]
LEGIT_WORDS = set(words_lst)


class BoggleLogic:
    """
    This class is responsible for the logical operations of the game
    """
    def __init__(self) -> None:
        """
        Creates a logical object that keeps variables related to logical calculations in the game
        """
        self.used_words = set()
        self.score = 0
        self.current_word = ""
        self.path_length = 0
        self.game_board = []
        self.final_words = set()

    def check_current_word(self):
        """
        This function checks whether the given word is a word in legit words, and updates the score
        :return: 0 if word not in legit words
                 1 if word already used
                 2 if word is in legit words and ia a new guess
        """
        if self.current_word in self.used_words:
            return 1
        if self.current_word not in LEGIT_WORDS:
            return 0
        self.score += self.path_length**2
        self.used_words.add(self.current_word)
        return 2

    def get_used_word_lst(self):
        """
        This function returns set of words already guessed so far in the game
        :return:
        """
        return self.used_words

    def get_all_words(self):
        """
        This function returns all the words that can be guessed on the current game board
        :return: set of words
        """
        words_paths = ex12_utils.max_score_paths(self.game_board, LEGIT_WORDS)
        return {ex12_utils.get_word(path, self.game_board) for path in words_paths}

    def win(self):
        """
        This function checks if a player wins the game, i.e. player guessed all possible words on the board
        :return: True if player wins
                 False otherwise
        """
        if len(self.used_words) == len(self.final_words):
            return True
        return False
