# ============================================================
# NOKIA SNAKE — TODO LIST
# ============================================================


# ---------- PHASE 1 : PROJECT SETUP ----------

# [1] Create project structure
# [1] Create main.py
# [1] Create game window
# [1] Set window title
# [1] Make window non-resizable
# [1] Create game canvas


# ---------- PHASE 2 : GAME BOARD ----------

# [1] Define grid dimensions
# [1] Define cell size
# [1] Draw game area
# [1] Create monochrome Nokia-style color scheme


# ---------- PHASE 3 : SNAKE ----------

# [1] Create Snake class
# [1] Store snake body positions
# [1] Give snake a starting position
# [1] Give snake a starting direction
# [1] Draw snake on canvas


# ---------- PHASE 4 : MOVEMENT ----------

# [1] Create game tick
# [1] Move snake automatically
# [ ] Bind arrow keys
# [ ] Change movement direction
# [ ] Prevent immediate 180° turns


# ---------- PHASE 5 : FOOD ----------

# [ ] Create Food class
# [ ] Generate random food position
# [ ] Prevent food spawning inside snake
# [ ] Draw food
# [ ] Detect snake eating food
# [ ] Grow snake after eating


# ---------- PHASE 6 : COLLISION & GAME OVER ----------

# [ ] Detect wall collision
# [ ] Detect snake collision with itself
# [ ] Stop game loop after collision
# [ ] Display GAME OVER
# [ ] Add restart control


# ---------- PHASE 7 : SCORE & DIFFICULTY ----------

# [ ] Track score
# [ ] Display score
# [ ] Increase score when food is eaten
# [ ] Gradually increase snake speed


# ---------- PHASE 8 : NOKIA POLISH ----------

# [ ] Create Nokia 3310-inspired screen appearance
# [ ] Polish snake appearance
# [ ] Polish food appearance
# [ ] Add simple start screen
# [ ] Test movement and collisions
# [ ] Refactor and clean up code
# [ ] Write README.md
# [ ] Release v1.0


# ============================================================
# THE SACRED RULE
# ============================================================

# Snake is allowed to be small.
#
# No databases.
# No AI.
# No accounts.
# No 3D.
# No 47-class architecture.
#
# Make snake.
# Snake eats food.
# Snake gets longer.
# Snake dies.
# Ship it.
#
# ============================================================

import tkinter as tk
import random

class GUI:
    WIDTH = 500
    HEIGHT = 500

    LCD_BACKGROUND = "#9BBC0F"
    LCD_DARK = "#0F380F"

    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window,width=self.WIDTH,height=self.HEIGHT,bg=self.LCD_BACKGROUND)

        self.create_window()
        self.canvas.pack()

    def create_window(self):
        self.window.title('Snake')
        self.window.configure(background=self.LCD_BACKGROUND)
        self.window.resizable(False,False)
        self.window.geometry(f'{self.WIDTH}x{self.HEIGHT}')

    def create_grid(self):
        for row in range(Board.ROWS):
            for col in range(Board.COLS):
                x1 = col * Board.CELL_SIZE
                y1 = row * Board.CELL_SIZE
                x2 = x1 + Board.CELL_SIZE
                y2 = y1 + Board.CELL_SIZE

                self.canvas.create_rectangle(x1,y1,x2,y2,outline=self.LCD_BACKGROUND)

    def _draw_snake(self,body):
        self.canvas.delete('snake')

        for row,col in body:
            x1 = col * Board.CELL_SIZE
            y1 = row * Board.CELL_SIZE
            x2 = x1 + Board.CELL_SIZE
            y2 = y1 + Board.CELL_SIZE

            self.canvas.create_rectangle(x1,y1,x2,y2,fill=self.LCD_DARK,tags='snake')

    def schedule_tick(self, delay, callback):
        self.window.after(delay,callback)



class Board:
    ROWS = 20
    COLS = 20
    CELL_SIZE = 25

    def __init__(self):
        self.grid = [
            [None for _ in range(self.COLS)]
            for _ in range(self.ROWS)
            ]

class Snake:
    STARTING_LENGTH = 4

    def __init__(self):
        self.middle_row = Board.ROWS//2
        self.middle_col = Board.COLS//2

        self.body = [
            (self.middle_row,self.middle_col - offset)
            for offset in range(self.STARTING_LENGTH)
        ]

        self.direction = (0,1)

    def move(self):
        row, col = self.body[0]
        direction_row, direction_col = self.direction

        new_row = row + direction_row
        new_col = col + direction_col

        self.body.insert(0,(new_row,new_col))
        self.body.pop(-1)

class Game:
    def __init__(self,gui,board,snake):
        self.gui = gui
        self.board = board
        self.snake = snake

    def game_tick(self):
        self.snake.move()
        self.gui._draw_snake(self.snake.body)
        self.gui.schedule_tick(300,self.game_tick)

def run():
    gui = GUI()
    board = Board()
    snake = Snake()

    game = Game(gui,board,snake)

    gui.create_grid()
    gui._draw_snake(snake.body)

    game.game_tick()

    gui.window.mainloop()


if __name__ == '__main__':
    run()





