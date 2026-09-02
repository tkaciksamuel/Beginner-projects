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
# [1] Bind arrow keys
# [1] Change movement direction
# [1] Prevent immediate 180° turns


# ---------- PHASE 5 : FOOD ----------

# [1] Create Food class
# [1] Generate random food position
# [1] Prevent food spawning inside snake
# [1] Draw food
# [1] Detect snake eating food
# [1] Grow snake after eating


# ---------- PHASE 6 : COLLISION & GAME OVER ----------

# [1] Detect wall collision
# [1] Detect snake collision with itself
# [1] Stop game loop after collision
# [1] Display GAME OVER
# [1] Add restart control


# ---------- PHASE 7 : SCORE & DIFFICULTY ----------

# [1] Track score
# [1] Display score
# [1] Increase score when food is eaten
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

    def _draw_food(self,position):
        self.canvas.delete("food")

        row, col = position

        x1 = col * Board.CELL_SIZE
        y1 = row * Board.CELL_SIZE
        x2 = x1 + Board.CELL_SIZE
        y2 = y1 + Board.CELL_SIZE

        self.canvas.create_rectangle(x1,y1,x2,y2,fill=self.LCD_DARK,tags='food')

    def draw_game_over(self,score):
        self.canvas.create_rectangle(0,0,self.WIDTH,self.HEIGHT,fill=self.LCD_DARK,tags='game_over')

        x = self.WIDTH//2
        y = self.HEIGHT//2
        self.canvas.create_text(x,
                                y,
                                text="GAME OVER!",
                                fill=self.LCD_BACKGROUND,
                                font=("Arial",32,"bold"),
                                tags='game_over'
                                )
        self.canvas.create_text(x,
                                y + 50,
                                text=f"SCORE: {score}",
                                fill=self.LCD_BACKGROUND,
                                font=("Arial",10,"bold italic"),
                                tags='game_over'
                                )

        self.canvas.create_text(x,
                                y + 100,
                                text="Press R to restart",
                                fill=self.LCD_BACKGROUND,
                                font=('Arial',15),
                                tags='game_over'
                                )


    def delete_game_over(self):
        self.canvas.delete("game_over")

    def schedule_tick(self, delay, callback):
        self.window.after(delay,callback)

    def bind_key(self,key, callback):
        self.window.bind(key,callback)


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

        self.can_change_direction = True
        self.growing = False

    def move(self):
        row, col = self.body[0]
        direction_row, direction_col = self.direction

        new_row = row + direction_row
        new_col = col + direction_col

        self.body.insert(0,(new_row,new_col))
        if not self.growing:
            self.body.pop(-1)

        self.can_change_direction = True
        self.growing = False

    def change_direction(self, new_direction):
        current_row, current_col = self.direction
        new_row, new_col = new_direction

        if not self.can_change_direction:
            return

        if (current_row + new_row == 0) and (current_col + new_col == 0):
            return

        self.direction = new_direction
        self.can_change_direction = False

    def grow(self):
        self.growing = True

    def reset(self):
        self.body = [
            (self.middle_row,self.middle_col - offset)
            for offset in range(self.STARTING_LENGTH)
        ]

        self.direction = (0,1)

        self.can_change_direction = True
        self.growing = False




class Food:
    def __init__(self):
        self.position = None

    def generate_position(self, occupied_positions):
        while True:
            row = random.randrange(Board.ROWS)
            col = random.randrange(Board.COLS)

            position = (row,col)

            if position not in occupied_positions:
                self.position = position
                return


class Game:
    MIN_SPEED = 100

    def __init__(self,gui,board,snake,food):
        self.gui = gui
        self.board = board
        self.snake = snake
        self.food = food

        self.game_over = False
        self.score = 0
        self.speed = 300

    def game_tick(self):
        self.snake.move()

        if self.wall_collision() or self.self_collision():
            self.game_over = True

        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.increase_score()
            self.food.generate_position(self.snake.body)
            self.gui._draw_food(self.food.position)

        self.gui._draw_snake(self.snake.body)

        if self.game_over:
            self.gui.draw_game_over(self.score)

        if not self.game_over:
            self.gui.schedule_tick(self.speed,self.game_tick)

    def move_up(self, event):
        self.snake.change_direction((-1,0))

    def move_right(self, event):
        self.snake.change_direction((0,1))

    def move_left(self, event):
        self.snake.change_direction((0,-1))

    def move_down(self, event):
        self.snake.change_direction((1,0))

    def wall_collision(self):
        row, col = self.snake.body[0]

        if (0 <= row < Board.ROWS) and (0 <= col < Board.COLS):
            return False

        return True

    def self_collision(self):
        if self.snake.body[0] in self.snake.body[1:]:
            return True

        return False

    def increase_score(self):
        self.score += 1

    def restart(self, event):
        if not self.game_over:
            return

        self.game_over = False
        self.score = 0

        self.snake.reset()

        self.food.generate_position(self.snake.body)

        self.gui.delete_game_over()
        self.gui._draw_snake(self.snake.body)
        self.gui._draw_food(self.food.position)

        if not self.game_over:
            self.gui.schedule_tick(self.speed,self.game_tick)


def run():
    gui = GUI()
    board = Board()
    snake = Snake()
    food = Food()

    game = Game(gui,board,snake,food)

    gui.bind_key("<Up>", game.move_up)
    gui.bind_key("<Right>", game.move_right)
    gui.bind_key("<Left>", game.move_left)
    gui.bind_key("<Down>", game.move_down)

    gui.bind_key("<r>",game.restart)

    gui.create_grid()
    gui._draw_snake(snake.body)

    food.generate_position(snake.body)
    gui._draw_food(food.position)

    game.game_tick()

    gui.window.mainloop()


if __name__ == '__main__':
    run()





