from grid import *
from random import randint, choice, shuffle
import heapq

def hunt_kill(grid):
    current_cell = grid.random_cell();

    while(current_cell):
        unvisited_neighbors = list(filter(lambda x:
                                          len(x.getlinks()) == 0,
                                          current_cell.neighbors()))
        if(len(unvisited_neighbors) > 0):
            #KILL
            next_cell = choice(unvisited_neighbors)
            current_cell.link(next_cell)
            current_cell = next_cell
        else:
            #HUNT
            for cell in grid.each_cell():
                visited_neighbors = list(filter(lambda x:
                                               len(x.getlinks()) > 0,
                                               cell.neighbors()))
                if(len(cell.getlinks()) == 0 and len(visited_neighbors) > 0):
                    current_cell = cell
                    next_cell = choice(list(visited_neighbors))
                    cell.link(next_cell)
                    break
            else:
                current_cell = None

def recursive_backtracker(grid):
    current_cell = grid.random_cell();
    stack = [current_cell]

    while(current_cell): 
        unvisited_neighbors = list(filter(lambda x:
                                          len(x.getlinks()) == 0,
                                          current_cell.neighbors()))
        if(len(unvisited_neighbors) > 0):
            next_cell = choice(unvisited_neighbors)
            current_cell.link(next_cell)
            current_cell = next_cell
            stack.append(current_cell)
        else:
            while(len(stack) > 0):
                cell = stack[-1]
                unvisited_neighbors = list(filter(lambda x:
                                               len(x.getlinks()) ==  0,
                                               cell.neighbors()))
                if(len(unvisited_neighbors) > 0):
                    current_cell = cell
                    next_cell = choice(list(unvisited_neighbors))
                    cell.link(next_cell)
                    current_cell = next_cell
                    stack.append(current_cell)
                    break
                else:
                    stack.pop()
            else:
                current_cell = None

def kruskals(grid):
    state = State(grid)
    shuffle(state.neighbors)
    while(state.neighbors):
        left, right = state.neighbors.pop()
        if state.can_merge(left, right):
            state.merge(left,right)

def prims(grid):
    active = [grid.random_cell()]
    while active:
        cell = choice(active)
        unvisited_neighbors = list(filter(lambda x:
                                               len(x.getlinks()) ==  0,
                                               cell.neighbors()))
        if(unvisited_neighbors):
            neighbor = choice(unvisited_neighbors)
            cell.link(neighbor)
            active.append(neighbor)
        else:
            active.remove(cell)

def aldous_broder(grid):
    cell = grid.random_cell()
    unvisited = grid.size() - 1;

    while(unvisited > 0):
        neighbor = choice(cell.neighbors())
        if(not neighbor.getlinks()):
            cell.link(neighbor)
            unvisited -= 1
        cell = neighbor


def divide(row, column, height, width, grid):
    if(height <= 1 or width <= 1):
        return
    if(height > width):
        divide_horizontally(row, column, height, width, grid)
    else:
        divide_vertically(row, column, height, width, grid)

def divide_horizontally(row, column, height, width, grid):
    divide_south_of = randint(0, height - 2)
    passage_at = randint(0, width - 1)
    for x in range(width):
        if(not (passage_at == x)):
            cell = grid.getCell(row + divide_south_of, column + x)
            cell.unlink(cell.south)

    divide(row, column, divide_south_of + 1, width, grid)
    divide(row + divide_south_of + 1, column, height - divide_south_of - 1, width, grid)


def divide_vertically(row, column, height, width, grid):
    divide_east_of = randint(0, width - 2)
    passage_at = randint(0, height - 1)
    for y in range(height):
        if(not (passage_at == y)):
            cell = grid.getCell(row + y, column + divide_east_of)
            cell.unlink(cell.east)

    divide(row, column, height, divide_east_of + 1, grid)
    divide(row, column + divide_east_of + 1, height, width - divide_east_of - 1, grid)

    
def recursive_division(grid):
    for cell in grid.each_cell():
        for neighbor in cell.neighbors():
            cell.link(neighbor, False)

    divide(0, 0, grid.rows, grid.columns, grid)


#Used to find shortest paths
def dijkstra(grid, start):
    Queue = []
    start.setCost(0)
    heapq.heappush(Queue, start)
    for cell in grid.each_cell():
        if(cell is not start):
            cell.setCost(float('Inf'))
            heapq.heappush(Queue, cell)
    while(Queue):
        cell = heapq.heappop(Queue)
        for neighbor in cell.getlinks():
            if(cell.getCost() + 1 < neighbor.getCost()):
                neighbor.setCost(cell.cost + 1)
                heapq.heapify(Queue)

#Helper functions and classes for maze generation algorithms

#Used by kruskals                
class State:
    def __init__(self, grid):
        self.grid = grid
        self.neighbors = []
        self.set_for_cell = {}
        self.cells_in_set = {}

        for cell in self.grid.each_cell():
            s = len(self.set_for_cell)

            self.set_for_cell[cell] = s
            self.cells_in_set[s] = [cell]

            if(cell.south):
                self.neighbors.append([cell, cell.south])
            if(cell.east):
                self.neighbors.append([cell, cell.east])

    def can_merge(self, left, right):
        return self.set_for_cell[left] is not self.set_for_cell[right]

    def merge(self, left, right):
        left.link(right)

        winner = self.set_for_cell[left]
        loser = self.set_for_cell[right]
        losers = self.cells_in_set[loser] or [right]

        for cell in losers:
            self.cells_in_set[winner].append(cell)
            self.set_for_cell[cell] = winner
        del self.cells_in_set[loser]
            
            
        
        
            


