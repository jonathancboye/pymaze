from grid import *
from math import log, floor

class Maze:
    def __init__(self, num_rows, num_columns, algo, braid=0):
        self.grid = Grid(num_rows, num_columns)
        algo(self.grid)
        self.grid.braid(braid)

        self.south, self.north, self.east, self.west = self.grid.passages()
        self.dead_ends = len(self.grid.dead_ends())
        self.twistiness, self.directness, self.intersections = self.grid.direct_twists_intersect()
        self.longest_path = self.grid.longest_path()
        self.average_path_length = self.grid.average_path_length()
        self.path = []
        self.steps = self.solve3()

    def __str__(self):
        return self.grid.__str__()

    def solution(self):
        self.path = [self.grid.start]
        self.steps = self.solve(self.grid.start, self.grid.end, self.path)

    def solve(self, start, end, visited):
        if(start is end):
            return 0
        else:
            linked_neighbors = [cell for cell in start.getlinks() if cell not in visited]
            if(linked_neighbors):
                next_cell = choice(linked_neighbors)
                visited.append(next_cell)
                if(next_cell is not start and next_cell is not end):
                    next_cell.setValue("x")
                return 1 + self.solve(next_cell, end, visited)
            else:
                previous_cell = visited[visited.index(start) - 1]
                visited.append(previous_cell)
                return 1 + self.solve(previous_cell, end, visited)
                
    def solve2(self):
        current_cell = self.grid.start
        visited = [current_cell]
        steps = 0
        while(current_cell is not self.grid.end):
            linked_neighbors = [cell for cell in current_cell.getlinks() if cell not in visited]
            if(linked_neighbors):
                next_cell = choice(linked_neighbors)
                visited.append(next_cell)
                if(next_cell is not self.grid.start and next_cell is not self.grid.end):
                    next_cell.setValue("x")
                steps += 1
                current_cell = next_cell
            else:
                current_cell = visited[visited.index(current_cell) - 1]
                visited.append(current_cell)
                steps += 1
        self.path = visited
        return steps

    def solve3(self):
        current_cell = self.grid.start
        visited = [current_cell]
        steps = 0
        while(current_cell is not self.grid.end):
            linked_neighbors = [cell for cell in current_cell.getlinks() if cell not in visited]
            if(linked_neighbors):
                if(current_cell.south in linked_neighbors):
                    next_cell = current_cell.south
                elif(current_cell.east in linked_neighbors):
                    next_cell = current_cell.east
                elif(current_cell.north in linked_neighbors):
                    next_cell = current_cell.north
                elif(current_cell.west in linked_neighbors):
                    next_cell = current_cell.west
                else:
                    print("SOMETHING IS WRONG")
                    exit(2)
                visited.append(next_cell)
                if(next_cell is not self.grid.start and next_cell is not self.grid.end):
                    next_cell.setValue("x")
                steps += 1
                current_cell = next_cell
            else:
                current_cell = visited[visited.index(current_cell) - 1]
                visited.append(current_cell)
                steps += 1
        self.path = visited
        return steps
