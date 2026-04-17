# Interactive Maze Generator and Solver

# Interactive Maze Generator and Solver

## 1. Introduction
This project provides a simple interactive maze application with a graphical interface. You can generate random mazes, solve them using different algorithms, and reset the maze with one click. The program uses **backtracking (DFS)** as the main solving algorithm, along with BFS and Trémaux’s method for comparison.

## 2. Design
### Algorithms
- **Backtracking (DFS)** – The primary solving algorithm. Explores each path until a dead end, then backtracks. Marks visited cells to avoid loops. Time complexity O(rows × cols).
- **BFS** – Explores level by level; finds the shortest path.
- **Trémaux’s algorithm** – Wall‑following with marking; at intersections, chooses the least‑visited direction.

### Data Structures
- **Stack** – Used explicitly in the iterative DFS solver.
- **Queue** – Used in BFS.
- **Union‑Find** – Used only for maze generation (Kruskal), not for solving.
- **2D list** – Represents the maze grid.

### OOP Design
- **`Solver` (ABC)** – Abstract base class defining `move()`, `intersection()`, `show_path()`.
- **`DFS_solver`, `BFS_solver`, `Trémaux_solver`** – Concrete subclasses.
- **`Maze_generator`** – Generates mazes (randomized Kruskal).
- **GUI** – Buttons for algorithm selection and a **Reset** button to generate a new maze.

## 3. Run Instructions
1. Ensure Python 3.7+ is installed.
2. Run the main script:
   ```bash
   python main.py
