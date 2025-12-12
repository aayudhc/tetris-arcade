# describes letters or tetrominoes
import random
random.seed()

letter_T = {
    0: [[1, 1, 1],
        [0, 1, 0]],
    
    1: [[0, 0, 1],
        [0, 1, 1],
        [0, 0, 1]],

    2: [[0, 0, 0],
        [0, 1, 0],
        [1, 1, 1]],

    3: [[1, 0],
        [1, 1],
        [1, 0]],

    'colour': (0, 103, 79, 222), #(20, 191, 177, 140),
    'rotation_count': 4
}

letter_I = {
    0: [[0, 2],
        [0, 2],
        [0, 2],
        [0, 2]],

    1: [[0, 0, 0, 0],
        [2, 2, 2, 2]],

    'colour': (209, 41, 192, 209),
    'rotation_count': 2
}

letter_O = {
    0: [[3, 3],
        [3, 3]],

    'colour': (69, 30, 128, 207), #(63, 0, 128, 166), #(116, 44, 188, 217), 
    'rotation_count': 1
}

letter_Z = {
    0: [[4, 4, 0],
        [0, 4, 4]],

    1: [[0, 0, 4],
        [0, 4, 4],
        [0, 4, 0]],

    'colour': (229, 229, 0, 255),
    'rotation_count': 2
}

letter_S = {
    0: [[0, 5, 5],
        [5, 5, 0]],

    1: [[5, 0],
        [5, 5],
        [0, 5]],

    'colour': (229, 0, 74, 168),
    'rotation_count': 2
}

letter_L = {
    0: [[0, 6, 0],
        [0, 6, 0],
        [0, 6, 6]],

    1: [[0, 0, 0],
        [6, 6, 6],
        [6, 0, 0]],

    2: [[6, 6],
        [0, 6],
        [0, 6]],

    3: [[0, 0, 6],
        [6, 6, 6]],

    'colour': (71, 200, 10, 168),
    'rotation_count': 4
}

letter_J = {
    0: [[0, 7],
        [0, 7],
        [7, 7]],

    1: [[7, 0, 0],
        [7, 7, 7],
        [0, 0, 0]],

    2: [[0, 7, 7],
        [0, 7, 0],
        [0, 7, 0]],

    3: [[0, 0, 0],
        [7, 7, 7],
        [0, 0, 7]],

    'colour': (180, 103, 79, 230), # (111, 37, 14, 230),
    'rotation_count': 4
}

letters_list = [letter_T, letter_I, letter_O, letter_Z, letter_S, letter_L, letter_J]

letters_bag: list = letters_list.copy() 
random.shuffle(letters_bag)

def peek_next_letter():
    return letters_bag[-1]

def get_next_letter():
    global letters_bag
    letter = letters_bag.pop()

    if len(letters_bag) == 0:
        letters_bag = letters_list.copy() 
        random.shuffle(letters_bag)

    return letter
