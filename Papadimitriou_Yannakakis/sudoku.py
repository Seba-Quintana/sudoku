# sudoku solver with Papadimitriou and Yannakakis algorithm

# import libraries
import heapq
import copy

# sudoku example board
board1 = [
    [0, 4, 0, 0, 0, 0, 0, 8, 0],
    [0, 0, 7, 0, 0, 0, 0, 6, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [4, 1, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 7, 0, 0, 3],
    [0, 0, 5, 8, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
]

# test board
board2 = [
    [5, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# function to find the first maximal independent set in the board in lexical order
def findMIS(original_board):
    # this board is created only for testing purposes
    board = copy.deepcopy(original_board)

    MIS = []
    # create a list of quadrants
    # each list contains the values found in the quadrant
    quadrants = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]

    # search an initial value in the board 
    # values: i, j, quadrant, actualValue
    initial_value = [0, 0, 0, 0]
    # this is to avoid changing the initial value
    found_one = False

    for i in range(len(board)):
        for j in range(len(board)):
            quadrant = (i // 3) * 3 + (j // 3)
            # found a value for the first time
            if board[i][j] != 0 and not found_one:
                found_one = True
                initial_value = [i, j, quadrant, board[i][j]]
                quadrants[i].append(initial_value[3])
                MIS.append(initial_value)
                continue
            if found_one:
                if board[i][j] == initial_value[3]:
                    MIS.append([i, j, quadrant, initial_value[3]])
                    quadrants[i].append(initial_value[3])
                if board[i][j] == 0:
                    is_in_quadrant = False
                    is_in_row = False
                    is_in_column = False

                    # check if the actual position's quadrant contains the value
                    quadrant = (i // 3) * 3 + (j // 3)
                    if initial_value[3] in quadrants[quadrant]:
                        is_in_quadrant = True
                    
                    # check if the actual position's row contains the value
                    if initial_value[3] in board[i]:
                        is_in_row = True

                    # check if the actual position's column contains the value
                    for k in range(len(board)):
                        if initial_value[3] == board[k][j]:
                            is_in_column = True

                    if is_in_quadrant or is_in_row or is_in_column:
                        continue
                    
                    # if the value is neither in the quadrant nor in the row nor in the column
                    # add it to the MIS
                    MIS.append([i, j, quadrant, initial_value[3]])
                    # board is for testing purposes
                    board[i][j] = initial_value[3]
                    # update quadrant
                    quadrants[quadrant].append(initial_value[3])
        continue
    # print_board(board)
    return MIS

def print_board(board):
    # traverse the print_board
    for i in range(len(board)):
        # print a line every 3 rows
        if i % 3 == 0 and i != 0:
            print("-----------------------")
        # traverse the columns
        for j in range(len(board)):
            # print a line every 3 columns
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            # print the value of the board
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")
    print("\n")

def get_quadrant_cells(board, x):
    # Get the starting row and column of the quadrant
    start_row = (x[0] // 3) * 3
    start_col = (x[1] // 3) * 3

    # Traverse the cells in the same quadrant
    quadrant_cells = []
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            cell = [i, j, x[2], board[i][j]]
            quadrant_cells.append(cell)

    return quadrant_cells

def sudoku(board):
    # find the first maximal independent set
    S_star = findMIS(board)
    # create a heap 
    Q = []
    heapq.heappush(Q, S_star)
    L = []
    print_board(board)
    # while the heap is not empty
    while Q:
        # extract the first element of the heap
        S = heapq.heappop(Q)
        # add the element to the list 
        L.append(S)
        # foreach j in V(G) adyacent to a vertex i in S with i < j 
        # for this you can check the position for every vertex in S, and search in the board for the adjacent vertex (vertex with same i, j, or in the same quadrant)

        # k's idea is to store all vertex in S
        k = copy.deepcopy(S)
        for x in S:
            row = board[x[0]]
            column = []
            for i in range(len(board)):
                column.append(board[i][x[1]])
            quadrant = []
            quadrant_cells = get_quadrant_cells(board, x)
            for cell in quadrant_cells:
                quadrant.append(cell)

            # search for the adjacent vertex
            Sj = []
            # j has all adjacent vertex to x
            j = []
            actual_row = 0
            # grab all rows before x[0]
            while actual_row < x[0]:
                actual_column = 0
                for elem in board[actual_row]:
                    j.append([actual_row, actual_column, (actual_row // 3) * 3 + (actual_column // 3), elem])
                    actual_column = actual_column + 1
                actual_row += 1
            # grab all elements in the same row as x until x[1]
            actual_column = 0
            while actual_column <= x[1]:
                for elem in row:
                    j.append([x[0], actual_column, x[2], elem])
                actual_column += 1
            # grab elements that are in S and j at the same time in Sj
            # if (Sj - neighbours of j) U {j}
    return L

# new_board = findMIS(board2)
a = sudoku(board1)
# print_board(new_board)

