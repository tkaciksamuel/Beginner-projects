#classes: Ship, Board , Player, Game
#start with board class ,work from there
#class Game as last
#2D array setup, 10x10 board
#single and multiplayer option
#clean ,expandable design(pygame or tkinter incorporation in mind)

#TODO
#1 = finish manual ship placement
#2 = finish random ship placement
#3 = update main game loop(start method)
#4 = make ships hidden for players
#5 = print board after every move or before
#6 = finish the damn game

import random

class Board:
    SIZE = 10

    def __init__(self):
        self.grid = [
            ['~' for _ in range(Board.SIZE)]
             for _ in range(Board.SIZE)
        ]

        self.ships = []

    def print_board(self,hide_ships = False):
        print('   ' + ' '.join(str(i) for i in range(Board.SIZE)))
        print('-'*(Board.SIZE*2 + 2))

        for i,row in enumerate(self.grid):
            display_row = []

            for cell in row:
                if hide_ships and cell == 'S':
                    display_row.append('~')
                else:
                    display_row.append(cell)


            print(str(i) + ' |' + ' '.join(display_row))

    def place_ship_h(self,row,col,size):
        if col + size > Board.SIZE:
            print("Out of bounds!")
            return False

        for i in range(size):
            if self.grid[row][col + i] == 'S':
                print("Coordinate already occupied!")
                return False

        for i in range(size):
            self.grid[row][col + i] = 'S'

        ship = Ship(size)

        for i in range(size):
            ship.coordinates.append((row, col + i))

        self.ships.append(ship)

        return True

    def place_ship_v(self,row,col,size):
        if row + size > Board.SIZE:
            print("Out of bounds!")
            return False

        for i in range(size):
            if self.grid[row + i][col] == 'S':
                print("Coordinate already occupied!")
                return False

        for i in range(size):
            self.grid[row + i][col] = 'S'

        ship = Ship(size)

        for i in range(size):
            ship.coordinates.append((row + i,col))

        self.ships.append(ship)


        return True


    def attack_ship(self,row,col):
        if row < 0 or row >= Board.SIZE or col < 0 or col >= Board.SIZE:
            return 'out_of_bounds'

        if self.grid[row][col] == 'S':
            self.grid[row][col] = 'X'

            ship = self.get_ship_at(row,col)
            ship.hits += 1

            if ship.is_sunk():
                return 'sunk'

            return 'hit'



        elif self.grid[row][col] == '~':
            self.grid[row][col] = 'O'
            return 'miss'

        else:
            return 'already_attacked'

    def all_ships_sunk(self):
        for row in self.grid:
            if 'S' in row:
                return False

        return True

    def get_ship_at(self,row,col):
        for ship in self.ships:
            if (row,col) in ship.coordinates:
                return ship

        return None


class Player:
    def __init__(self,name):
        self.name = name
        self.board = Board()



class Game:
    def __init__(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

        self.current_p = self.player1

    def get_enemy(self):
        if self.current_p == self.player1:
            return self.player2
        else:
            return self.player1

    def player_turn(self):
        enemy = self.get_enemy()

        print(f"{self.current_p.name}'s board:")
        self.current_p.board.print_board()
        print()

        print(f"{enemy.name}'s board:")
        enemy.board.print_board(hide_ships=True)
        print()

        print(f"{self.current_p.name}'s turn")
        print()

        try:
            row = int(input("Row:"))
            col = int(input("Col:"))
        except ValueError:
            print("Please enter numbers!")
            return False

        result = enemy.board.attack_ship(row,col)

        if result == 'hit':
            print("Ship Hit!")
            return True
        elif result == 'sunk':
            print("Ship sunk!")
            return True
        elif result == 'miss':
            print("Miss!")
            return True
        elif result == 'already_attacked':
            print("You have already attacked at this coordinate!")
            return False
        else:
            print("Out of bounds!")
            return False



    def switch_player(self):
        if self.current_p == self.player1:
            self.current_p = self.player2
        else:
            self.current_p = self.player1

    def setup_ships(self):
        ship_sizes = [5,4,3,3,2]

        for player in[self.player1, self.player2]:
            print(f"{player.name} please choose:\n"
                  f"1 - place ships manually\n"
                  f"2 - place ships automatically")
            print()

            while True:
                choice = input("Choose(1/2):")

                if choice == '1':
                    Game.manual_place(player,ship_sizes)
                    break
                elif choice == '2':
                    Game.auto_place(player,ship_sizes)
                    break
                else:
                    print("Please enter a valid choice.")



    @staticmethod
    def manual_place(player,ship_sizes):
        print(f"{player.name} choose direction to build your ship(H/V)\n"
              f"H = horizontal\n"
              f"V = vertical")
        print()

        for size in ship_sizes:
            placed = False

            while not placed:
                player.board.print_board()

                print(f"You are placing the ship of size {size}.")

                choice = input("Your direction: ").upper()

                if choice != 'H' and choice != 'V':
                    print("Invalid direction! Choose H or V.")
                    continue

                try:
                    row = int(input("Enter row: "))
                    col = int(input("Enter column: "))
                except ValueError:
                    print("Please input a number.")
                    continue

                if choice == 'H':
                    placed = player.board.place_ship_h(row,col,size)
                elif choice == 'V':
                    placed = player.board.place_ship_v(row,col,size)

        print(f"{player.name}'s final board looks like :")
        player.board.print_board()






    @staticmethod
    def auto_place(player,ship_sizes):
        for size in ship_sizes:
            placed = False

            while not placed:
                row = random.randint(0,Board.SIZE -1)
                col = random.randint(0,Board.SIZE -1)
                direction = random.choice(['H','V'])

                if direction == 'H':
                    placed = player.board.place_ship_h(row,col,size)
                else:
                    placed = player.board.place_ship_v(row,col,size)

        print(f"{player.name}'s final board looks like :")
        player.board.print_board()


    def start(self):

        while True:

            enemy = self.get_enemy()

            turn_happened = self.player_turn()

            if not turn_happened:
                continue

            if enemy.board.all_ships_sunk():
                print(f"{self.current_p.name} WINS!")
                break

            self.switch_player()


class Ship:
    def __init__(self,size):
        self.size = size
        self.coordinates = []
        self.hits = 0

    def is_sunk(self):
        if self.size == self.hits:
            return True

        return False

if __name__ == '__main__':
    game = Game()
    game.setup_ships()
    game.start()






