from abc import ABC, abstractmethod

class Solver(ABC): #abstract class for solvers
    _gameboard = None #gameboard and entrance as class attributes
    entrance = None
    visualizer = None

    def __init__(self, location):
        self._location = location #(row, column)

    def check_direction(self): #check for surroundings
        row, column = self._location[0], self._location[1]
        directions = [(row - 1, column), (row, column - 1), (row + 1, column), (row, column + 1)] #check for up, left, down and right
        border = [-1, len(self._gameboard), len(self._gameboard[0])] #check border to avoid index out of range

        neighbour = {dir: self._gameboard[dir[0]][dir[1]] for dir in directions
                     if dir[0] not in border and dir[1] not in border} #return dict{(dir, loc)} for neighbours in maze range
        return neighbour

    @classmethod
    def initialization(cls, map, entrance, visualizer = None): #initialize the class attributes for other solvers' uses
        cls._gameboard = map
        cls.entrance = entrance
        cls.visualizer = visualizer

    @classmethod
    @abstractmethod #start game abstract method
    def start(cls):
        pass
    
    @abstractmethod #special for intersections
    def intersection(self, neighbour):
        pass

    @abstractmethod
    def move(self): #basic movement
        pass

    @classmethod
    @abstractmethod #display path after reach destination
    def show_path(cls, destination):
        pass