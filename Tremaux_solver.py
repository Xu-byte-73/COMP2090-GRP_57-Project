from maze_solver import Solver

class Trémaux_solver(Solver): #creative solver using numbers
    @classmethod
    def start(cls):
        cls._gameboard = [[10 if cell == '■' else 0 for cell in row]
                           for row in Solver._gameboard] #copy gameboard as num
        solver = cls(cls.entrance)
        final_state = False

        while not final_state: #False to continue and True to stop
            final_state = solver.move()

        if final_state == 'No solution':
            print(final_state)
        else:
            distance = cls.show_path(cls._gameboard)
    
    @staticmethod
    def intersection(neighbour): #reduce path for intersection; for further passing
        return -3/4 if list(neighbour).count(0) > 1 else 0
    
    @staticmethod
    def backward(neightbour): #increase path if no way; stop passing
        return 1 if list(neightbour).count(10) == 3 else 0 #indicated by 3 walls surrounded
    
    def move(self):        
        neighbour = self.check_direction()
        adjustment = self.intersection(neighbour.values()) + self.backward(neighbour.values()) #adjust visit time for special cells
        row, column = self._location[0], self._location[1]

        if len(neighbour) < 4 and self._location != self.entrance: #reach exit
            self._gameboard[row][column] = 1
            if self.visualizer:
                self.visualizer.maze = self._gameboard
                self.visualizer.draw()
            return True #success

        for key, value in neighbour.items():
            if value == min(neighbour.values()): #move towards least traveled path
                self._gameboard[row][column] += 1 + adjustment #visit time +1
                self._location = key

                if self.visualizer:
                    self.visualizer.maze = self._gameboard
                    self.visualizer.draw()

                if self._location == self.entrance: #will return to entrance if no solution
                    return 'No solution'
                return
            
    @classmethod
    def show_path(cls, num_map):
        cls._gameboard = [['P' if cell > 0 and cell < 2 else cell for cell in row] for row in num_map] #correct path should be between 0 and 2 visit time
        return [cell for row in cls._gameboard for cell in row].count('P') #traserse the map
    
if __name__ == "__main__":
    Trémaux_solver.start()
    print(Trémaux_solver._gameboard)