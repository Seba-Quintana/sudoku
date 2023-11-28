import time

class backtraking:

    def __init__(self, sudoku):
        self.tamano = len(sudoku)
        self.sudoku = sudoku

    def is_valid(self, row, col, num): #Verifica si es valido el cambio
        for i in range(self.tamano):
            if self.sudoku[row][i] == num or self.sudoku[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.sudoku[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True  # Tablero resuelto

        row, col = empty

        for num in range(1, self.tamano + 1): 
            if self.is_valid(row, col, num):
                self.sudoku[row][col] = num
                if self.solve(): 
                    return True
                self.sudoku[row][col] = 0  # Deshacer la asignación si no lleva a una solución plausible

        return False

    def find_empty(self):
        for i in range(self.tamano):
            for j in range(self.tamano):
                if self.sudoku[i][j] == 0:
                    return (i, j)  
        return None

    def print_solution(self):
        for row in self.sudoku:
            print(row)

sudoku_board = [
    [0, 0, 5, 0, 0, 8, 3, 9, 0],
    [0, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 7, 0, 0, 0, 8, 0],
    [0, 0, 4, 5, 0, 0, 6, 0, 2],
    [6, 1, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 4, 0, 5],
    [0, 0, 9, 0, 8, 0, 0, 0, 0],
    [5, 6, 0, 0, 0, 0, 0, 0, 0],
]

sudoku_solver = backtraking(sudoku_board)
time1 = time.time()

if sudoku_solver.solve():
    print("Solución encontrada:")
    sudoku_solver.print_solution()
else:
    print("No hay solución.")
print(time.time() - time1)