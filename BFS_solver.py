from maze_solver import Solver
from queue import Queue
import time

class BFS_Solver(Solver):
    nodes = Queue() #maintain a queue to ensure balanced move of each branch

    def __init__(self, location, path):
        super().__init__(location)
        self._path = path #record the direction of intersections passed

    @classmethod
    def start(cls):
        cls.nodes = Queue() #empty the original queue
        cls._gameboard = [[cell for cell in row] for row in Solver._gameboard] #deep copy gameboard
        cls.nodes.put(cls(cls.entrance, [])) #enqueue for entrance
        final_state = False

        while not final_state: #continue moving
            final_state = cls.move()

        if final_state == 'No solution':
            print(final_state)
        else:
            distance = cls.show_path(final_state)  #display final path 
            if cls.visualizer:
                cls.visualizer.maze = cls._gameboard
                cls.visualizer.draw()
                time.sleep(1)    

    def intersection(self, neighbour):
        for index, (key, value) in enumerate(neighbour.items()): #split branches equal to number of forks
            if value == ' ':
                self.nodes.put(BFS_Solver(key, self._path + [index])) #all branches queue; will be used sequentially

    @classmethod

    def move(cls):
        node = cls.nodes.get() #dequeue
        cls._gameboard[node._location[0]][node._location[1]] = 'V' #record visited
        if cls.visualizer:
            cls.visualizer.maze = cls._gameboard
            cls.visualizer.draw()

        neighbour = node.check_direction()
        if len(neighbour) < 4 and node._location != cls.entrance: #edge checking; if not entrance than success
            return node
        
        if list(neighbour.values()).count(' ') == 1: #normal route
            node._location = [key for key, value in neighbour.items() if value == ' '][0]      
            cls.nodes.put(node) #enqueue with new location  
        elif list(neighbour.values()).count(' ') > 1: #check intersection
            node.intersection(neighbour)
        elif cls.nodes.empty(): #dequeue disabled; all ways unpractical
            return 'No solution'
        
    @classmethod
    def show_path(cls, destination):
        solver = cls(cls.entrance, destination._path[:]) #a new solver copying path list
        cls._gameboard[solver._location[0]][solver._location[1]] = 'P' #'P' for final path
        if cls.visualizer:
            cls.visualizer.maze = cls._gameboard
            cls.visualizer.draw()
        distance = 1

        while solver._location != destination._location: #move until reach exit
            neighbour = solver.check_direction()

            if list(neighbour.values()).count('V') == 1: #normal route
                solver._location = [key for key, value in neighbour.items() if value == 'V'][0]       
            elif list(neighbour.values()).count('V') > 1:
                solver._location = list(neighbour.keys())[solver._path[0]] #move to direction recorded
                solver._path.pop(0) #path copy pops used direction

            distance += 1    
            cls._gameboard[solver._location[0]][solver._location[1]] = 'P'
            if cls.visualizer:
                cls.visualizer.maze = cls._gameboard
                cls.visualizer.draw()

        return distance
    
if __name__ == "__main__": #load if at main program
    BFS_Solver.start()
    print(BFS_Solver._gameboard)