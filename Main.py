import pygame
from Maze import main
pygame.init()
win=pygame.display.set_mode((840,480))
win.fill((255,255,255))

from Maze import button
run=True
pygame.display.set_caption('MAZE')

greenbutton=button((0,255,0),295,25,250,100,"Start Game")
quitbutton=button((0,255,0),295,150,250,100,"Exit")



def redrawWindow():
    win.fill((0,0,0))
    greenbutton.draw(win,(0, 0, 0))
    quitbutton.draw(win,(0,0,0))


while run:
    redrawWindow()
    pygame.display.update()
    for event in pygame.event.get():
        pos=pygame.mouse.get_pos()
        if event.type==pygame.QUIT:
            run=False
            pygame.quit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if greenbutton.isOver(pos):
                redrawWindow()

                pygame.display.update()
                main()
            elif quitbutton.isOver(pos):
                run=False
                pygame.quit()


        if event.type==pygame.MOUSEMOTION:
            if greenbutton.isOver(pos):
                greenbutton.color=(255,0,0)
            else:
                greenbutton.color=(0,255,0)
            if quitbutton.isOver(pos):
                quitbutton.color=(255,0,0)

            else:
                quitbutton.color=(0,255,0)
