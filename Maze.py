import sys
import time

import pygame, random
from pygame.locals import *

MAX_LEVELS = 4
class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


rows = 4
columns = 6
size = 100
class Maze:
    def __init__(self, mazeLayer, solveLayer, level):
        self.mazeArray = []
        global rows,columns,size
        levels = {
            1: {
                "r":4,
                "c":6,
                "s":100
            },
            2: {
                "r": 8,
                "c": 12,
                "s": 50
            },
            3: {
                "r": 16,
                "c": 24,
                "s": 25
            },
            4: {
                "r": 40,
                "c": 60,
                "s": 10
            }
        }
        self.level = level
        rows = levels[level]["r"]
        columns = levels[level]["c"]
        size = levels[level]["s"]
        self.state = 'c'
        self.mLayer = mazeLayer  # surface
        self.sLayer = solveLayer  # surface
        self.mLayer.fill((0, 0, 0, 0))
        self.sLayer.fill((0, 0, 0, 0))
        for y in range(rows+1):
            pygame.draw.line(self.mLayer, (0, 0, 0, 255), (0, y * size), (columns * size, y * size))
            for x in range(columns):
                self.mazeArray.append(0)
                if (y == 0):
                    pygame.draw.line(self.mLayer, (0, 0, 0, 255), (x * size, 0), (x * size, rows * size))
        pygame.draw.rect(self.sLayer, (0, 0, 255, 255), Rect(0, 0, size, size))
        pygame.draw.rect(self.sLayer, (255, 0, 255, 255),
                         Rect(((columns * size - size)), (rows * size - size), size, size))
        # Maze Section
        self.totalCells = rows * columns
        self.currentCell = random.randint(0, self.totalCells - 1)
        self.visitedCells = 1
        self.cellStack = []
        self.compass = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def update(self):
        global nidx
        if self.state == 'c':

            if self.visitedCells >= self.totalCells:
                self.currentCell = 0  # set current to top-left
                self.cellStack = []
                self.state = 'p'
                return
            moved = False
            while (self.visitedCells < self.totalCells):  # moved == False):
                x = self.currentCell % columns
                y = self.currentCell // columns
                neighbors = []
                for i in range(4):
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]
                    if ((nx >= 0) and (ny >= 0) and (nx < columns) and (ny < rows)):
                        if (self.mazeArray[(ny * columns + nx)] & 0x000F) == 0:
                            nidx = ny * columns + nx
                            neighbors.append((nidx, 1 << i))
                if len(neighbors) > 0:
                    idx = random.randint(0, len(neighbors) - 1)
                    nidx, direction = neighbors[idx]
                    dx = x * size
                    dy = y * size
                    if direction & 1:
                        self.mazeArray[nidx] |= (4)
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (dx, dy + 1), (dx, dy + size - 1))
                    elif direction & 2:
                        self.mazeArray[nidx] |= (8)
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (dx + 1, dy + size), (dx + size - 1, dy + size))
                    elif direction & 4:
                        self.mazeArray[nidx] |= (1)
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (dx + size, dy + 1), (dx + size, dy + size - 1))
                    elif direction & 8:
                        self.mazeArray[nidx] |= (2)
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (dx + 1, dy), (dx + size - 1, dy))
                    self.mazeArray[self.currentCell] |= direction
                    self.cellStack.append(self.currentCell)
                    self.currentCell = nidx
                    self.visitedCells = self.visitedCells + 1
                    moved = True
                else:
                    if self.cellStack == []:
                        pass
                    else:
                        self.currentCell = self.cellStack.pop()
        if self.state == "p":

            solutionbutton = button((255, 0, 0), 600, 50, 180, 100, "See Solution")
            solutionbutton.draw(self.mLayer, (0, 0, 0))


            if self.currentCell == (self.totalCells - 1):  # have we reached the exit?
                self.state = 'r'
                return "w"

            for event in pygame.event.get():
                x = self.currentCell % columns
                y = self.currentCell // columns
                dx = x * size
                dy = y * size
                direction=0
                nidx= self.currentCell
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.quitbutton.isOver(pos):
                        pygame.quit()
                        sys.exit()
                    if solutionbutton.isOver(pos):
                        self.state="s"
                        self.currentCell = 0
                        break
                if event.type == pygame.MOUSEMOTION:
                    if self.quitbutton.isOver(pos):
                        self.quitbutton.color = (255, 0, 0)
                    else:
                        self.quitbutton.color = (0, 255, 0)
                    if solutionbutton.isOver(pos):
                        solutionbutton.color = (255, 0, 0)
                    else:
                        solutionbutton.color = (0, 255, 0)
                if event.type == pygame.KEYDOWN:
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_LEFT:
                        nx = x + self.compass[0][0]
                        ny = y + self.compass[0][1]
                        nidx=ny * columns + nx
                        direction=1
                        if(self.mazeArray[self.currentCell])&direction>0:
                            pygame.draw.rect(self.sLayer, (255, 255, 255, 255),
                                             Rect((x*size), (y*size), size, size))
                            pygame.draw.rect(self.sLayer, (0, 255, 0, 255),
                                             Rect((nx * size), (ny * size), size, size))
                        else:
                            continue
                    elif event.key == pygame.K_DOWN:
                        nx = x + self.compass[1][0]
                        ny = y + self.compass[1][1]
                        nidx = ny * columns + nx
                        direction = 2
                        if (self.mazeArray[self.currentCell]) & direction > 0:
                            pygame.draw.rect(self.sLayer, (255, 255, 255, 255),
                                                         Rect((x*size), (y*size), size, size))
                            pygame.draw.rect(self.sLayer, (0, 255, 0, 255),
                                                         Rect((nx * size), (ny * size), size, size))
                        else:
                            continue


                    elif event.key == pygame.K_RIGHT:
                        nx = x + self.compass[2][0]
                        ny = y + self.compass[2][1]
                        nidx = ny * columns + nx
                        direction = 4
                        if (self.mazeArray[self.currentCell]) & direction > 0:
                                pygame.draw.rect(self.sLayer, (255, 255, 255, 255),
                                                         Rect((x*size), (y*size), size, size))
                                pygame.draw.rect(self.sLayer, (0, 255, 0, 255),
                                                         Rect((nx * size), (ny * size), size, size))
                        else:
                            continue
                    if event.key == pygame.K_UP:
                        nx = x + self.compass[3][0]
                        ny = y + self.compass[3][1]
                        nidx = ny * columns + nx
                        direction = 8
                        if (self.mazeArray[self.currentCell]) & direction > 0:
                                pygame.draw.rect(self.sLayer, (255, 255, 255, 255),
                                                         Rect((x*size), (y*size), size, size))
                                pygame.draw.rect(self.sLayer, (0, 255, 0, 255),
                                                         Rect((nx * size), (ny * size), size, size))
                        else:
                            continue

                    self.currentCell = nidx
        elif self.state == 's':
            nextbutton = button((255, 0, 0), 600, 250, 180, 100, "Next level" if self.level<MAX_LEVELS else "Finish")
            nextbutton.draw(self.sLayer, (0, 0, 0))
            if self.currentCell == (self.totalCells-1): # have we reached the exit?
                for event in pygame.event.get():
                    pos=pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.quitbutton.isOver(pos):
                            pygame.quit()
                            sys.exit()
                        if nextbutton.isOver(pos):
                            self.state="r"
                            return "w"

                    if event.type == pygame.MOUSEMOTION:

                        if self.quitbutton.isOver(pos):
                            self.quitbutton.color = (255, 0, 0)
                        else:
                            self.quitbutton.color = (0, 255, 0)
                        if nextbutton.isOver(pos):
                            nextbutton.color = (255, 0, 0)
                        else:
                            nextbutton.color = (0, 255, 0)
                return



            moved = False
            while(not moved):
                x = self.currentCell % columns
                y = self.currentCell //columns
                neighbors = []
                directions = self.mazeArray[self.currentCell] & 0xF
                for i in range(4):
                    if (directions & (1<<i)) > 0:
                        nx = x + self.compass[i][0]
                        ny = y + self.compass[i][1]
                        if ((nx >= 0) and (ny >= 0) and (nx < columns) and (ny < rows)):
                            nidx = ny*columns+nx
                            if ((self.mazeArray[nidx] & 0xFF00) == 0): # make sure there's no backtrack
                                neighbors.append((nidx,1<<i))
                if len(neighbors) > 0:

                    idx = random.randint(0,len(neighbors)-1)
                    nidx,direction = neighbors[idx]
                    dx = x*size
                    dy = y*size
                    if direction & 1:
                        self.mazeArray[nidx] |= (4 << 12)
                    elif direction & 2:
                        self.mazeArray[nidx] |= (8 << 12)
                    elif direction & 4:
                        self.mazeArray[nidx] |= (1 << 12)
                    elif direction & 8:
                        self.mazeArray[nidx] |= (2 << 12)

                    pygame.draw.rect(self.sLayer, (0,255,0,255), Rect(dx,dy,size,size))

                    self.mazeArray[self.currentCell] |= direction << 8
                    self.cellStack.append(self.currentCell)
                    self.currentCell = nidx
                    moved = True
                else:
                    pygame.draw.rect(self.sLayer, (255,255,255,255), Rect((x*size),(y*size),size,size))

                    self.mazeArray[self.currentCell] &= 0xF0FF # not a solution
                    if self.cellStack==[]:
                        pass
                    else:
                        self.currentCell = self.cellStack.pop()
                        moved = True


    def draw(self, screen):

        self.quitbutton = button((255, 0, 0), 600, 150, 180, 100, "Exit")
        self.quitbutton.draw(self.mLayer, (0, 0, 0))
        screen.blit(self.sLayer, (0,0))
        screen.blit(self.mLayer, (0,0))
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()
def main():
    """Maze Main Function - Luke Arntson, Jan '09
        Written using - http://www.mazeworks.com/mazegen/mazetut/index.htm
    """
    pygame.init()
    screen = pygame.display.set_mode((columns * size+200, rows * size))
    pygame.display.set_caption('MAZE')
    pygame.mouse.set_visible(1)
    background = pygame.Surface(((columns * size+200), rows * size))
    background = background.convert()
    background.fill((255, 255, 255))
    mazeLayer = pygame.Surface((columns * size+200, rows * size))
    mazeLayer = mazeLayer.convert_alpha()
    mazeLayer.fill((0, 0, 0, 0))
    solveLayer = pygame.Surface((columns * size+200, rows * size))
    solveLayer = solveLayer.convert_alpha()
    solveLayer.fill((0, 0, 0, 0))
    textLayer = pygame.Surface((columns * size + 200, rows * size))
    textLayer = solveLayer.convert_alpha()
    textLayer.fill((0, 0, 0, 0))
    level=1
    newMaze = Maze(mazeLayer, solveLayer, level)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    while 1:
        clock.tick(240)
        # for event in pygame.event.get():
        #     if event.type == QUIT:
        #         return
        #     elif event.type == KEYDOWN and event.key == K_ESCAPE:
        #         return

        c = newMaze.update()
        if c == "w":
            if level < MAX_LEVELS:
                background = pygame.Surface((columns * size+200, rows * size))
                background = background.convert()
                background.fill((255, 255, 255))
                mazeLayer = pygame.Surface((columns * size+200, rows * size))
                mazeLayer = mazeLayer.convert_alpha()
                mazeLayer.fill((0, 0, 0, 0))
                solveLayer = pygame.Surface((columns * size+200, rows * size))
                solveLayer = solveLayer.convert_alpha()
                solveLayer.fill((0, 0, 0, 0))
                level += 1
                newMaze = Maze(mazeLayer, solveLayer, level)

                screen.blit(background, (0, 0))
            else:
                break



        screen.blit(background, (0, 0))
        newMaze.draw(screen)
        pygame.display.flip()




