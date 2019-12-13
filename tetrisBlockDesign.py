import pygame

pygame.init()
win = pygame.display.set_mode((500,500))
win.fill((0,0,0))

(0,204,204)
(0,230,230)
(1,255,255)

def main():
    run = True
    while run:

        pygame.display.update()
        drawBlock1()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

def drawBlock1():
    block1 = 200
    block2 = round(block1 - (15 * block1 / 100))
    block3 = 2*block2 - block1
    loc = 100
    loc3 = loc + (block1 - block2)
    pygame.draw.rect(win, ((0,204,204)), (loc,loc,block1,block1))
    pygame.draw.rect(win, ((1,255,255)), (loc,loc,block2,block2))
    pygame.draw.rect(win, ((0,230,230)), (loc3,loc3,block3,block3))

main()