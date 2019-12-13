import pygame

pygame.init()

win = pygame.display.set_mode((500,500))
win.fill((255,255,255))

class button():
    def __init__(self, color, x,y,width,height, text='', clicked=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.clicked = clicked

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


def redrawWindow():
    win.fill((255,255,255))
    if greenButton.clicked == False:
        greenButton.draw(win, (0,0,0))
    else:
        pygame.draw.rect(win, (0,0,0), (greenButton.x,greenButton.y,greenButton.width,greenButton.height),0)

run = True
greenButton = button((0,255,0), 150, 225, 250, 100)

while True:
    redrawWindow()
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if greenButton.isOver(pos) and greenButton.clicked == False:
                print('clicked')
                greenButton.clicked = True
                

        if event.type == pygame.MOUSEMOTION:
            if greenButton.isOver(pos):
                greenButton.color = (255,0,0)
            else:
                greenButton.color = (0,255,0)