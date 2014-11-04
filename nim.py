from random import randint, random
from time import sleep
import itertools

num_nodes_expanded = 0
MIN_REMOVE = 1
MAX_REMOVE = 3
board_size = 1
column_size = 8


def computer(board):
    '''Determine computer move.'''
    score, rec_col, rec_mov = recommend_move(board, False)

    if score > 0:
        column, pieces = rec_col, rec_mov
    else:
        # no winning move was found, find a random one.
        column = randint(0, len(board) - 1)
        pieces = MAX_REMOVE + 1
        while pieces > MAX_REMOVE:
            pieces = randint(1, board[column])

    show_text("\nI take {0} stone{1} from column {2}.\n".format(pieces, ("s", "")[pieces == 1], column + 1))

    return column, pieces


def recommend_move(board, play_as_opponent):
    global num_nodes_expanded
    num_nodes_expanded += 1
    if play_as_opponent:
        best_score = 1, 0, 0
    else:
        best_score = 0, 0, 0

    if sum(board) > 0:
        # best_score = (0,0,0)
        # for each col, and number of pieces pair
        for col, pcs in list(itertools.product(range(0, board_size), range(MAX_REMOVE, MIN_REMOVE - 1, -1))):
            # valid col, pcs pair?
            if board[col] < pcs:
                continue

            # new mutable copy of board
            new_board = board[:]
            new_board[col] -= pcs
            # no need to explore further - a winning combo is found

            score = (recommend_move(new_board, not play_as_opponent)[0],col,pcs)
            if play_as_opponent:
                best_score = min([best_score,score], key= lambda item: item[0])
            else:
                best_score = max([best_score,score], key= lambda item: item[0])

    # no winning move or lost game: no pieces to pick.

    return best_score


def human(board):
    '''Get and validate input from the human player.'''

    while True:
        show_text("\nHow many pieces do you want to remove? ")
        pieces = int(raw_input().strip())

        show_text("From which column? ")
        column = int(raw_input().strip()) - 1

        # validate input
        if 0 <= column < len(board) and 1 <= pieces <= board[column] and MIN_REMOVE <= pieces <= MAX_REMOVE:
            break

        show_text("\nYour input is not valid. Please reenter.")

    return column, pieces


def show_board(board):
    '''Display the board of stones.'''

    columnformat = "{0:4}".format
    lineformat = "\n{0:6}: {1}".format

    cols = map(columnformat, range(1, len(board) + 1))
    show_text(lineformat("column", ''.join(cols)))

    cols = map(columnformat, board)
    show_text(lineformat("pieces", ''.join(cols)))

    show_text("\n")


def show_text(s):
    print s


def nim():
    '''Play nim.'''

    # initialize random board for each column
    board = [randint(0,column_size) for n in range(board_size)]

    show_board(board)

    player, comp_start = (human, False) if random() > 0.5 else (computer, True)

    while True:
        column, pieces = player(board)
        board[column] -= pieces

        if sum(board) == 0:
            break

        player = computer if player == human else human
        show_board(board)

    show_text("\nThere are no pieces remaining, ")
    show_text("I win!\n" if player == computer else "You win!\n")
    sleep(1)
    sleep(0.5)
    show_text("\n\nBye.")

    with open('results.csv', 'wa') as results:
        results.write('{0},{1},{2}'.format(num_nodes_expanded, column_size, comp_start))


if __name__ == '__main__':
    nim()