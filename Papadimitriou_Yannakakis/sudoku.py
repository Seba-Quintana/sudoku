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

def paint_board(board, MIS):
    # traverse the MIS
    for x in MIS:
        x_row = x[0]
        x_column = x[1]
        x_value = x[3]
        # put the value
        board[x_row][x_column] = x_value
    return board

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

# return true if vertex1 is less than vertex2 in lexical order
def get_min_lex_vertex(vertex1, vertex2):
    # if vertex1 is in a previous row than vertex2
    if vertex1[0] < vertex2[0]:
        return True
    # if vertex2 is in a previous row than vertex1
    elif vertex1[0] > vertex2[0]:
        return False
    else:
        # if both vertex are in the same row, but vertex1 is in a previous column than vertex2
        if vertex1[1] < vertex2[1]:
            return True
        # if both vertex are in the same row, but vertex2 is in a previous column than vertex1
        elif vertex1[1] > vertex2[1]:
            return False
        else:
            # if they are both in the same row and column, they are the same vertex
            return True

# return all adyacents of a vertex without changing the board
def get_ady(board, x):
    ady = []
    row = copy.deepcopy(board[x[0]])
    # get the position and quadrant of each element in the row
    for i in range(len(row)):
        row[i] = [x[0], i, (x[0] // 3) * 3 + (i // 3), row[i]]
        if row[i] not in ady and row[i] != x:
            ady.append(row[i])
    column = []
    for i in range(len(board)):
        column.append(copy.deepcopy(board[i][x[1]]))
    # get the position and quadrant of each element in the column
    for i in range(len(column)):
        column[i] = [i, x[1], (i // 3) * 3 + (x[1] // 3), column[i]]
        if column[i] not in ady and column[i] != x:
            ady.append(column[i])
    quadrant = []
    quadrant_cells = get_quadrant_cells(copy.deepcopy(board), x)
    for cell in quadrant_cells:
        quadrant.append(cell)
        if cell not in ady and cell != x:
            ady.append(cell)
    return ady

def is_MIS(board, S):
    for x in S:
        ady = get_ady(board, x)
        for elem in ady:
            if elem in S:
                return False
    return True

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
        # in Papadimitriou's paper, x is vertex i
        # this for is to find all the neighbours of S's vertex
        for x in S:
            ady = get_ady(board, x)
            # add all elements in the row, column and quadrant to J
            J = []
            for elem in ady:
                if get_min_lex_vertex(x, elem) and elem not in S:
                    J.append(elem)
            
            for j in J:
                Sj = []
                for elem in S:
                    if get_min_lex_vertex(elem, j):
                        Sj.append(elem)
                j_ady = get_ady(board, j)
                possible_MIS = []
                possible_MIS.append(j)
                for elem in j_ady:
                    if elem not in Sj:
                        possible_MIS.append(elem)
                if is_MIS(board, possible_MIS):
                    heapq.heappush(Q, possible_MIS)



        # # for each vertex j adjacent to a vertex in S
        # for j in ady:
        #     Sj = []
        #     i_j = []
        #     # grab all rows before j[0]
        #     actual_row = 0
        #     while actual_row < j[0]:
        #         row = copy.deepcopy(board[actual_row])
        #         actual_column = 0
        #         for elem in row:
        #             i_j.append([actual_row, actual_column, (actual_row // 3) * 3 + (actual_column // 3), elem])
        #             actual_column = actual_column + 1
        #         actual_row += 1
        #     # grab all elements in the same row as j until j[1]
        #     actual_column = 0
        #     while actual_column <= j[1]:
        #         row = copy.deepcopy(board[j[0]])
        #         for elem in row:
        #             i_j.append([j[0], actual_column, j[2], elem])
        #         actual_column += 1
        #     # grab elements that are in S and {1,..,j} at the same time in Sj
        #     for elem in i_j:
        #         if elem in S:
        #             Sj.append(elem)
        #     # if (Sj - neighbours of j) U {j}
        #     res = []
        #     res.append(j)
        #     for elem in Sj:
        #         a=0
        #


    return L

def test():
    MIS = findMIS(board2)
    print(MIS)
    paint_board(board2, MIS)
    print_board(board2)
    print(is_MIS(board2, MIS))

# test()

a = sudoku(board1)
print(a)




