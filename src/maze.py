from cell import Cell
import time
import random

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        self.__left = x1
        self.__top = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_width = cell_size_x
        self.__cell_height = cell_size_y
        self.__win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        if seed:
            random.seed(seed)
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self.__num_cols):
            self._cells.append([])
            for j in range(self.__num_rows):
                x1 = self.__left + i * self.__cell_width
                y1 = self.__top + j * self.__cell_height
                x2 = x1 + self.__cell_width
                y2 = y1 + self.__cell_height
                new_cell = Cell(x1, y1, x2, y2, self.__win)
                self._cells[i].append(new_cell)
                self._draw_cell(i, j)
    
    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()
    
    def _animate(self):
        if self.__win:
            self.__win.redraw()
        time.sleep(0.005)

    def _break_entrance_and_exit(self):
        self._cells[0][0].walls["top"] = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].walls["bottom"] = False
        self._draw_cell(-1, -1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            if i > 0 and self._cells[i-1][j].visited == False:
                to_visit.append((i-1,j))
            if i < self.__num_cols - 1 and self._cells[i+1][j].visited == False:
                to_visit.append((i+1,j))
            if j > 0 and self._cells[i][j-1].visited == False:
                to_visit.append((i,j-1))
            if j < self.__num_rows - 1 and self._cells[i][j+1].visited == False:
                to_visit.append((i, j+1))
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            dir = random.randrange(len(to_visit))
            m, n = to_visit[dir]
            if m < i:
                self._cells[i][j].walls["left"] = False
                self._cells[m][n].walls["right"] = False
            elif m > i:
                self._cells[i][j].walls["right"] = False
                self._cells[m][n].walls["left"] = False
            elif n < j:
                self._cells[i][j].walls["top"] = False
                self._cells[m][n].walls["bottom"] = False
            elif n > j:
                self._cells[i][j].walls["bottom"] = False
                self._cells[m][n].walls["top"] = False
            self._draw_cell(i, j)
            self._break_walls_r(m, n)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True
        if i > 0 and self._cells[i-1][j].visited == False and self._cells[i][j].walls["left"] == False:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        if i < self.__num_cols - 1 and self._cells[i+1][j].visited == False and self._cells[i][j].walls["right"] == False:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)
        if j > 0 and self._cells[i][j-1].visited == False and self._cells[i][j].walls["top"] == False:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
        if j < self.__num_rows - 1 and self._cells[i][j+1].visited == False and self._cells[i][j].walls["bottom"] == False:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        return False
