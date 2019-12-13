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
    while run:
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pygame.draw.rect(win, (0,0,0), (x,y,blocksize,blocksize), fill=(170, 170, 170))


main()