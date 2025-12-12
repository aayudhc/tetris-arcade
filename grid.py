import arcade, letters 
from scores import Scores

CELL_SIZE = 40 # 40 * 40 pixels
GRID_WIDTH = 12 # number of columns
GRID_HEIGHT = 15 # number of rows
GRID_H_SIZE = GRID_WIDTH * CELL_SIZE # 600 pixels
GRID_V_SIZE = GRID_HEIGHT * CELL_SIZE # 480 pixels
GRID_LINE_COLOUR = (243, 232, 255, 30)
BORDERING_BOX_COLOUR = (93, 0, 59, 196) #(243, 232, 255, 100)
BOX_MARGIN_COLOUR = (119, 18, 82)

''' each letter starts at row 1 column 4 '''
START_Y = 4
START_X = 1

''' position in relation to the grid '''
current_x = START_X
current_y = START_Y

''' co-ordinates of preview window '''
PREVIEW_Y = GRID_WIDTH + 1
PREVIEW_X = 5  # and goes till 8 


class Grid:
    def __init__(self):
        self.main_grid = self.create_grid()
        self.active_letter = letters.letter_T
        self.letter_rotation = 0
        self.copy_letter_to_grid()
        self.game_over = False
        self.scores = Scores()

    def create_grid(self) -> list[list]:
        ''' creates the tetris grid of required dimensions '''
        grid = []

        usual_row = [0 for _ in range(GRID_WIDTH)]
        usual_row[0] = -1
        usual_row[-1] = -1
        for x in range(GRID_HEIGHT - 1):
            grid.append(usual_row.copy())

        grid.append([-1 for _ in range(GRID_WIDTH)])

        #for i in range(15):
        #    print(grid[i])

        return grid
    
    def draw_grid_lines(self) -> None:
        # horizontal lines
        for y in range(1, GRID_HEIGHT):
            arcade.draw_line(0, y * CELL_SIZE,
                              GRID_H_SIZE, y * CELL_SIZE, 
                              GRID_LINE_COLOUR)

        # vertical lines
        for x in range(1, GRID_WIDTH):
            arcade.draw_line(x * CELL_SIZE, 0, 
                             x * CELL_SIZE, GRID_V_SIZE, 
                             GRID_LINE_COLOUR)
                
    def get_cell(self, x0: int, x1: int) -> int: #x0 & x1 are the 2 dimensions of matrix
        return self.main_grid[x0][x1]
    
    def set_cell(self, x0: int, x1: int, val: int) -> None: #x0 & x1 are the 2 dimensions of matrix
        self.main_grid[x0][x1] = val

    def draw_walls(self) -> None:
        ''' x & y get flipped as we convert from matrix form to grid '''
        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                if self.get_cell(x, y) != -1:
                    continue

                square_y: int = (GRID_HEIGHT - x - 1) * CELL_SIZE
                square_x: int = y * CELL_SIZE

                #arcade.draw_lrbt_rectangle_filled(square_x, square_x + CELL_SIZE, 
                #                                  square_y, square_y + CELL_SIZE, 
                #                                  BORDERING_BOX_COLOUR)
                arcade.draw_lbwh_rectangle_outline(square_x, square_y, 
                                                   CELL_SIZE, CELL_SIZE, 
                                                   BOX_MARGIN_COLOUR)
                arcade.draw_lbwh_rectangle_filled(square_x, square_y, 
                                                   CELL_SIZE, CELL_SIZE, 
                                                   BORDERING_BOX_COLOUR)

    def can_copy_letter_to_grid(self) -> bool:
        pattern = self.active_letter[0]

        for x in range(len(pattern) + START_X - 1, START_X - 1, -1):
            for y in range(START_Y, START_Y + len(pattern[0])):
                if pattern[x - START_X][y - START_Y] == 0:
                    continue

                if self.get_cell(x, y) != 0:
                    self.game_over = True
                    return False
                
        return True

    def copy_letter_to_grid(self) -> None:
        ''' copies active letter to grid '''
        if not self.can_copy_letter_to_grid():
            return

        pattern = self.active_letter[0]

        for x in range(len(pattern) - 1, -1, -1):
            for y in range(len(pattern[0])):
                if pattern[x][y] == 0:
                    continue

                self.set_cell(x + START_X, y + START_Y, pattern[x][y])

    def draw_letters(self) -> None:
        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                if self.get_cell(x, y) in (0, -1):
                    continue

                square_y = (GRID_HEIGHT - x - 1) * CELL_SIZE
                square_x = y * CELL_SIZE

                #arcade.draw_lbwh_rectangle_filled(square_x, square_y, 
                #                                  CELL_SIZE, CELL_SIZE, 
                #                                  letters.letter_T['colour'])
                arcade.draw_lbwh_rectangle_filled(square_x, square_y, 
                                                  CELL_SIZE, CELL_SIZE, 
                                                  letters.letters_list[self.get_cell(x, y) - 1]['colour'])
                arcade.draw_lbwh_rectangle_outline(square_x, square_y, 
                                                  CELL_SIZE, CELL_SIZE, 
                                                  BOX_MARGIN_COLOUR)
                
    def clear_grid(self) -> None:
        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                if self.get_cell(x, y) in [0, -1]:
                    continue

                self.set_cell(x, y, 0)

    def clear_active_letter(self) -> None:
        pattern = self.active_letter[self.letter_rotation]
        for x in range(current_x, current_x + len(pattern)):
            for y in range(current_y, current_y + len(pattern[0])):
                if pattern[x - current_x][y - current_y] == 0:
                    continue

                self.set_cell(x, y, 0)

    def can_rotate_letter(self) -> bool:
        pattern_current = self.active_letter[self.letter_rotation]
        pattern_next = self.active_letter[(self.letter_rotation + 1) % self.active_letter['rotation_count']]

        # print([row for row in self.main_grid])

        for x in range(len(pattern_next)):
            for y in range(len(pattern_next[0])):
                if x < len(pattern_current) and y < len(pattern_current[0]):
                    if pattern_current[x][y] != 0: # skips check if place curruntly occupied by old block
                        continue

                if pattern_next[x][y] == 0:
                    continue

                if self.main_grid[x + current_x][y + current_y] != 0: # if its occupied
                    return False

        return True

    def rotate_letter(self) -> None:
        if not self.can_rotate_letter():
            return

        self.clear_active_letter()

        self.letter_rotation = (self.letter_rotation + 1) % self.active_letter['rotation_count']

        pattern = self.active_letter[self.letter_rotation]
        for x in range(len(pattern)):
            for y in range(len(pattern[0])):
                if pattern[x][y] == 0:
                    continue

                if self.get_cell(x + current_x, y + current_y) == 0: # when its blank
                    self.set_cell(x + current_x, y + current_y, pattern[x][y])

    def can_move(self, x0: int, x1: int) -> bool:
        if self.get_cell(x0, x1) == 0:
            return True
        
        return False
    
    def _can_move_left(self) -> bool:
        test_grid = []
        pattern = self.active_letter[self.letter_rotation]
        
        if current_y - 1 < 0:
            return False

        for x in range(current_x, current_x + len(pattern)):
            test_grid.append(self.main_grid[x][current_y - 1 : current_y + len(pattern[0])])
        #print([row for row in test_grid], sep='\n')

        for y in range(len(test_grid[0]) - 1):
            for x in range(len(test_grid)):
                if test_grid[x][y + 1] == 0: # if letter is empty at that location
                    continue

                if test_grid[x][y] != 0: # if letter can't be accepted in new position
                    return False
                
                # doing the shifting
                test_grid[x][y] = test_grid[x][y + 1]
                test_grid[x][y + 1] = 0

        return True
    
    def can_move_left(self) -> bool:
        pattern = self.active_letter[self.letter_rotation]

        for x in range(0, len(pattern)):
            for y in range(0, len(pattern[0])):
                if pattern[x][y] == 0: # if block is empty, no need to check
                    continue
                if y - 1 >= 0 and pattern[x][y - 1] != 0: # if the block its moving to was occupied by the same pattern, no need to check
                    continue

                if self.get_cell(x + current_x, y + current_y - 1) != 0:
                    return False
                
        return True
    
    def move_left(self) -> None:
        global current_y # current_y gets modified here

        if not self.can_move_left():
            return

        pattern = self.active_letter[self.letter_rotation]
        for x in range(len(pattern)):
            for y in range(len(pattern[0])):
                # val = self.get_cell(x + current_x, y + current_y)
                val = pattern[x][y] # disregards unrelated blocks

                if val in [0, -1]:
                    continue

                self.set_cell(x + current_x, y + current_y - 1, val)
                self.set_cell(x + current_x, y + current_y, 0)
        
        current_y -= 1 # changes only once for the whole letter

    def _can_move_right(self) -> bool:
        test_grid = []
        pattern = self.active_letter[self.letter_rotation]

        for x in range(current_x, current_x + len(pattern)):
            test_grid.append(self.main_grid[x][current_y : current_y + len(pattern[0]) + 1])

        for y in range(len(test_grid[0]) - 2, -1, -1):
            for x in range(len(test_grid)):
                if test_grid[x][y] == 0: # if letter is empty at that location
                    continue

                if test_grid[x][y + 1] != 0: # if letter can't be accepted in new position
                    return False
                
                # doing the shifting
                test_grid[x][y + 1] = test_grid[x][y]
                test_grid[x][y] = 0

        return True
    
    def can_move_right(self) -> bool:
        pattern = self.active_letter[self.letter_rotation]

        for x in range(0, len(pattern)):
            for y in range(0, len(pattern[0])):
                if pattern[x][y] == 0: # if block is empty, no need to check
                    continue
                if y + 1 < len(pattern[0]) and pattern[x][y + 1] != 0: # if the block its moving to was occupied by the same pattern, no need to check
                    continue

                if self.get_cell(x + current_x, y + current_y + 1) != 0:
                    return False
                
        return True

    def move_right(self) -> None:
        global current_y # current_y gets modified here

        if not self.can_move_right():
            return

        pattern = self.active_letter[self.letter_rotation]
        for x in range(len(pattern)):
            for y in range(len(pattern[0]) - 1, -1, -1):
                # val = self.get_cell(x + current_x, y + current_y)
                val = pattern[x][y] # disregards unrelated blocks

                if val in [0, -1]:
                    continue

                self.set_cell(x + current_x, y + current_y + 1, val)
                self.set_cell(x + current_x, y + current_y, 0)
        
        current_y += 1 # changes only once for the whole letter

    def clear_row(self, x: int) -> None:
        self.main_grid.pop(x)
        self.main_grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        self.main_grid[0][0] = -1
        self.main_grid[0][-1] = -1

    def check_clears(self) -> None:
        pattern = self.active_letter[self.letter_rotation]
        rows_to_clear = []
        #for x in range(GRID_HEIGHT - 2, current_x - 1, -1): 
        for x in range(current_x, GRID_HEIGHT - 1):
            # lower bound is max as fallen blocks may complete lines below
            if 0 in self.main_grid[x]: # not filled
                continue

            rows_to_clear.append(x) 
            self.scores.record() # record number of lines cleared
        
        for x in rows_to_clear:
            self.clear_row(x)
        self.scores.convert_points() # convert recored lines to points

    def next_letter(self) -> None:
        global current_x, current_y

        self.active_letter = letters.get_next_letter()
        current_x = START_X
        current_y = START_Y

        self.letter_rotation = 0
        self.copy_letter_to_grid()
    
    def can_move_down(self) -> bool:
        ''' Checks if the active block can move down '''
        pattern = self.active_letter[self.letter_rotation]
        accounted_cols = []
        for x in range(current_x + len(pattern) - 1, current_x - 1, -1):
            for y in range(current_y, current_y + len(pattern[0])):
                if y in accounted_cols: # only check lowermost filled block in each column
                    continue

                if pattern[x - current_x][y - current_y] == 0: # if the current block is empty, skip it
                    continue

                if self.main_grid[x + 1][y] != 0: # if the lower block is not empty
                    return False
                
                accounted_cols.append(y)
                
        return True

    def move_down(self) -> None:
        ''' Moves down the active block in the grid, if it can '''
        global current_x

        if not self.can_move_down():
            self.check_clears() # check if a row is cleared
            self.next_letter() # switch to next letter
            return
        
        pattern = self.active_letter[self.letter_rotation]
        for x in range(len(pattern) - 1, -1, -1):
            for y in range(len(pattern[0])):
                if pattern[x][y] == 0:
                    continue

                self.set_cell(x + current_x + 1, y + current_y, pattern[x][y])
                self.set_cell(x + current_x, y + current_y, 0)

        current_x += 1

    def draw_next_letter(self) -> None:
        letter = letters.peek_next_letter()
        pattern = letter[0]
        for x in range(len(pattern)):
            for y in range(len(pattern[0])):
                if pattern[x][y] == 0:
                    continue

                arcade.draw_lbwh_rectangle_filled((PREVIEW_Y + y) * CELL_SIZE, ( PREVIEW_X + 3 - x) * CELL_SIZE, 
                                                  CELL_SIZE, CELL_SIZE, letter['colour'])
                arcade.draw_lbwh_rectangle_outline((PREVIEW_Y + y) * CELL_SIZE, ( PREVIEW_X + 3 - x) * CELL_SIZE, 
                                                   CELL_SIZE, CELL_SIZE, BORDERING_BOX_COLOUR)
                
    def draw_preview_box(self) -> None:
        arcade.draw_lbwh_rectangle_outline(PREVIEW_Y * CELL_SIZE - 1, PREVIEW_X * CELL_SIZE - 1, 
                                           3 * CELL_SIZE + 1, 4 * CELL_SIZE + 1, GRID_LINE_COLOUR)

    def draw_all(self) -> None:
        self.draw_grid_lines()
        self.draw_walls()
        self.draw_letters()
        self.draw_next_letter()
        #self.draw_preview_box()


# grid = Grid()
# print(grid.main_grid)
