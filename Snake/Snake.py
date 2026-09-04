import tkinter as tk
import random
from PIL import Image,ImageTk

class GUI:
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 600

    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500

    PHONE_BACKGROUND = "#34495E"
    LCD_BACKGROUND = "#9BBC0F"
    LCD_DARK = "#0F380F"

    def __init__(self):
        self.window = tk.Tk()

        image = Image.open("assets/meat.png")
        image = image.resize((24, 24))
        self.food_image = ImageTk.PhotoImage(image)

        self.frame = tk.Frame(self.window,bg='gray')
        self.canvas = tk.Canvas(self.frame,width=self.SCREEN_WIDTH,height=self.SCREEN_HEIGHT,bg=self.LCD_BACKGROUND)

        self.create_window()
        self.frame.pack(expand=True)
        self.canvas.pack(padx=10,pady=10)

    def create_window(self):
        self.window.title('Snake')
        self.window.configure(background=self.PHONE_BACKGROUND)
        self.window.resizable(False,False)
        self.window.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')

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

        x = col * Board.CELL_SIZE + Board.CELL_SIZE//2
        y = row * Board.CELL_SIZE + Board.CELL_SIZE//2

        self.canvas.create_image(x,y,image=self.food_image,tags='food')

    def draw_game_over(self, score):
        self.canvas.create_rectangle(
            0,
            0,
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT,
            fill=self.LCD_DARK,
            tags="game_over"
        )

        x = self.SCREEN_WIDTH // 2

        self.canvas.create_text(
            x,
            170,
            text="GAME OVER",
            fill=self.LCD_BACKGROUND,
            font=("Lucida Console", 34, "bold"),
            tags="game_over"
        )

        self.canvas.create_text(
            x,
            250,
            text=f"SCORE  {score}",
            fill=self.LCD_BACKGROUND,
            font=("Lucida Console", 24, "bold"),
            tags="game_over"
        )

        self.canvas.create_text(
            x,
            340,
            text="Press R to restart",
            fill=self.LCD_BACKGROUND,
            font=("Lucida Console", 14),
            tags="game_over"
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
            self.increase_speed()
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

    def increase_speed(self):
        if self.score % 6 == 0:
            self.speed -= 50

        if self.speed <= self.MIN_SPEED:
            self.speed = self.MIN_SPEED

    def restart(self, event):
        if not self.game_over:
            return

        self.game_over = False
        self.score = 0
        self.speed = 300

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





