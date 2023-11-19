# sudoku solver with papadimitriou and yannakakis algorithm

# import libraries
import heapq
import copy

# sudoku board
board = [
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
    # once found an initial value, find all quadrants that contain the value
    initial_value_quadrants = []
    # this is to avoid changing the initial value
    found_one = False

    for i in range(len(board)):
        for j in range(len(board)):
            quadrant = (i // 3) * 3 + (j // 3)
            # found a value
            if board[i][j] != 0 and not found_one:
                found_one = True
                # find initial's value quadrant
                initial_value = [i, j, quadrant, board[i][j]]
                # if quadrant not in initial_value_quadrants:
                quadrants[i].append(initial_value[3])
                #
                MIS.append(initial_value)
                continue
            # every time we find the value again, we update the quadrant list
            if found_one:
                if board[i][j] == initial_value[3]:
                    MIS.append([i, j, quadrant, initial_value[3]])
                    # find initial's value quadrant
                    # if quadrant not in initial_value_quadrants:
                    quadrants[i].append(initial_value[3])
                    #
                if board[i][j] == 0:
                    is_in_quadrant = False
                    is_in_row = False
                    is_in_column = False

                    # check if the position's quadrant contains the value
                    quadrant = (i // 3) * 3 + (j // 3)
                    if initial_value[3] in quadrants[quadrant]:
                        is_in_quadrant = True
                    
                    # check if the position's row contains the value
                    if initial_value[3] in board[i]:
                        is_in_row = True

                    # check if the position's column contains the value
                    for k in range(len(board)):
                        if initial_value[3] == board[k][j]:
                            is_in_column = True

                    if is_in_quadrant or is_in_row or is_in_column:
                        continue
                    
                    # if the value is neither in the quadrant nor in the row nor in the column
                    # add it to the MIS
                    MIS.append([i, j, quadrant, initial_value[3]])
                    board[i][j] = initial_value[3]
                    # update quadrant
                    quadrants[quadrant].append(initial_value[3])
        continue
    print_board(board)
    return MIS

# function to print the board
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

def sudoku(board):
    # find the first maximal independent set
    S_star = findMIS(board)
    # create a heap 
    Q = []
    heapq.heappush(Q, S_star)
    L = []
    # while the heap is not empty
    while Q:
        # extract the first element of the heap
        S = heapq.heappop(Q)
        # add the element to the list 
        L.append(S)
        # foreach j in V(G) adyacent to a vertex i in S with i < j 
        # for this you can check the position for every vertex in S, and search in the board for the adjacent vertex (vertex with same i, j, or in the same quadrant)

        # for i in range(len(board)):
            # for j in range(len(board)):
    return L

# new_board = findMIS(board2)
a = sudoku(board)
# print_board(new_board)








        # foreach j in V(G) adyacent to a vertex i in S with i < j
    #     for i in range(len(board)):
    #         for j in range(i+1, len(board)):
    #             # Check if j is adjacent to i in S
    #             if board[i][j] == 0 and i in S and j in S:
    #                 # Compute S_j = S intersection {i, ..., j}
    #                 S_j = set(range(i, j+1)) & S
    #
    #                 # Compute the set difference S_j - neighbors(j) union {j}
    #                 neighbors_j = {k for k in range(len(board)) if board[j][k] == 0 and k != j}
    #                 potential_set = (S_j - neighbors_j) | {j}
    #
    #                 # Check if potential_set is a maximal independent set in {i, ..., j}
    #                 if all(board[x][y] == 0 or (x not in potential_set and y not in potential_set) for x in range(i, j+1) for y in range(i, j+1) if x != y):
    #                     # Find the lex-first maximal independent set containing potential_set
    #                     T = findMIS(board)
    #                     # Insert T into the heap Q
    #                     Q.insert(T)
    #
    # # Return the list L of maximal independent sets
