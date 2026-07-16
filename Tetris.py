#thinkter design
#oop focus

# ============================================================
# TETRIS — TODO LIST
# ============================================================

# ---------- PHASE 1: WINDOW + CANVAS ----------
# [1] Import tkinter
# [1] Create Tk window
# [1] Set window title: "Tetris"
# [1] Define constants:
#       - CELL_SIZE
#       - ROWS = 20
#       - COLS = 10
# [1] Create Canvas with size: COLS * CELL_SIZE x ROWS * CELL_SIZE
# [1] Draw a visible 10x20 grid
# [1] Start root.mainloop()

# ---------- PHASE 2: BOARD CLASS ----------
# [1] Create Board class
# [1] Create 2D grid:
#       self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
# [1] Add Board.draw(canvas)
# [1] Draw empty cells
# [1] Draw locked/fixed blocks with their colors
# [1] Add Board.is_inside(row, col)

# ---------- PHASE 3: FIRST TEST PIECE ----------
# [1] Create Piece class
# [1] Add attributes:
#       - shape
#       - color
#       - row
#       - col
# [1] Start with only O (square) piece
# [1] Add Piece.draw(canvas)
# [1] Spawn piece at top center
# [1] Draw active piece over the board

# ---------- PHASE 4: GAME CLASS + TIMER ----------
# [1] Create Game class
# [1] Store:
#       - root
#       - canvas
#       - board
#       - active_piece
# [1] Create Game.draw()
# [1] Create Game.game_tick()
# [1] Use root.after(500, self.game_tick)
# [1] Move active piece down automatically
# [1] Redraw after each tick

# ---------- PHASE 5: PLAYER MOVEMENT ----------
# [1] Bind keyboard events
# [1] Left arrow -> move piece left
# [1] Right arrow -> move piece right
# [1] Down arrow -> soft drop
# [1] Prevent piece from leaving board boundaries
# [1] Redraw after movement

# ---------- PHASE 6: COLLISION DETECTION ----------
# [1] Create Board.is_valid_position(piece, row_offset=0, col_offset=0)
# [1] Check collision with left wall
# [1] Check collision with right wall
# [1] Check collision with bottom
# [1] Check collision with locked blocks
# [1] Only move piece if new position is valid

# ---------- PHASE 7: LOCKING PIECES ----------
# [1] When piece cannot move down:
#       - add piece blocks to board.grid
#       - spawn a new piece
# [1] Create Board.lock_piece(piece)
# [1] Check if newly spawned piece collides
# [1] If it collides -> game over

# ---------- PHASE 8: ALL TETROMINOES ----------
# [1] Add I piece
# [1] Add O piece
# [1] Add T piece
# [1] Add S piece
# [1] Add Z piece
# [1] Add J piece
# [1] Add L piece
# [1] Give every piece a color
# [1] Randomly choose a new piece

# ---------- PHASE 9: ROTATION ----------
# [1] Bind Up arrow -> rotate piece
# [1] Create Piece.rotate()
# [1] Rotate piece matrix clockwise
# [1] Only rotate if new rotation is valid
# [1] Later: add simple wall kicks

# ---------- PHASE 10: CLEARING LINES ----------
# [1] Create Board.clear_full_lines()
# [1] Detect full rows
# [1] Remove full rows
# [1] Add empty rows at the top
# [1] Return number of cleared lines
# [1] Redraw board

# ---------- PHASE 11: SCORE + LEVEL ----------
# [1] Add score attribute to Game
# [1] Add score Label beside canvas
# [1] Add points:
#       1 line = 100
#       2 lines = 300
#       3 lines = 500
#       4 lines = 800
# [1] Track total cleared lines
# [1] Add levels
# [1] Increase falling speed every level

# ---------- PHASE 12: GAME STATES ----------
# [ ] Add game_over attribute
# [ ] Display "GAME OVER"
# [ ] Bind R -> restart game
# [ ] Bind P -> pause/unpause
# [ ] Prevent movement when paused or game over

# ---------- PHASE 13: EXTRA FEATURES ----------
# [ ] Next piece preview
# [ ] Hold piece with C
# [ ] Ghost piece / landing preview
# [ ] Sound effects
# [ ] Background music
# [ ] Line clear animation
# [ ] Save high score in JSON file
# [ ] Start menu
# [ ] Difficulty selection
# [ ] Different color themes

# ============================================================


import tkinter as tk
import random


