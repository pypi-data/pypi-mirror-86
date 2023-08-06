from krestiki_noliki.board import Board

board = Board()


def win(figure):
    win_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

    for comb in win_list:
        if figure in board.getPosition(comb[0]):
            if figure in board.getPosition(comb[1]):
                if figure in board.getPosition(comb[2]):
                    return True
    return False


def start():
    count = 0
    check = True
    print("Player X name = ", end="")
    x_name = input()
    print("Player O name = ", end="")
    o_name = input()
    print(str(board))

    while check:
        set_status = False

        while not set_status:
            print("X position? ", end="")
            try:
                position = int(input())

                if position in range(1, 10):
                    set_status = board.setFigure(position, "X")

                    if not set_status:
                        print("\033[31mThis position is taken\033[0m")
                else:
                    print("Position not in 1..9")
            except ValueError:
                print("Position not in 1..9")

        if win("X"):
            print("{} WIN!".format(x_name))
            break
        else:
            count += 1
            print(str(board))

        set_status = False

        while not set_status:
            print("O position? ", end="")
            try:
                position = int(input())

                if position in range(1, 10):
                    set_status = board.setFigure(position, "O")

                    if not set_status:
                        print("\033[31mThis position is taken\033[0m")
                else:
                    print("Position not in 1..9")
            except ValueError:
                print("Position not in 1..9")

        if win("O"):
            print("{} WIN!".format(o_name))
            break
        else:
            count += 1
            print(str(board))

        if count == 9:
            print("DRAW")
            break


def main():
    start()

    print("Play again (y/n")
    if input() == "y":
        start()
