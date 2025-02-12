from line import Line
from point import Point
from window import Window

class Cell():
    def __init__(self, x1, y1, x2, y2, window = None):
        self.__window = window
        p1 = Point(x1, y1)
        p2 = Point(x1, y2)
        p3 = Point(x2, y1)
        p4 = Point(x2, y2)
        self.centre = Point((x1+x2)/2, (y1+y2)/2)
        left = Line(p1, p2)
        right = Line(p3, p4)
        top = Line(p1, p3)
        bottom = Line(p2, p4)
        self.walls = {
            "left": True,
            "right": True,
            "top": True,
            "bottom": True,
        }
        self.__lines = {
            "left": left,
            "right": right,
            "top": top,
            "bottom": bottom,
        }
        self.visited = False
    
    def draw(self):
        if self.__window:
            for wall in self.__lines:
                if self.walls[wall]:
                    self.__window.draw_line(self.__lines[wall], "black")
                else:
                    self.__window.draw_line(self.__lines[wall], "#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        move = Line(self.centre, to_cell.centre)
        color = "red"
        if undo:
            color = "gray"
        if self.__window:
            self.__window.draw_line(move, color)