class Board:
    ROWS = 20
    COLS = 10
    CELL_SIZE = 30

    def __init__(self):
        self.grid = [
            [None for _ in range(Board.COLS)]
            for _ in range(Board.ROWS)
            ]

    def is_inside(self,row,col):
        if 0 <= row < Board.ROWS and 0 <= col < Board.COLS:
            return True
        return False

    def is_valid_position(self,piece,row_offset = 0, col_offset = 0):
        for shape_row in range(len(piece.shape)):
            for shape_col in range(len(piece.shape[shape_row])):

                #checks for ghost blocks
                if piece.shape[shape_row][shape_col] == 1:
                    board_row = piece.row + shape_row + row_offset
                    board_col = piece.col + shape_col + col_offset

                    if not self.is_inside(board_row,board_col):
                        return False

                    if self.grid[board_row][board_col] is not None:
                        return False

        return True

    def lock_piece(self, piece):
        for shape_row in range(len(piece.shape)):
            for shape_col in range(len(piece.shape[shape_row])):

                if piece.shape[shape_row][shape_col] == 1:
                    board_row = piece.row + shape_row
                    board_col = piece.col + shape_col

                    self.grid[board_row][board_col] = piece.color

    def draw(self, canvas):
        for row in range(Board.ROWS):
            for col in range(Board.COLS):

                x1 = col * Board.CELL_SIZE
                y1 = row * Board.CELL_SIZE
                x2 = x1 + Board.CELL_SIZE
                y2 = y1 + Board.CELL_SIZE

                color = self.grid[row][col]

                if color is None:
                    color = 'Black'

                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill = color,
                    outline = 'gray'
                )

    def clear_full_lines(self):
        cleared_lines = 0

        new_grid = []

        for row in self.grid:
            if None in row:
                new_grid.append(row)
            else:
                cleared_lines += 1

        while len(new_grid) < Board.ROWS:
            new_grid.insert(0,[None for _ in range(Board.COLS)])

        self.grid = new_grid

        return cleared_lines

PIECES = {
    'O':{
        'shape':[
            [1,1],
            [1,1]
            ],
        'color':'cyan'
    },
    'I':{
        'shape':[
            [1,1,1,1]
            ],
        'color':'yellow'
    },
    'T':{
        'shape':[
            [0,1,0],
            [1,1,1]
        ],
        'color':'purple'
    },
    'S':{
        'shape':[
            [0,1,1],
            [1,1,0]
        ],
        'color':'green'
    },
    'Z':{
        'shape':[
            [1,1,0],
            [0,1,1]
        ],
        'color':'red'
    },
    'J':{
        'shape':[
            [0,0,1],
            [1,1,1]
        ],
        'color':'orange'
    },
    'L':{
        'shape':[
            [1,0,0],
            [1,1,1]
        ],
        'color':'blue'
    }
}

class Piece:
    def __init__(self):
        piece_name = random.choice(list(PIECES.keys()))

        piece = PIECES[piece_name]

        self.name = piece_name
        self.shape = [row[:] for row in piece['shape']]
        self.color = piece['color']


        #Top center position
        self.row = 0
        self.col = 4

    def draw(self,canvas):
        for shape_row in range(len(self.shape)):
            for shape_col in range(len(self.shape[shape_row])):

                #Checks if position contains a block
                if self.shape[shape_row][shape_col] == 1:

                    #Coordinate conversion
                    board_row = self.row + shape_row
                    board_col = self.col + shape_col

                    x1 = board_col * Board.CELL_SIZE
                    y1 = board_row * Board.CELL_SIZE
                    x2 = x1 + Board.CELL_SIZE
                    y2 = y1 + Board.CELL_SIZE

                    canvas.create_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill = self.color,
                        outline = 'gray'
                    )

    def rotate(self):
        rows = len(self.shape)
        cols = len(self.shape[0])

        new_shape = []

        for col in range(cols):
            new_row = []
            for row in range(rows -1,-1,-1):
                new_row.append(self.shape[row][col])

            new_shape.append(new_row)

        self.shape = new_shape


