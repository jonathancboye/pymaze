from maze import Maze
from algo import hunt_kill, recursive_backtracker, kruskals, aldous_broder, recursive_division

maze = Maze(6, 6, kruskals, 0)
for cell in maze.grid.each_cell():
    cell.setValue(cell.cost)
print(maze)
print "Longest Path: ", maze.longest_path
