import time, argparse, random, os

parser = argparse.ArgumentParser()
parser.add_argument("--size", "-s", type=int, default=10, help="Size of the board")
parser.add_argument("--prob", "-p", type=float, default=0.2, help="Probability of a cell being alive")
parser.add_argument("--steps", "-n", type=int, default=20, help="Number of steps to run the simulation for")

args = parser.parse_args()
s = args.size   # this will contain the size of the board
p = args.prob   # this will contain the probability of a cell being alive
n = args.steps  # this will contain the number of steps to run the simulation for
print(s, p, n)

def get_empty_board(i): # return i x i table of dead cells (a list of lists)
    zeros = []
    for j in range(i):
        zeros.append(i*[0])
    return zeros

def print_board(grid): # print the table
    słownik = {0:'.', 1:'X'}
    for rząd in grid:
        l = ''
        for i in rząd:
            l += słownik[i] + ' '
        print(l[:-1])

def get_random_board(i, pr=0.2): # return i x i table where each cell is alive with probability 0.2
    random_board = get_empty_board(i)
    for row in range(i):
        for el in range(i):
            x = random.random()
            if x < pr:
                random_board[row][el] = 1
    return random_board

def add_glider(board): # return a board with a glider
    board[0][2] = 1
    board[1][0] = 1
    board[1][2] = 1
    board[2][1] = 1
    board[2][2] = 1
    return board

def count_live_neighbors(board, x, y): # return the number of live neighbors of cell x, y
    suma = 0
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            if i < 0 or j < 0 or i > len(board)-1 or j > len(board)-1:
                suma += 0
            else:
                suma += board[i][j]
    if board[x][y] == 1:
        suma -= 1
    return suma

def step(board): # return board at the next timestep
    new_board = get_empty_board(len(board))
    for i in range(len(board)):
        for j in range(len(board)):
            neigh = count_live_neighbors(board, i, j)
            if board[i][j] == 1:
                if neigh in {2, 3}:
                    new_board[i][j] = 1
            else:
                if neigh == 3:
                    new_board[i][j] = 1
    return new_board

board = get_random_board(s, pr=p)

t1 = time.perf_counter()

for _ in range(n):    # run for n steps
    os.system('cls')    # clear the output
    print_board(board)          # print the board
    time.sleep(0.5)               # wait for half a second
    new_board = step(board)     # generate the next step
    board = new_board           # update the board

t2 = time.perf_counter()
print(f'\nTime of simulation: {t2 - t1} seconds.\n')