class TetrisGUI:
    CELL_SIZE = 30
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tetris")

        canvas_width = self.CELL_SIZE * self.BOARD_WIDTH
        canvas_height = self.CELL_SIZE * self.BOARD_HEIGHT
        sidebar_width = canvas_width // 2

        window_width = canvas_width + sidebar_width
        window_height = canvas_height

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self._setup_window(window_width,window_height)
        self._create_widgets(canvas_width,canvas_height,sidebar_width)


    def _setup_window(self,window_width,window_height):

        self.window.geometry(f"{window_width}x{window_height}")
        self.window.resizable(False,False)

    def _create_widgets(self,canvas_width,canvas_height,sidebar_width):

        self.canvas = tk.Canvas(
            self.window,
            width = canvas_width,
            height = canvas_height,
            bg = 'black'
        )
        self.canvas.pack(side='left')

        self.sidebar = tk.Frame(
            self.window,
            width=sidebar_width,
            height=canvas_height,
            bg='black',
        )
        self.sidebar.pack(side= 'right')
        self.sidebar.pack_propagate(False)

        self.score_display = tk.Label(
            self.sidebar,
            text = 'SCORE = 0 ',
            bg='black',
            fg='white'
        )
        self.score_display.pack(pady=(20,10))

        self.lines_display = tk.Label(
            self.sidebar,
            text='Lines cleared = 0  ',
            bg='black',
            fg='white'
        )
        self.lines_display.pack(pady=10)

        self.level_display = tk.Label(
            self.sidebar,
            text='Level: 0 ',
            bg='black',
            fg='white'
        )
        self.level_display.pack(pady=10)


    def draw(self,board,active_piece,game_over,score,total_lines,level):
        self.canvas.delete('all')

        board.draw(self.canvas)
        active_piece.draw(self.canvas)

        if game_over:
            self._draw_game_over()

        self.score_display.config(text = f'SCORE = {score}')
        self.lines_display.config(text = f'Lines cleared = {total_lines}')
        self.level_display.config(text = f'Level: {level+1}')

    def _draw_game_over(self):
        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2

        self.canvas.create_text(
            center_x,
            center_y,
            text='GAME OVER',
            font=('Arial', 24, 'bold'),
            fill='red'

        )

    def bind_keys(self,game):
        self.window.bind('<Left>',game.move_left)
        self.window.bind('<Right>',game.move_right)
        self.window.bind('<Up>',game.rotate_piece)
        self.window.bind('<Down>',game.move_down)

    def run(self):
        self.window.mainloop()


class Game:
    SCORING = {
        0: 0,
        1: 100,
        2: 300,
        3: 500,
        4: 800
    }

    MAX_LVL = 8

    def __init__(self):
        self.gui = TetrisGUI()

        self.board = Board()
        self.active_piece = Piece()
        self.game_over = False

        self.score = 0
        self.total_lines = 0
        self.level = 0
        self.fall_speed = 500

        self.gui.bind_keys(self)

        self.draw()
        self.game_tick()



    def draw(self):
        self.gui.draw(
            self.board,
            self.active_piece,
            self.game_over,
            self.score,
            self.total_lines,
            self.level
        )

    def try_move_down(self):
        if self.board.is_valid_position(self.active_piece,row_offset = 1):
            self.active_piece.row += 1

        else:
            self.board.lock_piece(self.active_piece)

            lines = self.board.clear_full_lines()
            self.update_game_stats(lines)

            self.spawn_piece()

            self.check_game_over()




    def update_game_stats(self,lines):
        self.total_lines += lines
        self.score += Game.SCORING[lines]
        self.update_level()

    def spawn_piece(self):
        self.active_piece = Piece()


    def check_game_over(self):
        if not self.board.is_valid_position(self.active_piece):
            print("GAME OVER!")
            self.game_over = True

    def game_tick(self):
        if not self.game_over:
            self.try_move_down()

        self.draw()

        self.gui.window.after(self.fall_speed,self.game_tick)

    def update_level(self,):
        self.level = self.total_lines//20

        if self.level >= Game.MAX_LVL:
            self.level = Game.MAX_LVL

        self.fall_speed = 500 - (self.level * 50)



    def move_left(self, event):
        if self.game_over:
            return

        if self.board.is_valid_position(
            self.active_piece,
            col_offset=-1
        ):
            self.active_piece.col -= 1
            self.draw()

    def move_right(self, event):
        if self.game_over:
            return

        if self.board.is_valid_position(
            self.active_piece,
            col_offset=+1
        ):
            self.active_piece.col += 1
            self.draw()

    def move_down(self, event):
        if self.game_over:
            return

        if not self.game_over:
            self.try_move_down()
            self.draw()

    def rotate_piece(self, event):
        if self.game_over:
            return

        old_col = self.active_piece.col
        old_shape = [row[:] for row in self.active_piece.shape]
        kick_offsets = [-1,1,-2,2]

        self.active_piece.rotate()

        if self.board.is_valid_position(self.active_piece):
            self.draw()
            return

        else:
            for kick in kick_offsets:
                self.active_piece.col = old_col + kick

                if self.board.is_valid_position(self.active_piece):
                    self.draw()
                    return

        self.active_piece.col = old_col
        self.active_piece.shape = old_shape

        self.draw()

    def run(self):
        self.gui.run()

game = Game()
game.run()








