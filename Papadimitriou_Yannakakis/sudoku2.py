import heapq
import copy
import numpy as np

grid1 = [
    [0, 0, 0, 0, 8, 9, 5, 0, 0],
    [0, 0, 1, 2, 0, 0, 0, 0, 4],
    [7, 0, 0, 0, 0, 0, 2, 3, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 5, 1, 0, 7, 6, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 5],
    [0, 7, 8, 0, 0, 0, 0, 0, 6],
    [5, 0, 0, 0, 0, 3, 4, 0, 0],
    [0, 0, 9, 6, 4, 0, 0, 0, 0],
]

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

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


def possible(y,x,n,grid):
    for i in range(0,9):
        if(grid[y][i] == n or grid[i][x] == n):
            return False
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j] == n:
                return False
    return True

def findMIS(grid):
    MIS = []
    copy_grid = copy.deepcopy(grid)

    #busca el primer casillero donde haya una pista 
    for i in range(len(grid)):
        for j in range(len(grid)):
            if(grid[i][j]!=0):
                quadrant = (i // 3) * 3 + (j // 3)
                MIS.append([i,j,quadrant,grid[i][j]])
                break
        break
    
    #forma el MIS a partir de la pista anterior
    for i in range(len(grid)):
        for j in range(len(grid)):
            if(copy_grid[i][j]==MIS[0][3] or (copy_grid[i][j] == 0 and possible(i,j,MIS[0][3],copy_grid))):
                if ([i,j,quadrant,MIS[0][3]] not in MIS):
                    quadrant = (i // 3) * 3 + (j // 3)
                    MIS.append([i,j,quadrant,MIS[0][3]])
                    copy_grid[i][j] = MIS[0][3]
    print_board(copy_grid)
    return MIS

def get_ady(grid, i):
    ADY = []
    for x in range(len(grid)):
        for y in range(len(grid)):
            quadrant = (x // 3) * 3 + (y // 3)
            if(i[0] == x or i[1] == y or i[2] == quadrant) and ([x,y,quadrant,grid[x][y]] not in ADY): #and grid[x][y] == 0: 
                ADY.append([x,y,quadrant,grid[x][y]])
    if i in ADY:
        ADY.remove(i)
    return ADY

def get_min_lex_vertex(i, j):
    # if vertex1 is in a previous row than vertex2
    if i[0] < j[0]:
        return True
    # if vertex2 is in a previous row than vertex1
    elif i[0] > j[0]:
        return False
    else:
        # if both vertex are in the same row, but vertex1 is in a previous column than vertex2
        if i[1] < j[1]:
            return True
        # if both vertex are in the same row, but vertex2 is in a previous column than vertex1
        elif i[1] > j[1]:
            return False
        else:
            # if they are both in the same row and column, they are the same vertex
            return True

def is_MIS(possible_MIS, grid, j):
    
    for elem in possible_MIS:
        if elem != j and (elem[0] == j[0] or elem[1] == j[1] or elem[2] == j[2]):
            return False


    for x in range(len(grid)):
        for y in range(len(grid)):
            if(x == j[0] and y == j[1]):
                break
            i = 0
            for elem in possible_MIS:
                quadrant = (x // 3) * 3 + (y // 3)
                if elem[0] == x or elem[1] == y or elem[2] == quadrant:
                    i = i + 1
            if i == 0:
                return False          
        if(x == j[0] and y == j[1]):
                break
    return True

def is_MIS2(original_board, possible_S, j):
    board = copy.deepcopy(original_board)
    for x in possible_S:
        ady = get_ady(board, x)
        for elem in ady:
            if elem in possible_S:
                return False
    j_row = j[0]
    j_column = j[1]
    for i in range(len(board)):
        for j in range(len(board)):
            if i == j_row and j == j_column:
                break
            elem = [i, j, (i // 3) * 3 + (j // 3), board[i][j]]
            paint_board(board, possible_S)
            is_possible = possible(i, j, possible_S[0][3], board)
            if is_possible and elem[3] == 0:
                return False
        if i == j_row and j == j_column:
            break
    return True

def paint_board(board, MIS):
    # traverse the MIS
    for x in MIS:
        x_row = x[0]
        x_column = x[1]
        x_value = x[3]
        # put the value
        board[x_row][x_column] = x_value
    return board

def findMIS_WithPossibleMIS(possible_MIS, grid):
    for x in range(len(grid)):
        for y in range(len(grid)):
            quadrant = (x // 3) * 3 + (y // 3)
            i = 0
            for elem in possible_MIS:
                if (elem[0] == x or elem[1] == y or elem[2] == quadrant):
                    i = i + 1
            if i == 0:
                possible_MIS.append([x,y,quadrant,0])
    return possible_MIS

def sortLex(C):
    n = len(C)
    
    for i in range(n - 1):
        # Encuentra el índice del mínimo elemento en el resto del conjunto
        indice_minimo = i
        for j in range(i + 1, n):
            if get_min_lex_vertex(C[j], C[indice_minimo]):
                indice_minimo = j

        # Intercambia el elemento mínimo con el elemento en la posición actual
        C[i], C[indice_minimo] = C[indice_minimo], C[i]
    return C

def sudoku(grid):
    #S_x = findMIS(grid)
    S_x = [[0,0,0,0],[1,3,1,0],[2,6,2,0],[3,1,3,0],[4,4,4,0],[5,7,5,0],[6,2,6,0],[7,5,7,0],[8,8,8,0]]
    Q = []
    heapq.heappush(Q, S_x)
    L = []
    
    while Q:
        S = heapq.heappop(Q)
        L.append(S)

        for i in S:
            # Agarramos todos los adyacentes a i mayores a i
            ady_i = get_ady(grid, i)      
            J = []
            for elem in ady_i:
                if get_min_lex_vertex(i, elem):
                    J.append(elem)
            
            #para cada j S_j es S interseccion {1,...,j}
            for j in J:
                S_j = []
                for i in S:
                    if(get_min_lex_vertex(i,j)):
                        S_j.append(i)
                
                copy_grid = copy.deepcopy(grid)

                R_j = get_ady(grid, j)
                possibleMIS = [x for x in S_j if x not in R_j]
                
                possibleMIS.append(j)
                
                #if possibleMIS is a MIS of the first j vertices
                if(is_MIS(possibleMIS,grid, j)):
                    #find the lexicographically first MIS of G whit contains possibleMIS
                    T = findMIS_WithPossibleMIS(possibleMIS, copy_grid)
                    #T = sortLex(T)
                    if T not in Q and T not in L:
                        print(T)
                        print("separa")
                        heapq.heappush(Q, T)
    return L
                    
                
#print(get_ady(grid, [0,4,1,8]))
#print_board(grid)
print(sudoku(grid))

