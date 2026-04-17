from maze_solver import Solver
import time

class DFS_solver(Solver):
    anchors = [] #record for backtracking

    def __init__(self, location, direction):
        super().__init__(location) #Inheritance location attribute
        self._direction = direction

    @classmethod
    def start(cls):
        cls.anchors = [] #clear the anchor stack
        cls._gameboard = [[cell for cell in row] for row in Solver._gameboard] #deep copy gameboard
        solver = cls(cls.entrance, None)
        final_state = False

        while not final_state: #True → end; False → continue
            final_state = solver.move()

        if final_state == 'No solution': #all paths attempted
            print(final_state)
        else:
            distance = cls.show_path(solver) #display final path and record distance
            if cls.visualizer:
                cls.visualizer.maze = cls._gameboard
                cls.visualizer.draw()
                time.sleep(1) #one second interval for display

    def intersection(self, neighbour):
        branch = [key for key, value in neighbour.items() if value == ' ']
        self.anchors.append(DFS_solver(self._location, branch))
        self._location = branch[0]

    def backward(self):
        if not self.anchors: #all intersections used up
            return 'No solution'
        
        branch = self.anchors[-1]._direction #change direction
        branch.pop(0)

        if not branch:
            self.anchors.pop() #stack pop
            return self.backward() #recusively traceback until feasible intersection
        
        self._location = branch[0] #new direction's corresponding location
            

    def move(self):
        self._gameboard[self._location[0]][self._location[1]] = 'V' #record visited cells
        
        if self.visualizer:
            self.visualizer.maze = self._gameboard
            self.visualizer.draw()

        neighbour = self.check_direction()
        if len(neighbour) < 4 and self._location != self.entrance: #reach edge and not entrance
            row, col = self._location

            if self.visualizer:
                self.visualizer.maze = self._gameboard
                self.visualizer.draw()

            return True #game succuss
        
        if list(neighbour.values()).count(' ') == 1: #normal path
            self._location = [key for key, value in neighbour.items() if value == ' '][0] #move to blank cell     
        elif list(neighbour.values()).count(' ') > 1: #more than 1 path: intersection
            self.intersection(neighbour)
        else:
            return self.backward() #dead end; backtracking
        
    @classmethod
    def show_path(cls, destination): #path display
        intersection = [anchor._location for anchor in cls.anchors] #intersection location
        path = [anchor._direction[0] for anchor in cls.anchors] #corresponding direction
        
        solver = cls(cls.entrance, None) #forward navigation

        cls._gameboard[solver._location[0]][solver._location[1]] = 'P' #'P' for final path
        if cls.visualizer:
            cls.visualizer.maze = cls._gameboard
            cls.visualizer.draw()
        distance = 1

        while solver._location != destination._location:
            if solver._location in intersection:
                solver._location = path.pop(0) #guiding direction
            else:
                neighbour = solver.check_direction()
                solver._location = [key for key, value in neighbour.items() if value == 'V'][0] #normal routing

            distance += 1    
            cls._gameboard[solver._location[0]][solver._location[1]] = 'P'
            if cls.visualizer:
                cls.visualizer.maze = cls._gameboard
                cls.visualizer.draw()
        return distance

if __name__ == "__main__":
    DFS_solver.start()
    print(DFS_solver._gameboard)