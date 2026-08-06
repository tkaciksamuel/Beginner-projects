
import tkinter as tk
import random

BOARD_ROWS = 20
BOARD_COLS = 10
CELL_SIZE = 30

PREVIEW_CELL_SIZE = 25

class Board:

    def __init__(self):
        self.grid = [
            [None for _ in range(BOARD_COLS)]
            for _ in range(BOARD_ROWS)
        ]

    def is_inside(self, row, col):
        if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            return True
        return False

    def is_valid_position(self, piece, row_offset=0, col_offset=0):
        for shape_row in range(len(piece.shape)):
            for shape_col in range(len(piece.shape[shape_row])):

                # checks for ghost blocks
                if piece.shape[shape_row][shape_col] == 1:
                    board_row = piece.row + shape_row + row_offset
                    board_col = piece.col + shape_col + col_offset

                    if not self.is_inside(board_row, board_col):
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

    def draw(self, canvas, clearing_rows):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):

                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = self.grid[row][col]

                if color is None:
                    color = 'Black'

                if row in clearing_rows:
                    color = 'White'

                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline='gray'
                )

    def get_full_rows(self):
        full_rows = []

        for i,row in enumerate(self.grid):
            if None not in row:
                full_rows.append(i)

        return full_rows

    def remove_full_rows(self,full_rows):
        for row_index in reversed(full_rows):
            self.grid.pop(row_index)
            self.grid.insert(0,[None for _ in range(BOARD_COLS)])


PIECES = {
    'O': {
        'shape': [
            [1, 1],
            [1, 1]
        ],
        'color': 'cyan'
    },
    'I': {
        'shape': [
            [1, 1, 1, 1]
        ],
        'color': 'yellow'
    },
    'T': {
        'shape': [
            [0, 1, 0],
            [1, 1, 1]
        ],
        'color': 'purple'
    },
    'S': {
        'shape': [
            [0, 1, 1],
            [1, 1, 0]
        ],
        'color': 'green'
    },
    'Z': {
        'shape': [
            [1, 1, 0],
            [0, 1, 1]
        ],
        'color': 'red'
    },
    'J': {
        'shape': [
            [0, 0, 1],
            [1, 1, 1]
        ],
        'color': 'orange'
    },
    'L': {
        'shape': [
            [1, 0, 0],
            [1, 1, 1]
        ],
        'color': 'blue'
    }
}


class Piece:
    START_ROW = 0
    START_COL = 4

    def __init__(self):
        piece_name = random.choice(list(PIECES.keys()))

        piece = PIECES[piece_name]

        self.name = piece_name
        self.shape = [row[:] for row in piece['shape']]
        self.color = piece['color']

        # Top center position
        self.row = self.START_ROW
        self.col = self.START_COL

    def rotate(self):
        rows = len(self.shape)
        cols = len(self.shape[0])

        new_shape = []

        for col in range(cols):
            new_row = []
            for row in range(rows - 1, -1, -1):
                new_row.append(self.shape[row][col])

            new_shape.append(new_row)

        self.shape = new_shape


class TetrisGUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tetris")

        canvas_width = CELL_SIZE * BOARD_COLS
        canvas_height = CELL_SIZE * BOARD_ROWS
        sidebar_width = canvas_width // 2

        self.center_x = canvas_width // 2
        self.center_y = canvas_height // 2

        window_width = canvas_width + sidebar_width
        window_height = canvas_height

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self._setup_window(window_width, window_height)
        self._create_widgets(canvas_width, canvas_height, sidebar_width)

    def _setup_window(self, window_width, window_height):

        self.window.geometry(f"{window_width}x{window_height}")
        self.window.resizable(False, False)

    def _create_widgets(self, canvas_width, canvas_height, sidebar_width):

        self.canvas = tk.Canvas(
            self.window,
            width=canvas_width,
            height=canvas_height,
            bg='black'
        )
        self.canvas.pack(side='left')

        self.sidebar = tk.Frame(
            self.window,
            width=sidebar_width,
            height=canvas_height,
            bg='black',
        )
        self.sidebar.pack(side='right')
        self.sidebar.pack_propagate(False)

        self.score_display = tk.Label(
            self.sidebar,
            text='SCORE = 0 ',
            bg='black',
            fg='white'
        )
        self.score_display.pack(pady=(20, 10))

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

        self.preview_label = tk.Label(
            self.sidebar,
            text='Next:',
            bg='black',
            fg='white'
        )
        self.preview_label.pack(pady=(10, 0))

        self.preview_canvas = tk.Canvas(
            self.sidebar,
            width=PREVIEW_CELL_SIZE * 4,
            height=PREVIEW_CELL_SIZE * 4,
            bg='black'
        )
        self.preview_canvas.pack(pady=10)

        self.held_label = tk.Label(
            self.sidebar,
            text='Held:',
            bg='black',
            fg='white'
        )
        self.held_label.pack(pady=(10,0))

        self.held_canvas = tk.Canvas(
            self.sidebar,
            width=PREVIEW_CELL_SIZE * 4,
            height=PREVIEW_CELL_SIZE * 4,
            bg='black'
        )
        self.held_canvas.pack(pady=10)

    def draw(self, board, active_piece,ghost_row,clearing_rows, next_piece,held_piece, game_over, paused, score, total_lines, level):
        self.canvas.delete('all')

        board.draw(self.canvas, clearing_rows)
        if not clearing_rows:
            self._draw_active_piece(active_piece)
            self._draw_ghost_piece(active_piece,ghost_row)
        self._draw_piece_preview(self.preview_canvas,next_piece)
        self._draw_piece_preview(self.held_canvas,held_piece)

        if game_over:
            self._draw_game_over()
        elif paused:
            self._draw_paused()

        self.score_display.config(text=f'SCORE = {score}')
        self.lines_display.config(text=f'Lines cleared = {total_lines}')
        self.level_display.config(text=f'Level: {level + 1}')

    def _draw_piece(
            self,canvas,
            piece,
            x,
            y,
            cell_size = CELL_SIZE,
            fill=None,
            outline='gray',
            width = 1
    ):

        if fill is None:
            fill = piece.color

        for shape_row in range(len(piece.shape)):
            for shape_col in range(len(piece.shape[shape_row])):

                # Checks if position contains a block
                if piece.shape[shape_row][shape_col] == 1:

                    x1 = x +shape_col * cell_size
                    y1 = y +shape_row * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size

                    canvas.create_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill=fill,
                        outline=outline,
                        width=width
                    )

    def _draw_active_piece(self,active_piece):
        x = active_piece.col * CELL_SIZE
        y = active_piece.row * CELL_SIZE

        self._draw_piece(self.canvas,active_piece,x,y)


    def _draw_piece_preview(self, canvas, piece):
        canvas.delete('all')

        if piece is None:
            return

        rows = len(piece.shape)
        cols = len(piece.shape[0])

        preview_width = 4 * PREVIEW_CELL_SIZE
        preview_height = 4 * PREVIEW_CELL_SIZE

        piece_width = PREVIEW_CELL_SIZE * cols
        piece_height = PREVIEW_CELL_SIZE * rows

        x_offset = (preview_width - piece_width) / 2
        y_offset = (preview_height - piece_height) / 2

        self._draw_piece(
            canvas,
            piece,
            x_offset,
            y_offset,
            cell_size=PREVIEW_CELL_SIZE
        )

    def _draw_ghost_piece(self,active_piece,ghost_row):
        x = active_piece.col * CELL_SIZE
        y = ghost_row * CELL_SIZE

        self._draw_piece(
            self.canvas,
            active_piece,
            x,
            y,
            fill = '',
            outline = active_piece.color,
            width = 2
        )


    def _draw_overlay(self, color):
        self.canvas.create_rectangle(
            0,
            0,
            self.canvas_width,
            self.canvas_height,
            fill=color,
            outline=''
        )

    def _draw_game_over(self):
        self._draw_overlay('#111111')

        self.canvas.create_text(
            self.center_x,
            self.center_y,
            text='GAME OVER',
            font=('Arial', 24, 'bold'),
            fill='red'

        )

    def _draw_paused(self):
        self._draw_overlay('#333333')

        self.canvas.create_text(
            self.center_x,
            self.center_y,
            text='PAUSED',
            font=('Arial', 24, 'bold'),
            fill='white'

        )


    def bind_keys(self, game):
        self.window.bind('<Left>', game.move_left)
        self.window.bind('<Right>', game.move_right)
        self.window.bind('<Up>', game.rotate_piece)
        self.window.bind('<Down>', game.move_down)
        self.window.bind('<r>', game.restart)
        self.window.bind('<p>', game.toggle_pause)
        self.window.bind('<c>', game.hold_piece)

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
        self.tick_id = None


        self.reset_game_state()

        self.gui.bind_keys(self)

        self.draw()
        self.game_tick()

    def reset_game_state(self):
        self.board = Board()

        self.active_piece = Piece()
        self.next_piece = Piece()

        self.held_piece = None
        self.can_hold = True

        self.game_over = False
        self.paused = False
        self.animating = False

        self.clearing_rows = []

        self.score = 0
        self.total_lines = 0
        self.level = 0
        self.fall_speed = 500

    def restart(self, event=None):
        if self.tick_id is not None:
            self.gui.window.after_cancel(self.tick_id)
            self.tick_id = None

        self.reset_game_state()
        self.draw()
        self.game_tick()

    def draw(self):
        ghost_row = self.get_landing_row()

        self.gui.draw(
            self.board,
            self.active_piece,
            ghost_row,
            self.clearing_rows,
            self.next_piece,
            self.held_piece,
            self.game_over,
            self.paused,
            self.score,
            self.total_lines,
            self.level
        )

    def try_move_down(self):
        if self.board.is_valid_position(self.active_piece, row_offset=1):
            self.active_piece.row += 1

        else:
            self.board.lock_piece(self.active_piece)

            full_rows = self.board.get_full_rows()

            if full_rows:
                self.animate_line_clear(full_rows)
                return

            self.finish_piece_turn()


    def finish_piece_turn(self):
        self.spawn_piece()
        self.can_hold = True
        self.check_game_over()

    def animate_line_clear(self, full_rows):
        self.animating = True
        self.clearing_rows = full_rows

        self.draw()

        self.gui.window.after(300,
                              self.finish_line_clear,
                              full_rows)


    def finish_line_clear(self,full_rows):
        self.board.remove_full_rows(full_rows)

        self.update_game_stats(len(full_rows))
        self.animating = False
        self.clearing_rows = []
        self.finish_piece_turn()

        self.draw()


    def update_game_stats(self, lines):
        self.total_lines += lines
        self.score += Game.SCORING[lines]
        self.update_level()

    def spawn_piece(self):
        self.active_piece = self.next_piece

        self.next_piece = Piece()

    def check_game_over(self):
        if not self.board.is_valid_position(self.active_piece):
            print("GAME OVER!")
            self.game_over = True

    def game_tick(self):
        if not self.locked_controls():
            self.try_move_down()

        self.draw()

        self.tick_id = (
            self.gui.window.after(
                self.fall_speed,
                self.game_tick
            )
        )

    def update_level(self, ):
        self.level = self.total_lines // 20

        if self.level >= Game.MAX_LVL:
            self.level = Game.MAX_LVL

        self.fall_speed = 500 - (self.level * 50)

    def move_left(self, event):
        if self.locked_controls():
            return

        if self.board.is_valid_position(
                self.active_piece,
                col_offset=-1
        ):
            self.active_piece.col -= 1
            self.draw()

    def move_right(self, event):
        if self.locked_controls():
            return

        if self.board.is_valid_position(
                self.active_piece,
                col_offset=+1
        ):
            self.active_piece.col += 1
            self.draw()

    def move_down(self, event):
        if self.locked_controls():
            return

        if not self.game_over:
            self.try_move_down()
            self.draw()

    def rotate_piece(self, event):
        if self.locked_controls():
            return

        old_col = self.active_piece.col
        old_shape = [row[:] for row in self.active_piece.shape]
        kick_offsets = [-1, 1, -2, 2]

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

    def locked_controls(self):
        return self.game_over or self.paused or self.animating

    def toggle_pause(self, event=None):
        if self.game_over:
            return

        self.paused = not self.paused
        self.draw()

    def hold_piece(self,event):
        if self.locked_controls():
            return

        if not self.can_hold:
            return

        if self.held_piece is None:
            self.held_piece = self.active_piece
            self.active_piece = self.next_piece
            self.next_piece = Piece()

        else:
            temp_piece = self.active_piece
            self.active_piece = self.held_piece
            self.held_piece = temp_piece

        self.active_piece.row = Piece.START_ROW
        self.active_piece.col = Piece.START_COL

        self.check_game_over()

        if not self.game_over:
            self.draw()

        self.can_hold = False

    def get_landing_row(self):
        landing_row = self.active_piece.row

        while self.board.is_valid_position(
            self.active_piece,
            row_offset = landing_row - self.active_piece.row + 1
        ):
            landing_row += 1

        return landing_row


    def run(self):
        self.gui.run()


game = Game()
game.run()








