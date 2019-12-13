import pygame

pygame.init()
win = pygame.display.set_mode((500,500))
win.fill((0,0,0))


def main():
    run = True
    color = (15, 155, 215)
    x = 100
    y = 100
    blocksize = 300
    fade = False
    while run:
        pygame.display.update()
        if fade == False:
            draw(color, x, y, blocksize)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                
                if (event.key == pygame.K_SPACE):
                    color = (15, 155, 215)
                elif (event.key == pygame.K_c):
                    fade = True
                    pygame.display.update()
                    for i in range(blocksize, 0, -1):
                        pass
                    draw((15, 155, 215), x, y, 200)
                        

                    fade = False
                    

def draw(color, x, y, blocksize):
    pygame.draw.rect(win, color, (x,y,blocksize,blocksize))


main()