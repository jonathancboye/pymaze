from random import randint, random, choice
from algo import hunt_kill, recursive_backtracker, dijkstra, kruskals, prims, aldous_broder, recursive_division

class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.value = " ";
        self.cost = 1
        self.north = None;
        self.south = None;
        self.east = None;
        self.west = None;
        self.links = {};

    def __lt__(self, cell):
        return self.cost < cell.getCost()

    def __str__(self):
        return "(" + str(self.row) + "," + str(self.column) + ")"
    
    def link(self, cell, bidi=True):
        self.links[cell] = True
        if(bidi):
            cell.link(self, False)
        
    def unlink(self, cell, bidi=True):
        del self.links[cell]
        if(bidi):
            cell.unlink(self, False)

    def getlinks(self):
        return self.links.keys();

    def linked(self, cell):
        return cell in self.links;

    def neighbors(self):
        retval = [];
        if(self.north):
            retval.append(self.north);
        if(self.south):
            retval.append(self.south);
        if(self.east):
            retval.append(self.east);
        if(self.west):
            retval.append(self.west);
        return retval;

    def setValue(self, value):
        self.value = str(value)

    def getValue(self):
        return self.value

    def setCost(self, cost):
        self.cost = cost

    def getCost(self):
        return self.cost
        
class Grid:

    def __init__(self, rows, columns):
        self.rows = rows;
        self.columns = columns;
        self.print_size = 5
        self.Cells = [[Cell(row, column) for column in range(self.columns)] for row in range(self.rows)];
        self.configure_cells();
        self.start = self.Cells[0][0];
        self.end = self.Cells[self.rows - 1][self.columns - 1];
        self.start.setValue("S")
        self.end.setValue("E")


        #self.set_start_end();

    def __str__(self):
        dashes = self.print_size * "-"
        output = "+" + (dashes + "+") * self.columns + "\n"
        for row in self.Cells:
            top = "|"
            bottom = "+"
            pad = ""
            for cell in row:
                #format value of cell
                value = cell.getValue()
                start_pos = int(self.print_size/2) - int(len(value)/2)
                end_pos = start_pos + len(value) - 1
                body = ""
                for i in range(self.print_size):
                    if(i < start_pos or i > end_pos):
                        body += " "
                    else:
                        body += value[i - start_pos]

                #format the rest of cell
                east_boundary = " " if cell.linked(cell.east) else "|"
                top += body + east_boundary
                pad += self.print_size * " " + east_boundary
                south_boundary = self.print_size * " " if cell.linked(cell.south) else dashes
                corner = "+"
                bottom += south_boundary + corner

            output += top + "\n"
            for i in range(int(self.print_size/2) - 1):
                output +=  "|" + pad + "\n"
            output += bottom + "\n"
        return output

    #Get a cell within grid bounds
    def getCell(self, row, column):
        if(row < 0 or self.rows <= row):
            return None;
        if(column < 0 or self.columns <= column):
            return None;
        return self.Cells[row][column];

    #Create the grid
    def configure_cells(self):
        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.Cells[row][column];
                cell.north = self.getCell(row - 1, column);
                cell.south = self.getCell(row + 1, column);
                cell.east = self.getCell(row, column + 1);
                cell.west = self.getCell(row, column - 1);

    #Set the start and end point of the grid
    def set_start_end(self):
        while(True):
            self.start = self.random_cell()
            self.end = self.random_cell()
            if(self.start is not self.end):
                break
        self.start.setValue("S")
        self.end.setValue("E")

    def clearValues(self):
        for cell in self.each_cell():
            if(not(cell.getValue() == " S " or cell.getValue() == " E ")):
                cell.setValue(" ")

    def clearCost(self):
        for cell in self.each_cell():
            cell.setCost(1)
        
    def random_cell(self):
        row = randint(0, self.rows - 1);
        column = randint(0, self.columns - 1);
        return self.getCell(row, column);

    def size(self):
        return self.rows * self.columns

    def each_row(self):
        for row in self.Cells:
            yield row

    def each_cell(self):
        for row in self.Cells:
            for cell in row:
                yield cell

    def braid(self, p=1.0):
        for cell in self.dead_ends():
            not_linked = list(filter(lambda x : x not in cell.getlinks(),
                                     cell.neighbors()))
            if(p > random() and len(not_linked) > 0):
                cell.link(choice(not_linked))
            
    def dead_ends(self):
        return [cell for cell in self.each_cell() if len(cell.getlinks()) == 1]

    def longest_path(self):
        dijkstra(self, self.start)
        return max(self.each_cell()).cost

    def average_path_length(self):
        cost = 0
        for cell in self.each_cell():
            cost += cell.getCost()
        return cost / self.size()
        
    def direct_twists_intersect(self):
        twistiness = 0
        directness = 0
        intersections = 0
        for cell in self.each_cell():
            if(len(cell.getlinks()) > 2):
                intersections += 1

            if((cell.linked(cell.north) or cell.linked(cell.south)) and
               (cell.linked(cell.east) or cell.linked(cell.west))):
                twistiness += 1
            else:
                directness += 1
        return twistiness, directness, intersections

    def passages(self):
        south = 0
        north = 0
        east = 0
        west = 0
        for cell in self.each_cell():
            if(cell.south):
                south += 1
            if(cell.north):
                north += 1
            if(cell.east):
                east += 1
            if(cell.west):
                west += 1
        return south, north, east, west
