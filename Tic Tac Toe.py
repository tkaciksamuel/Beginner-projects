#Build a Tic Tac Toe game from scratch
#define some functions you will need beforehand
#Build game with singleplayer and multiplayer option
#generate with 3x3 board in mind primarily

from random import randint

P1 = 'x'
P2 = 'o'
BOT = 'o'

def start_new_game():
    global board
    board = gen_board(3)
    print("Welcome to my Tic Tac Toe game.\n"
          "Would you like to play singleplayer ? Press 's'!\n"
          "Would you like to play singleplayer ? Press 'm'!")
    choice = input()
    if choice == 's':
        spmain()
    if choice == 'm':
        mpmain()
    print("Would you like to play again ?\n"
          "'y' for yes\n"
          "'n' for no")
    new_game = input()
    if new_game == 'y':
        start_new_game()

def bot_move():
    while True:
        movebot = randint(0, 8)
        if is_valid(movebot):
            board[movebot] = BOT
            return board



def gen_board(size):
    row = [' '] * size
    board = row * size
    return board

board = gen_board(3)

def pretty_board():
    print("-------------")
    print("|" , board[0] ,"|",board[1] ,"|",board[2] ,"|",)
    print("|", board[3], "|", board[4], "|", board[5], "|", )
    print("|", board[6], "|", board[7], "|", board[8], "|", )
    print("-------------")

def player1_move():
    move = input("Which position do you wanna occupy ?")
    if move.isdigit():
        move = int(move) -1
    else:
        print("Please select number from 1 to 9")
    if is_valid(move):
        board[int(move)] = P1
    else:
        print("Please select unoccupied position")
    return board

def player2_move():
    move = input("Which position do you wanna occupy ?")
    if move.isdigit():
        move = int(move) - 1
    else:
        print("Please select number from 1 to 9")
    if is_valid(move):
        board[int(move)] = P2
    else:
        print("Please select unoccupied position")
    return board

def spmain():
    while tie_game() == False:
        player1_move()
        pretty_board()
        if is_winner() == True:
            print("P1 WON")
            break
        bot_move()
        pretty_board()
        if is_winner() == True:
            print("BOT WON")
            break

def mpmain():
    while tie_game() == False:
        player1_move()
        pretty_board()
        if is_winner() == True:
            print("P1 WON")
            break
        player2_move()
        pretty_board()
        if is_winner() == True:
            print("P2 WON")
            break


def is_valid(move)-> bool:
    if 0 <= move < len(board) and board[move] == ' ':
        return True
    return False

def is_winner()-> bool:
    #rows
    if board[0] == board[1] == board[2] == P1 or board[0] == board[1] == board[2] == P2:
        return True
    elif board[3] == board[4] == board[5] == P1 or board[3] == board[4] == board[5] == P2:
        return True
    elif board[6] == board[7] == board[8] == P1 or board[6] == board[7] == board[8] == P2:
        return True
    #columns
    if board[0] == board[3] == board[6] == P1 or board[0] == board[3] == board[6] == P2:
        return True
    elif board[1] == board[4] == board[7] == P1 or board[1] == board[4] == board[7] == P2:
        return True
    elif board[2] == board[5] == board[8] == P1 or board[2] == board[5] == board[8] == P2:
        return True
    #diagonals
    if board[0] == board[4] == board[8] == P1 or board[0] == board[4] == board[8] == P2:
        return True
    if board[6] == board[4] == board[2] == P1 or board[6] == board[4] == board[2] == P2:
        return True
    return False

def tie_game():
    if ' ' not in board:
        print("Tie game!")
        return True
    return False

if __name__ == "__main__":
    start_new_game()
