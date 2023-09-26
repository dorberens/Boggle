#################################################################
# FILE : ex12_utils.py
# WRITER : in AUTHORS file
# EXERCISE : intro2cs2 ex12 2022
# DESCRIPTION: some functions for boggle game
# STUDENTS I DISCUSSED THE EXERCISE WITH: ........
# WEB PAGES I USED:
# NOTES:
#################################################################

import boggle_board_randomizer
BOARD_SIZE = boggle_board_randomizer.BOARD_SIZE
POSSIBLE_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
ROW = 0
COL = 1


def is_valid_path(board, path, words):
    """
    This function checks if given path is valid, i.e. a word exists in its coordinates,
    and the coordinates are in the right order
    :param board: list of lists of strings
    :param path: list of coordinates
    :param words: iterable object
    :return: the word if exists, None otherwise
    """
    word = ""
    if duplicated_coords(path):
        return
    for i, coord in enumerate(path):
        if in_range_of_board(coord) and valid_continuation(coord, i, path):
            word += board[coord[ROW]][coord[COL]]
        else:
            return
    if word in words:
        return word
    return


def valid_continuation(cur_coord, index, path):
    """
    This function checks if the word continuity on the board is in consecutive order
    :param cur_coord: current coord of a letter
    :param index: coord index in path list
    :param path: list with coords
    :return: True if order is consecutive
             False otherwise
    """
    if index >= len(path)-1:
        return True
    next_coord = path[index+1]
    if abs(cur_coord[COL] - next_coord[COL]) == 1 and cur_coord[ROW] == next_coord[ROW]:
        return True
    if abs(cur_coord[ROW] - next_coord[ROW]) == 1 and cur_coord[COL] == next_coord[COL]:
        return True
    if abs(cur_coord[ROW] - next_coord[ROW]) == 1 and abs(cur_coord[COL] - next_coord[COL]) == 1:
        return True
    return False


def in_range_of_board(coord):
    """
    This function checks if the coordinate values are in range of board
    :param coord: (col, row) tuple
    :return: True if coord in range, False otherwise
    """
    return 0 <= coord[ROW] < BOARD_SIZE and 0 <= coord[COL] < BOARD_SIZE


def duplicated_coords(lst):
    """
    This function checks if the list contains duplicate values
    :param lst: list
    :return: True if list contains duplicate values, False otherwise
    """
    if len(lst) != len(set(lst)):
        return True
    return False


def make_board_dict(board):
    """
    This function creates a dictionary from board values,
    such that the keys are the letters on the board, and the values are their coordinates.
    :param board: list of lists
    :return: dictionary
    """
    letters = set()
    board_dict = {}
    for r, row in enumerate(board):
        for c, val in enumerate(row):
            if val in board_dict:
                board_dict[val].append((r, c))
            else:
                board_dict[val] = [(r, c)]
                if len(val) == 1:
                    letters.add(val)
                else:
                    letters.add(val[0])
                    letters.add(val[1])
    return board_dict, letters


def check_word_possibility(word, letters, n):
    """
    This function checks if the word has an initial chance to be on the board,
    according to the presence of all the letters of the word on the board,
    and to appropriate max and min desired length
    :param word: word to check
    :param letters: letters set on board
    :param n: desired length of path
    :return: True if word is possible to be on board, False otherwise
    """
    if len(word) < n or len(word) > 2*n:
        return False
    if not all(letter in letters for letter in word):
        return False
    return True


def find_length_n_paths(n, board, words):
    """
    This function returns list of paths with n length, that represent a valid word.
    The function runs over the words and looks for relevant words only.
    :param n: desired path length
    :param board: list of lists of strings
    :param words: iterable object
    :return: list of paths with the desired length
    """
    if n > BOARD_SIZE**2:
        return []
    all_paths = []
    board_dict, letters = make_board_dict(board)
    for word in set(words):
        if check_word_possibility(word, letters, n):
            if word[0] in board_dict:
                for coord in board_dict[word[0]]:
                    all_paths = find_length_n_paths_helper(n, board, word, "", {}, all_paths, 1, coord[ROW], coord[COL])
            if word[0:2] in board_dict:
                for coord in board_dict[word[0:2]]:
                    all_paths = find_length_n_paths_helper(n, board, word, "", {}, all_paths, 1, coord[ROW], coord[COL])
    return all_paths


