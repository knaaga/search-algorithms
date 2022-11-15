import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk

# grid dimensions
width = 640
height = 480
size = (width, height)
cols, rows = 64, 48
w = width // cols
h = height // rows
grid = []

# pygame initialization
pygame.init()
win = pygame.display.set_mode(size)
pygame.display.set_caption("Path Finding Algorithms - Breadth First Search")
clock = pygame.time.Clock()


class Cell:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.wall = False

    def show(self, window, col):
        if self.wall:
            col = (0, 0, 0)
        pygame.draw.rect(window, col, (self.x * w, self.y * h, w - 1, h - 1))

    def add_neighbors(self, grid):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state


# required data structures
open = deque()
closed = set()
predecessors = dict()
path = []

# populate grid
for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Cell(i, j))
    grid.append(arr)

# set neighbors
for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

# start and goal nodes
start = grid[10][10]
goal = grid[40][30]
start.wall = False
goal.wall = False

open.append(start)
closed.add(start)

stopSearchFlag = False
def BFS():
    global stopSearchFlag
    if len(open) > 0 and not stopSearchFlag:  # don't use while loop because it won't update dynamically then
        current = open.popleft() # pop current node
        if current == goal: # goal check
            print("Found Goal Node!")
            stopSearchFlag = True  # BFS stops here
            temp = goal
            while temp in predecessors:
                path.append(predecessors[temp])
                temp = predecessors[temp]
            print("Total Path Cost:", len(path))

        if not stopSearchFlag:  # do this only if search is not stopped
            for neighbor in current.neighbors: # get neighbors
                if neighbor not in closed and neighbor not in open and not neighbor.wall:
                    predecessors[neighbor] = current
                    open.append(neighbor) # add neighbors to open list
                    # closed.add(neighbor) # add neighbors to close list
            closed.add(current) # add current node to closed list

    else:
        if not stopSearchFlag:
            return -1

if __name__ == "__main__":

    startAlgorithm = False

    while True:
        # visualization loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    clickWall(pygame.mouse.get_pos(), event.button == 1)
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:
                    # if left mouse button is pressed, event.buttons[0] = True. Hence the wall is set to true
                    # if right mouse is pressed, event.buttons[0] = False. Hence the wall is set to true
                    left_button_status = event.buttons[0]
                    clickWall(pygame.mouse.get_pos(), left_button_status)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startAlgorithm = True

        if startAlgorithm:
            result = BFS()
            if result == -1:
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There was no solution")
                break


        # set colors based on whether the cell is in visited or frontier or start/end
        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (250,201,110))
                if spot in path:
                    spot.show(win, (245, 102, 86))
                elif spot in closed:
                    spot.show(win, (110, 201, 250))
                if spot in open:
                    spot.show(win, (110, 133, 250))
                if spot == start:
                    spot.show(win, (73, 235, 143))
                if spot == goal:
                    spot.show(win, (235, 73, 181))

        pygame.display.flip()
