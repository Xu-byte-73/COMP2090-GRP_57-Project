import tkinter as tk
from maze_solver import Solver
from BFS_solver import BFS_Solver
from DFS_solver import DFS_solver
from Tremaux_solver import Trémaux_solver
import time
from maze_generator import Maze_generator


class MazeVisualizer:
    def __init__(self, canvas, maze, player_pos, cell_size=20, delay=0.05):
        self.canvas = canvas
        self.maze = maze
        self.player_pos = player_pos
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.cell_size = cell_size
        self.delay = delay

    def draw(self):
        self.canvas.delete("all")

        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.maze[r][c]

                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = self.get_color(cell)

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="gray"
                )

        # draw player
        r, c = self.player_pos
        x1 = c * self.cell_size
        y1 = r * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e74c3c")

        self.canvas.update()
        time.sleep(self.delay)

    def get_color(self, cell):
        #User path
        if cell == "U":
            return "grey"
        
        #DFS, BFS
        if cell == "■" or cell == 10:
            return "black"
        if cell == "V":
            return "blue"
        if cell == " ":
            return "white"
        if cell == "P":
            return "yellow"

        #Trémaux
        if isinstance(cell, (int, float)):
            if cell == 0:
                return "white"
            elif 0 < cell < 1:
                return "yellow"
            elif 1 <= cell < 2:
                return "orange"
            elif cell >= 2:
                return "red"

        return "white"


class MazeUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Maze Solver")
        self.root.geometry("600x700")
        self.palyer_start_time = None
        self.player_running = False

        # keyboard control
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        # generate maze
        self.original_maze, self.entrance = Maze_generator.generate(19, 19, 0)
        self.player_pos = self.entrance
        self.maze = [row.copy() for row in self.original_maze]

        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.cell_size = 25

        self.canvas = tk.Canvas(
            self.root,
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="white"
        )
        self.canvas.pack(pady=20)

        self.visualizer = MazeVisualizer(
            self.canvas,
            self.maze,
            self.player_pos,
            cell_size=self.cell_size,
            delay=0.05
        )

        # buttons
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="BFS", width=10,
                  command=lambda: self.run_solver("bfs")).grid(row=0, column=0, padx=5)

        tk.Button(frame, text="DFS", width=10,
                  command=lambda: self.run_solver("dfs")).grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Trémaux", width=10,
                  command=lambda: self.run_solver("tremaux")).grid(row=0, column=2, padx=5)

        tk.Button(self.root, text="Reset", width=10,
                  command=self.reset).pack(pady=10)

        tk.Button(self.root, text="Quit", width=10,
                  command=self.root.quit).pack(pady=5)

        self.draw_maze()

    def run_solver(self, algo):
        maze_copy = [row.copy() for row in self.original_maze]

        Solver._gameboard = None
        Solver.visualizer = None

        Solver.initialization(maze_copy, self.entrance, self.visualizer)

        start_time = time.time()#start timing

        if algo == "bfs":
            BFS_Solver.start()

        elif algo == "dfs":
            DFS_solver.start()

        elif algo == "tremaux":
            Trémaux_solver.start()

        end_time = time.time()#stop timing
        times = end_time - start_time

        print(f"{algo.upper()} time: {times:.4f} seconds")

        self.maze = Solver._gameboard
        self.visualizer.maze = self.maze
        self.visualizer.player_pos = self.player_pos
        self.visualizer.draw()

    def reset(self):
        self.original_maze, self.entrance = Maze_generator.generate(19, 19, 0)
        self.player_pos = self.entrance
        self.maze = [row.copy() for row in self.original_maze]

        Solver._gameboard = None
        Solver.visualizer = None

        self.visualizer.maze = self.maze
        self.visualizer.player_pos = self.player_pos
        self.visualizer.draw()

    def draw_maze(self):
        self.visualizer.maze = self.maze
        self.visualizer.player_pos = self.player_pos
        self.visualizer.draw()

    # player movement
    def move_player(self, dr, dc):
        r, c = self.player_pos
        new_r, new_c = r + dr, c + dc

        if (0 <= new_r < self.rows and
            0 <= new_c < self.cols and
            self.maze[new_r][new_c] != "■"):

            if not self.player_running:
                self.palyer_start_time = time.time()
                self.player_running = True

            self.maze[r][c] = "U"

            self.player_pos = (new_r, new_c)
            self.visualizer.player_pos = self.player_pos
            self.draw_maze()

            if self.player_pos == (self.rows - 2, self.cols - 1):
                end_time = time.time()
                print(f"Player time: {end_time - self.player_start_time:.4f} seconds")
                self.player_running = False
                
    def move_up(self, event):
        self.move_player(-1, 0)

    def move_down(self, event):
        self.move_player(1, 0)

    def move_left(self, event):
        self.move_player(0, -1)

    def move_right(self, event):
        self.move_player(0, 1)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MazeUI()
    app.run()