def find_length_n_paths_helper(n, board, word, cur_word, single_path, all_paths, index_n, row, col):
    """
    This function receives an initial coordinate and searches for paths with the desired length
    that start on this coordinate, and represents the given word
    :param n: desired path length
    :param board: game board
    :param word: given word to check for
    :param cur_word: current word
    :param single_path: current path
    :param all_paths: all paths dict
    :param index_n: length of the current path
    :param row: row of coord
    :param col: col of coord
    :return: updated all paths dict
    """
    single_path.update({(row, col): None})
    cur_word += board[row][col]

    if index_n >= n:
        if cur_word == word:
            all_paths.append(list(single_path.keys()))
        return all_paths

    for move in POSSIBLE_MOVES:
        if continue_is_possible(move, row, col, single_path, cur_word, board, word):
            find_length_n_paths_helper(n, board, word, cur_word, single_path, all_paths, index_n+1,
                                       row+move[ROW], col+move[COL])
        else:
            continue
        if len(single_path) != 0:
            single_path.popitem()

    return all_paths


def continue_is_possible(move, row, col, single_path, cur_word, board, word):
    """
    This function checks if there is a point in continuing the word search in the current path,
    depends on the next continuation letter and the legality of the next step
    :param move: (row,col) row and col steps needed for move
    :param row: coord row
    :param col: coord col
    :param single_path: current path
    :param cur_word: current word
    :param board: board
    :param word: given word to check for
    :return: True if continue this move is possible, False otherwise
    """
    if not in_range_of_board((row + move[ROW], col + move[COL])):
        return False
    if (row + move[ROW], col + move[COL]) in single_path:
        return False
    cur_word += board[row+move[ROW]][col+move[COL]]
    if cur_word not in word:
        return False
    return True


def find_length_n_words(n, board, words):
    """
    This function returns list of paths of words with n length.
    The function runs over the words and looks for relevant words only.
    :param n: desired word length
    :param board: game board
    :param words: iterable object
    :return: list of paths with the desired word
    """
    if n > 2 * (BOARD_SIZE ** 2):
        return []
    all_paths = []
    board_dict, letters = make_board_dict(board)
    for word in set(words):
        if len(word) == n and all(letter in letters for letter in word):
            if word[0] in board_dict:
                for coord in board_dict[word[0]]:
                    all_paths = find_length_n_words_helper(n, board, word, "", {}, all_paths, 1, coord[ROW], coord[COL])
            if word[0:2] in board_dict:
                for coord in board_dict[word[0:2]]:
                    all_paths = find_length_n_words_helper(n, board, word, "", {}, all_paths, 2, coord[ROW], coord[COL])
    return all_paths


def find_length_n_words_helper(n, board, word, cur_word, single_path, all_paths, index_n, row, col):
    """
    This function receives an initial coordinate and searches for paths with the desired length
    that start on this coordinate, and represents the given word
    :param n: desired path length
    :param board: game board
    :param word: given word to check for
    :param cur_word: current word
    :param single_path: current path
    :param all_paths: all paths dict
    :param index_n: length of the current word
    :param row: row of coord
    :param col: col of coord
    :return: updated all paths dict
    """
    single_path.update({(row, col): None})
    cur_word += board[row][col]

    if index_n >= n:
        if index_n == n:
            if cur_word == word:
                all_paths.append(list(single_path.keys()))
            return all_paths
        return all_paths

    for move in POSSIBLE_MOVES:
        if continue_is_possible(move, row, col, single_path, cur_word, board, word):
            find_length_n_words_helper(n, board, word, cur_word, single_path, all_paths,
                                       index_n+len(board[row + move[0]][col + move[1]]),
                                       row+move[ROW], col+move[COL])
        else:
            continue
        if len(single_path) != 0:
            single_path.popitem()

    return all_paths


def max_score_paths(board, words):
    """
    This function returns the paths the user must select in order to get the maximum score in the game
    :param board: game board
    :param words: iterable object
    :return: list of paths that entitle the player with maximum score
    """
    all_paths = []
    for n in range(1, BOARD_SIZE**2 + 1):
        all_paths.append(find_length_n_paths(n, board, words))
    exist_words_dict = {}
    for path_n in all_paths:
        if not path_n:
            continue
        for path in path_n:
            word = get_word(path, board)
            if word in exist_words_dict:
                choose_higher_score(exist_words_dict, path, word)
            else:
                exist_words_dict.update({word: path})
    return list(exist_words_dict.values())


def get_word(path, board):
    """
    This function returns the string at the position of the path coordinates on the board
    :param path: list of tuples represents the coordinates
    :param board: game board
    :return: string
    """
    word = ""
    for coord in path:
        word += board[coord[ROW]][coord[COL]]
    return word


def choose_higher_score(words_dict, cur_path, cur_word):
    """
    This function compares the length of the existing route with the length of the new found route
    and selects the highest
    :param words_dict: dictionary with existing words and paths
    :param cur_path: the new path to compare
    :param cur_word: the new word to compare
    :return: updated words dictionary
    """
    if len(words_dict[cur_word]) < len(cur_path):
        words_dict[cur_word] = cur_path
    return words_dict

