import random
from union_find import UnionFind

class Maze_generator:
    def __init__(self, row, column, cycle): #maze framework
        self.size = (row, column)
        self.cycle = cycle #loop ratio

    @classmethod
    def generate(cls, row = 19, column = 19, cycle = 0, entrance = (1, 0), exit = (-2, -1)): #default setting
        generator = cls(row, column, cycle)
        row, column = (row - 1) // 2, (column - 1) // 2 # (n,n) will expand to (2n+1, 2n+1)
        cell_list = UnionFind(row * column) #initialize cell list with union-find

        vertical_wall = [((r, c), (r, c + 1)) for r in range(row) for c in range(column - 1)] #wall seperate cells in a row
        horizontal_wall = [((r, c), (r + 1, c)) for r in range(row - 1) for c in range(column)] #wall seperate cells in a column
        wall_list = vertical_wall + horizontal_wall
        random.shuffle(wall_list) #ensure unbiased maze generation
    
        wall_break = []
        for cell_1, cell_2 in wall_list:
            id_1 = cell_1[0] * column + cell_1[1]
            id_2 = cell_2[0] * column + cell_2[1]

            if cell_list.union(id_1, id_2): #connect two unconnected cells
                wall_break.append((cell_1, cell_2)) #record the wall between
                if len(wall_break) == row * column - 1: #MST already generated
                    break

        map = generator.connect_cell(wall_break)
        wall_remain = list(set(wall_list) - set(wall_break))
        map = generator.cycle_path(map, len(wall_list), wall_remain) #break some remain walls according to a ratio

        map[entrance[0]][entrance[1]], map[exit[0]][exit[1]] = ' ', ' ' #break entrance and exit
        return map, entrance #return values for solvers

    @staticmethod
    def break_wall(map, walls): #break list of walls
        for wall in walls:
            if wall[0][0] == wall[1][0]: #horizontal wall
                row = wall[0][0] * 2 + 1 #calculate cell id
                column = wall[0][1] * 2 + 2
            else:                         #verticle wall
                row = wall[0][0] * 2 + 2
                column = wall[0][1] * 2 + 1

            map[row][column] = ' ' #set wall to path

    def connect_cell(self, connection):
        map = [['■' if row % 2 == 0 or column % 2 == 0 else ' ' #initialize a maze with all cells seperated
                for column in range(self.size[1])] for row in range(self.size[0])]
        self.break_wall(map, connection) #break recorded walls

        return map
    
    def cycle_path(self, map, total_wall, remained): #break remain walls to create cycle
        random.shuffle(remained)
        break_part = round(total_wall * self.cycle) #explicit break number
        self.break_wall(map, remained[:break_part]) #break shuffled walls 

        return map          #update map