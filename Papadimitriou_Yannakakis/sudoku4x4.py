import heapq
import copy
import numpy as np


grid4 = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
]


def getQuadrant(x,y):
    if 0 <= x <= 1 and 0 <= y <= 1:
        return 0
    elif 0 <= x <= 1 and 2 <= y <= 3:
        return 1
    elif 2 <= x <= 3 and 0 <= y <= 1:
        return 2
    elif 2 <= x <= 3 and 2 <= y <= 3:
        return 3
    else:
        return "Fuera de rango"
    
def get_ady(grid, i):
    ADY = []
    for x in range(len(grid)):
        for y in range(len(grid)):
            quadrant = getQuadrant(x,y)
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
                quadrant = getQuadrant(x,y)
                if elem[0] == x or elem[1] == y or elem[2] == quadrant:
                    i = i + 1
            if i == 0:
                return False          
        if(x == j[0] and y == j[1]):
                break
    return True


def findMIS_WithPossibleMIS(possible_MIS, grid):
    for x in range(len(grid)):
        for y in range(len(grid)):
            quadrant = getQuadrant(x,y)
            i = 0
            for elem in possible_MIS:
                if (elem[0] == x or elem[1] == y or elem[2] == quadrant):
                    i = i + 1
            if i == 0:
                possible_MIS.append([x,y,quadrant,0])
    return possible_MIS


def sudoku(grid):
    S_x = [[0,0,0,0],[1,2,1,0],[2,1,2,0],[3,3,3,0]]
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

                R_j = get_ady(grid, j)
                
                # S_j / R_j U j
                possibleMIS = [x for x in S_j if x not in R_j]
                possibleMIS.append(j)
                
                #if possibleMIS is a MIS of the first j vertices
                if(is_MIS(possibleMIS,grid, j)):
                    #find the lexicographically first MIS of G whit contains possibleMIS
                    T = findMIS_WithPossibleMIS(possibleMIS, grid)
                    if T not in Q and T not in L:
                        print(T)
                        print("separa")
                        heapq.heappush(Q, T)
    return L
                    
                
sudoku(grid4)