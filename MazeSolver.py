class Solver(object):
    def __init__(self, location):
        self._location = location


    @classmethod
    def initialization(cls, entrance): #start at entrance
        return cls(entrance)
    
    def check_direction(self): #check for up, left, down and right
        row, column = self._location[0], self._location[1]

        return {
            (row - 1, column): gameboard[row - 1][column],
            (row, column - 1): gameboard[row][column - 1],
            (row + 1, column): gameboard[row + 1][column],
            (row, column + 1): gameboard[row][column + 1]
            }
    
    @staticmethod
    def intersection(neighbour): #reduce path for intersection
        return -3/4 if list(neighbour).count(0) > 1 else 0
    
    @staticmethod
    def backward(neightbour): #increase path if no way
        return 1 if list(neightbour).count(10) == 3 else 0 #indicated by 3 walls surrounded
    
    def final_state(self):
        row, col = self._location[0], self._location[1]
        if self._location == entrance:
            return 'No solution'
        return row == 0 or row == len(gameboard[0])- 1 or col == 0 or col == len(gameboard) - 1 #check edge of 2d map

    def move(self):
        neighbour = self.check_direction()
        adjustment = self.intersection(neighbour.values()) + self.backward(neighbour.values())

        for key, value in neighbour.items():
            if value == min(neighbour.values()): #move towards least traveled path
                gameboard[self._location[0]][self._location[1]] += 1 + adjustment
                self._location = list(key)

                return self.final_state() if self.final_state() else self.move()
        







gameboard =[ #simulation
[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
[0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 10],
[10, 10, 10, 10, 10, 0, 10, 0, 10, 10, 10, 0, 10, 10, 10, 0, 10, 10, 10],
[10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 10, 0, 10, 0, 10, 0, 0, 0, 10],
[10, 0, 10, 10, 10, 10, 10, 0, 10, 0, 10, 0, 10, 0, 10, 10, 10, 0, 10],
[10, 0, 10, 0, 0, 0, 10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 0, 0, 10],
[10, 0, 10, 0, 10, 0, 10, 10, 10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 10],
[10, 0, 10, 0, 10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 10, 0, 10, 0, 10],
[10, 0, 10, 0, 10, 10, 10, 0, 10, 0, 10, 10, 10, 10, 10, 0, 10, 0, 10],
[10, 0, 10, 0, 10, 0, 0, 0, 10, 0, 10, 0, 0, 0, 0, 0, 10, 0, 10],
[10, 0, 10, 0, 10, 0, 10, 10, 10, 10, 10, 0, 10, 10, 10, 10, 10, 0, 10],
[10, 0, 10, 0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 10, 0, 0, 0, 10],
[10, 0, 10, 0, 10, 10, 10, 10, 10, 0, 10, 0, 10, 0, 10, 10, 10, 10, 10],
[10, 0, 0, 0, 10, 0, 0, 0, 10, 0, 10, 0, 10, 0, 0, 0, 0, 0, 10],
[10, 10, 10, 10, 10, 10, 10, 0, 10, 0, 10, 0, 10, 10, 10, 10, 10, 0, 10],
[10, 0, 10, 0, 0, 0, 0, 0, 10, 0, 10, 0, 0, 0, 10, 0, 0, 0, 10],
[10, 0, 10, 0, 10, 0, 10, 10, 10, 0, 10, 10, 10, 10, 10, 0, 10, 0, 10],
[10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0],
[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
]
entrance = [1,0]

solver = Solver.initialization(entrance)


print(solver.move())

for row in range(19): #print final gameboard
    for column in range(19):
        output = gameboard[row][column] if gameboard[row][column] >= 2 else '☆'
        print(f'{output:<5}', end = '')
    print('\n')
