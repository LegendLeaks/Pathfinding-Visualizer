from tkinter import messagebox, Tk
import pygame
import sys
import time
import random


WIN_WIDTH = 500
WIN_HEIGHT = 500

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

COLUMNS = 25
ROWS = 25

CELL_WIDTH = WIN_WIDTH // COLUMNS
CELL_HEIGHT = WIN_HEIGHT // ROWS

WHITE = (255, 255, 255)
BLUE = (42, 205, 230)
LIGHT_BLUE = (120, 228, 245)
DARK_BLUE = (20, 127, 209)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (130, 130, 130)

grid = []
queue = []
path = []

class Cell:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.end = False
        self.queued = False
        self.visited = False
        self.nearby_cells = []
        self.prior = None

    def draw(self, win, colour):
        gap = 1
        if self.start or self.wall or self.end:
            gap = 0
        pygame.draw.rect(win, colour, (self.x * CELL_WIDTH, self.y * CELL_HEIGHT, CELL_WIDTH - gap, CELL_HEIGHT - gap))

    def set_nearby_cells(self):
        # gets nearby cells by checking if there are valid cells in all 4 directions
        if self.x > 0: #if valid cell to the left
            self.nearby_cells.append(grid[self.x - 1][self.y])
        if self.x < COLUMNS - 1: #if valid cell to the right
            self.nearby_cells.append(grid[self.x + 1][self.y])
        if self.y > 0: #if valid cell above
            self.nearby_cells.append(grid[self.x][self.y - 1])
        if self.y < ROWS - 1: #if valid cell below
            self.nearby_cells.append(grid[self.x][self.y + 1])

# create grid
for i in range(COLUMNS):
    array = []
    for j in range(ROWS):
        array.append(Cell(i, j))
    grid.append(array)

#set neighbouring cells to each cell in grid
for i in range(COLUMNS):
    for j in range(ROWS):
        grid[i][j].set_nearby_cells()

end_cell = grid[24][24]
end_cell.end = True

start_cell = grid[0][0]
start_cell.start = True



def main():
    run = True
    begin_search = False
    searching = True

    global end_cell

    while run:
        for event in pygame.event.get():
            #quit window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouse controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                #draw wall
                if event.buttons[0] and not begin_search: #if left mouse down
                    i = x // CELL_WIDTH
                    j = y // CELL_HEIGHT
                    try:
                        if not grid[i][j].wall and not grid[i][j].wall:
                            grid[i][j].wall = True
                    except:
                        print('drawing out of bounds')
                
                #set start cell
                if event.buttons[1] and not begin_search:
                    global start_cell
                    start_cell.start = False
                    i = x // CELL_WIDTH
                    j = y // CELL_HEIGHT
                    try:
                        start_cell = grid[i][j]
                    except:
                        print('drawing out of bounds')
                    start_cell.start = True
                    if start_cell.wall:
                        start_cell.wall = False
                
                #set end cell
                if event.buttons[2] and not begin_search:
                    end_cell.end = False
                    i = x // CELL_WIDTH
                    j = y // CELL_HEIGHT
                    try:
                        end_cell = grid[i][j]
                    except:
                        print('drawing out of bounds')
                    end_cell.end = True
                    if end_cell.wall:
                        end_cell.wall = False

            #start algorithm
            if event.type == pygame.KEYDOWN and not begin_search:
                begin_search = True
                start_cell.visited = True
                queue.append(start_cell)
        
        if begin_search:
            if len(queue) > 0 and searching:
                current_cell = queue.pop(0)
                current_cell.visited = True
                if current_cell == end_cell: #target found
                    target_found = True
                    searching = False
                    while current_cell.prior != start_cell:
                        path.append(current_cell.prior)
                        current_cell = current_cell.prior
                else:
                    #add neighbouring cells to queue
                    for neighbour in current_cell.nearby_cells:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_cell
                            queue.append(neighbour)
            else: #if there is no solution
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo('No Solution', 'There is no solution.')
                    searching = False


        window.fill(BLUE)
        
        for i in range(COLUMNS):
            for j in range(ROWS):
                cell = grid[i][j]
                cell.draw(window, WHITE)

                if cell.queued:
                    cell.draw(window, LIGHT_BLUE)
                if cell.visited:
                    cell.draw(window, BLUE)
                if cell in path:
                    cell.draw(window, DARK_BLUE)

                if cell.start:
                    cell.draw(window, GREEN)
                if cell.wall:
                    cell.draw(window, BLACK)
                if cell.end:
                    cell.draw(window, RED)


        pygame.display.update() #updates display

main()