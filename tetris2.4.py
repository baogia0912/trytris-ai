import random, time, pygame, sys
from pygame.locals import *
from pynput import keyboard 

FPS = 500 
WINDOWWIDTH = 1240
WINDOWHEIGHT = 600
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 40
PLAYBOARD = 20
BLANK = '.'

AUTOREPEATRATE = 0.01
DELAYAUTOSHIFT = 0.10
MOVEDOWNFREQ = 0
DELAYLOCKIN = 0.5

PUSHUPREQUIRED = 10
MAXABILITYCOUNT = 5

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2) 
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 80

ATTACKTABLE = (0,0,1,2,4,4,6,2,0,10,1) # (0lines,1lines,2lines,3lines,4lines,T Spin Double,T Spin Triple,T Spin Single,T Spin Mini, Perfect Clear, Back 2 Back)
COMBOTABLE = (0,0,1,1,1,2,2,3,3,4,4,4,5) # (0,1,2,3,4,5,6,7,8,9,10,11,12+)

#               R    G    B 
WHITE       = (255, 255, 255) 
GRAY1       = ( 12,  12,  12)
GRAY2       = ( 50,  50,  50)
GRAY3       = (106, 106, 106)
GRAY4       = (150, 150, 150)
GRAY5       = ( 34,  34,  34)
BLACK       = (  0,   0,   0) 
RED         = (215,  15,  54) # S-piece
GREEN       = ( 89, 177,   1) # Z-piece
BLUE        = ( 33,  65, 198) # J-piece
ORANGE      = (227,  91,   3) # L-piece
LIGHTBLUE   = ( 15, 155, 215) # I-piece
YELLOW      = (227, 159,   1) # O-piece
PINK        = (175,  40, 138) # T-piece
FROZEN      = (165, 242, 243)

S_RED         = (107,   9,  27) # S-piece
S_GREEN       = ( 45,  88,   6) # Z-piece
S_BLUE        = ( 17,  33,  99) # J-piece
S_ORANGE      = (113,  45,   6) # L-piece
S_LIGHTBLUE   = ( 10,  78, 107) # I-piece
S_YELLOW      = (113,  79,   8) # O-piece
S_PINK        = ( 87,  21,  69) # T-piece

RED1A       = (160,0,0)
RED1B       = (220,0,0)
RED1C       = (180,0,0)
GREEN1A     = (0,204,0)
GREEN1B     = (0,252,0)
GREEN1C     = (0,230,0)
BLUE1A      = (0,0,150)
BLUE1B      = (0,0,220)
BLUE1C      = (0,0,180)
ORANGE1A    = (179,70,0)
ORANGE1B    = (230,90,0)
ORANGE1C    = (204,80,0)
LIGHTBLUE1A = (0,204,204)
LIGHTBLUE1B = (0,255,255)
LIGHTBLUE1C = (0,230,230)
YELLOW1A    = (204,204,0)
YELLOW1B    = (230,230,0)
YELLOW1C    = (255,255,0)
PINK1A      = (204,0,204)
PINK1B      = (230,0,230)
PINK1C      = (255,0,255)

RED1        = (RED1A,RED1B,RED1C)
GREEN1      = (GREEN1A,GREEN1B,GREEN1C)
BLUE1       = (BLUE1A,BLUE1B,BLUE1C)
ORANGE1     = (ORANGE1A,ORANGE1B,ORANGE1C)
LIGHTBLUE1  = (LIGHTBLUE1A,LIGHTBLUE1B,LIGHTBLUE1C)
YELLOW1     = (YELLOW1A,YELLOW1B,YELLOW1C)
PINK1       = (PINK1A,PINK1B,PINK1C)

BORDERCOLOR     = GRAY2
BGCOLOR         = BLACK
TEXTCOLOR       = WHITE
COLORS          = (GREEN, RED, BLUE, ORANGE, LIGHTBLUE, YELLOW, PINK, S_GREEN, S_RED, S_BLUE, S_ORANGE, S_LIGHTBLUE, S_YELLOW, S_PINK, GRAY3, GRAY4, FROZEN)
GAMEOVERCOLOR   = GRAY3

TEMPLATEWIDTH   = 4
TEMPLATEHEIGHT  = 4

S_SHAPE_TEMPLATE = [['.OO.',
                     'OO..',
                     '....',
                     '....'],
                    ['.O..',
                     '.OO.',
                     '..O.',
                     '....'],
                    ['....',
                     '.OO.',
                     'OO..',
                     '....'],
                    ['O...',
                     'OO..',
                     '.O..',
                     '....']]

Z_SHAPE_TEMPLATE = [['OO..',
                     '.OO.',
                     '....',
                     '....'],
                    ['..O.',
                     '.OO.',
                     '.O..',
                     '....'],
                    ['....',
                     'OO..',
                     '.OO.',
                     '....'],
                    ['.O..',
                     'OO..',
                     'O...',
                     '....']]

I_SHAPE_TEMPLATE = [['....',
                     'OOOO',
                     '....',
                     '....'],
                    ['..O.',
                     '..O.',
                     '..O.',
                     '..O.'],
                    ['....',
                     '....',
                     'OOOO',
                     '....'],
                    ['.O..',
                     '.O..',
                     '.O..',
                     '.O..']]


O_SHAPE_TEMPLATE = [['.OO.',
                     '.OO.',
                     '....',
                     '....'],
                    ['.OO.',
                     '.OO.',
                     '....',
                     '....'],
                    ['.OO.',
                     '.OO.',
                     '....',
                     '....'],
                    ['.OO.',
                     '.OO.',
                     '....',
                     '....']]

J_SHAPE_TEMPLATE = [['O...',
                     'OOO.',
                     '....',
                     '....'],
                    ['.OO.',
                     '.O..',
                     '.O..',
                     '....'],
                    ['....',
                     'OOO.',
                     '..O.',
                     '....'],
                    ['.O..',
                     '.O..',
                     'OO..',
                     '....']]

L_SHAPE_TEMPLATE = [['..O.',
                     'OOO.',
                     '....',
                     '....'],
                    ['.O..',
                     '.O..',
                     '.OO.',
                     '....'],
                    ['....',
                     'OOO.',
                     'O...',
                     '....'],
                    ['OO..',
                     '.O..',
                     '.O..',
                     '....']]

T_SHAPE_TEMPLATE = [['.O..',
                     'OOO.',
                     '....',
                     '....'],
                    ['.O..',
                     '.OO.',
                     '.O..',
                     '....'],
                    ['....',
                     'OOO.',
                     '.O..',
                     '....'],
                    ['.O..',
                     'OO..',
                     '.O..',
                     '....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

PIECES_COLOR = {'S': 0,
                'Z': 1,
                'J': 2,
                'L': 3,
                'I': 4,
                'O': 5,
                'T': 6,
                'S_S': 7,
                'S_Z': 8,
                'S_J': 9,
                'S_L': 10,
                'S_I': 11,
                'S_O': 12,
                'S_T': 13,
                }

set1WallkickData = [(( 0, 0), (-1, 0), (-1, 1), ( 0,-2), (-1,-2)),
                    (( 0, 0), ( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)),
                    (( 0, 0), ( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)),
                    (( 0, 0), (-1, 0), (-1, 1), ( 0,-2), (-1,-2)),
                    (( 0, 0), ( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2)),
                    (( 0, 0), (-1, 0), (-1,-1), ( 0, 2), (-1, 2)),
                    (( 0, 0), (-1, 0), (-1,-1), ( 0, 2), (-1, 2)),
                    (( 0, 0), ( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2))]

set2WallkickData = [(( 0, 0), (-2, 0), ( 1, 0), (-2,-1), ( 1, 2)),
                    (( 0, 0), ( 2, 0), (-1, 0), ( 2, 1), (-1,-2)),
                    (( 0, 0), (-1, 0), ( 2, 0), (-1, 2), ( 2,-1)),
                    (( 0, 0), ( 1, 0), (-2, 0), ( 1,-2), (-2, 1)),
                    (( 0, 0), ( 2, 0), (-1, 0), ( 2, 1), (-1,-2)),
                    (( 0, 0), (-2, 0), ( 1, 0), (-2,-1), ( 1, 2)),
                    (( 0, 0), ( 1, 0), (-2, 0), ( 1,-2), (-2, 1)),
                    (( 0, 0), (-1, 0), ( 2, 0), (-1, 2), ( 2,-1))]


def main():
    global FPSCLOCK, DISPLAYSURF, SMALLFONT, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    SMALLFONT = pygame.font.Font('freesansbold.ttf', 14)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetris')

    showTextScreen('Tetris')
    while True: # game loop
        runGame2P()
        showTextScreen('Game Over')


def runGame2P():
    # setup variables for the start of the game
    global loseP1, loseP2, DISPLAYSURF, P1Frozen, P2Frozen
    boardP1 = getBlankBoard()
    boardP2 = getBlankBoard()
    lastMoveDownTimeP1 = time.time()
    lastMoveSidewaysTimeP1 = time.time()
    lastFallTimeP1 = time.time()
    loseP1 = False
    movingDownP1 = False # note: there is no movingUp variable
    movingLeftP1 = False
    movingRightP1 = False
    canHoldedP1 = True
    P1Tspin = False
    P2Tspin = False
    P1backToBack = False
    P2backToBack = False
    P1ComboCounter = 0
    P2ComboCounter = 0
    spinDirectionP1 = ''
    spinDirectionP2 = ''
    lastMoveDownTimeP2 = time.time()
    lastMoveSidewaysTimeP2 = time.time()
    lastFallTimeP2 = time.time()
    loseP2 = False
    movingDownP2 = False # note: there is no movingUp variable
    movingLeftP2 = False
    movingRightP2 = False
    canHoldedP2 = True
    P1LineRemoved = 0
    P2LineRemoved = 0
    P1PerfectClear = False
    P2PerfectClear = False
    P1backToBackPrint = False
    P2backToBackPrint = False
    P1Tetris = False
    P2Tetris = False
    P1Combo = False
    P2Combo = False
    P1TMini = False
    P2TMini = False
    P1TSingle = False
    P2TSingle = False
    P1TDouble = False
    P2TDouble = False
    P1TTriple = False
    P2TTriple = False
    P1Jspin = False
    P1Lspin = False
    P1Sspin = False
    P1Zspin = False
    P1Ispin = False
    P2Jspin = False
    P2Lspin = False
    P2Sspin = False
    P2Zspin = False
    P2Ispin = False
    P1Frozen = False
    P2Frozen = False
    freezeP1 = 0
    freezeP2 = 0
    freezeP1Timer = time.time()
    freezeP2Timer = time.time()

    P1Ability = {'Jspin':0,'Lspin':0,'Sspin':0,'Zspin':0,'Ispin':0,}
    P2Ability = {'Jspin':0,'Lspin':0,'Sspin':0,'Zspin':0,'Ispin':0,}

    garbageQueueForP1 = []
    garbageQueueForP2 = []

    transferQueueForP1 = []
    transferQueueForP2 = []

    lineSentToP1 = 0
    lineSentToP2 = 0

    fallFreq = 1
    bagP1 = list(PIECES.keys())
    bagP2 = list(PIECES.keys())

    fallingPieceP1 = getNewPieceP1(bagP1)
    bagP1.remove(fallingPieceP1['shape'])

    fallingPieceP2 = getNewPieceP2(bagP2)
    bagP2.remove(fallingPieceP2['shape'])

    nextPiece1P1 = getNewPieceP1(bagP1)
    bagP1.remove(nextPiece1P1['shape'])
    nextPiece2P1 = getNewPieceP1(bagP1)
    bagP1.remove(nextPiece2P1['shape'])
    nextPiece3P1 = getNewPieceP1(bagP1)
    bagP1.remove(nextPiece3P1['shape'])
    nextPiece4P1 = getNewPieceP1(bagP1)
    bagP1.remove(nextPiece4P1['shape'])
    nextPiece5P1 = getNewPieceP1(bagP1)
    bagP1.remove(nextPiece5P1['shape'])

    NEXT_PIECESP1 = [nextPiece1P1,nextPiece2P1,nextPiece3P1,nextPiece4P1,nextPiece5P1]
    holdPieceP1 = None

    nextPiece1P2 = getNewPieceP2(bagP2)
    bagP2.remove(nextPiece1P2['shape'])
    nextPiece2P2 = getNewPieceP2(bagP2)
    bagP2.remove(nextPiece2P2['shape'])
    nextPiece3P2 = getNewPieceP2(bagP2)
    bagP2.remove(nextPiece3P2['shape'])
    nextPiece4P2 = getNewPieceP2(bagP2)
    bagP2.remove(nextPiece4P2['shape'])
    nextPiece5P2 = getNewPieceP2(bagP2)
    bagP2.remove(nextPiece5P2['shape'])

    NEXT_PIECESP2 = [nextPiece1P2,nextPiece2P2,nextPiece3P2,nextPiece4P2,nextPiece5P2]
    holdPieceP2 = None

    while True: # game loop

        for playerAbility in (P1Ability, P2Ability):
            for ability, count in playerAbility.items():
                if count > MAXABILITYCOUNT:
                    playerAbility[ability] = MAXABILITYCOUNT

        if fallingPieceP1 == None:
            # No falling piece in play, so start a new piece at the top
            fallingPieceP1 = nextPiece1P1
            if len(bagP1) == 0:
                bagP1 = list(PIECES.keys())
            
            nextPiece1P1 = nextPiece2P1
            nextPiece2P1 = nextPiece3P1
            nextPiece3P1 = nextPiece4P1
            nextPiece4P1 = nextPiece5P1

            nextPiece5P1 = getNewPieceP1(bagP1)
            bagP1.remove(nextPiece5P1['shape'])
            NEXT_PIECESP1 = [nextPiece1P1,nextPiece2P1,nextPiece3P1,nextPiece4P1,nextPiece5P1]
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(boardP1, fallingPieceP1):
                fallingPieceP1['y'] = 18
                if not isValidPosition(boardP1, fallingPieceP1):
                    loseP1 = True
                    for x in range(BOARDWIDTH):
                        for y in range(BOARDHEIGHT):
                            drawBoxP1(x, y, boardP1[x][y])
                    drawHiddenBoardP1()
                    return # can't fit a new piece on the board, so game over

        if fallingPieceP2 == None:
            # No falling piece in play, so start a new piece at the top
            fallingPieceP2 = nextPiece1P2
            if len(bagP2) == 0:
                bagP2 = list(PIECES.keys())
            
            nextPiece1P2 = nextPiece2P2
            nextPiece2P2 = nextPiece3P2
            nextPiece3P2 = nextPiece4P2
            nextPiece4P2 = nextPiece5P2

            nextPiece5P2 = getNewPieceP2(bagP2)
            bagP2.remove(nextPiece5P2['shape'])
            NEXT_PIECESP2 = [nextPiece1P2,nextPiece2P2,nextPiece3P2,nextPiece4P2,nextPiece5P2]
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(boardP2, fallingPieceP2):
                fallingPieceP2['y'] = 18
                if not isValidPosition(boardP2, fallingPieceP2):
                    loseP2 = True
                    for x in range(BOARDWIDTH):
                        for y in range(BOARDHEIGHT):
                            drawBoxP2(x, y, boardP2[x][y])
                    drawHiddenBoardP2()
                    return # can't fit a new piece on the board, so game over


        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_TAB):
                    #quit the game
                    terminate()
                elif (event.key == K_f):
                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
                    DISPLAYSURF.fill(BGCOLOR)
                    showTextScreen('Paused') # pause until a key press
                    lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP1 = time.time()
                    lastMoveSidewaysTimeP1 = time.time()
                    lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP2 = time.time()
                    lastMoveSidewaysTimeP2 = time.time()
                elif (event.key == K_g):
                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
                    DISPLAYSURF.fill(BGCOLOR)
                    showTextScreen('Paused') # pause until a key press
                    lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP1 = time.time()
                    lastMoveSidewaysTimeP1 = time.time()
                    lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP2 = time.time()
                    lastMoveSidewaysTimeP2 = time.time()
                elif (event.key == K_r):
                    #reset the game
                    return
                elif (event.key == K_t):
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('/Users/bao/Desktop/python stuff/learning pygame/tetris/sound track/Fire.mp3'), maxtime = 1000)
                elif (event.key == K_h):
                    DISPLAYSURF.fill(BGCOLOR)
                    drawInstructions(WINDOWWIDTH/2 - 100, 200, WHITE)
                    titleSurf, titleRect = makeTextObjs('Instructions', BIGFONT, TEXTCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 200)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
                    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 200)
                    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

                    while checkForKeyPress() == None:
                        pygame.display.update()
                        FPSCLOCK.tick()
                elif (event.key == K_p):
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    showTextScreen('Paused') # pause until a key press
                    lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP1 = time.time()
                    lastMoveSidewaysTimeP1 = time.time()

                    lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP2 = time.time()
                    lastMoveSidewaysTimeP2 = time.time()

                elif (event.key == K_LEFT):
                    movingLeftP1 = False
                elif (event.key == K_RIGHT):
                    movingRightP1 = False
                elif (event.key == K_DOWN):
                    movingDownP1 = False
                elif (event.key == K_j):
                    movingLeftP2 = False
                elif (event.key == K_l):
                    movingRightP2 = False
                elif (event.key == K_k):
                    movingDownP2 = False

            if event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT) and fallingPieceP1 != None and not P1Frozen:
                    movingRightP1 = False
                    movingLeftP1 = True
                    if isValidPosition(boardP1, fallingPieceP1, adjX=-1):
                        fallingPieceP1['x'] -= 1
                        lastMoveSidewaysTimeP1 = time.time() + DELAYAUTOSHIFT
                        if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                            lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                        if fallingPieceP1['shape'] == 'J':
                            P1Jspin = False
                        if fallingPieceP1['shape'] == 'L':
                            P1Lspin = False
                        if fallingPieceP1['shape'] == 'S':
                            P1Sspin = False
                        if fallingPieceP1['shape'] == 'Z':
                            P1Zspin = False
                        if fallingPieceP1['shape'] == 'I':
                            P1Ispin = False

                elif (event.key == K_RIGHT) and fallingPieceP1 != None and not P1Frozen:
                    movingLeftP1 = False
                    movingRightP1 = True
                    if isValidPosition(boardP1, fallingPieceP1, adjX=1):
                        fallingPieceP1['x'] += 1
                        lastMoveSidewaysTimeP1 = time.time() + DELAYAUTOSHIFT
                        if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                            lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                        if fallingPieceP1['shape'] == 'J':
                            P1Jspin = False
                        if fallingPieceP1['shape'] == 'L':
                            P1Lspin = False
                        if fallingPieceP1['shape'] == 'S':
                            P1Sspin = False
                        if fallingPieceP1['shape'] == 'Z':
                            P1Zspin = False
                        if fallingPieceP1['shape'] == 'I':
                            P1Ispin = False
                    
                elif (event.key == K_j) and fallingPieceP2 != None and not P2Frozen:
                    movingRightP2 = False
                    movingLeftP2 = True
                    if isValidPosition(boardP2, fallingPieceP2, adjX=-1):
                        fallingPieceP2['x'] -= 1
                        lastMoveSidewaysTimeP2 = time.time() + DELAYAUTOSHIFT
                        if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                            lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                        if fallingPieceP2['shape'] == 'J':
                            P2Jspin = False
                        if fallingPieceP2['shape'] == 'L':
                            P2Lspin = False
                        if fallingPieceP2['shape'] == 'S':
                            P2Sspin = False
                        if fallingPieceP2['shape'] == 'Z':
                            P2Zspin = False
                        if fallingPieceP2['shape'] == 'I':
                            P2Ispin = False


                elif (event.key == K_l) and fallingPieceP2 != None and not P2Frozen:
                    movingLeftP2 = False
                    movingRightP2 = True
                    if isValidPosition(boardP2, fallingPieceP2, adjX=1):
                        fallingPieceP2['x'] += 1
                        lastMoveSidewaysTimeP2 = time.time() + DELAYAUTOSHIFT
                        if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                            lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                        if fallingPieceP2['shape'] == 'J':
                            P2Jspin = False
                        if fallingPieceP2['shape'] == 'L':
                            P2Lspin = False
                        if fallingPieceP2['shape'] == 'S':
                            P2Sspin = False
                        if fallingPieceP2['shape'] == 'Z':
                            P2Zspin = False
                        if fallingPieceP2['shape'] == 'I':
                            P2Ispin = False

                # hold a peice
                elif (event.key == K_e) and canHoldedP1 and fallingPieceP1 != None and not P1Frozen:
                    lastMoveSidewaysTimeP1 = time.time() + DELAYAUTOSHIFT
                    copyPieceP1 = holdPieceP1
                    holdPieceP1 = fallingPieceP1
                    fallingPieceP1 = copyPieceP1
                    holdPieceP1['x'] = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2) 
                    holdPieceP1['rotation'] = 0
                    canHoldedP1 = False
                    if fallingPieceP1 != None:
                        fallingPieceP1['y'] = 19
                        if not isValidPosition(boardP1, fallingPieceP1):
                            fallingPieceP1['y'] = 18
                    P1Tspin = False
                    P1Jspin = False 
                    P1Lspin = False
                    P1Sspin = False
                    P1Zspin = False
                    P1Ispin = False
                    
                elif (event.key == K_3) and canHoldedP2 and fallingPieceP2 != None and not P2Frozen:
                    lastMoveSidewaysTimeP2 = time.time() + DELAYAUTOSHIFT
                    copyPieceP2 = holdPieceP2
                    holdPieceP2 = fallingPieceP2
                    fallingPieceP2 = copyPieceP2
                    holdPieceP2['x'] = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2) 
                    holdPieceP2['rotation'] = 0
                    canHoldedP2 = False
                    if fallingPieceP2 != None:
                        fallingPieceP2['y'] = 19
                        if not isValidPosition(boardP2, fallingPieceP2):
                            fallingPieceP2['y'] = 18
                    P2Tspin = False
                    P2Jspin = False 
                    P2Lspin = False
                    P2Sspin = False
                    P2Zspin = False
                    P2Ispin = False

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP) and fallingPieceP1 != None and not P1Frozen:
                    P1Tspin = False
            
                    if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                        lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    spinDirectionP1 = 'CW'
                    fallingPieceP1['rotation'] = (fallingPieceP1['rotation'] + 1) % len(PIECES[fallingPieceP1['shape']])
                    if fallingPieceP1['shape'] == 'T':
                        if isValidPosition(boardP1, fallingPieceP1) and not isValidPosition(boardP1, fallingPieceP1, adjY=-1) and is3ConnerRule(boardP1, fallingPieceP1):
                            P1Tspin = True
                        elif not isValidPosition(boardP1, fallingPieceP1):
                            superRotationSystem(boardP1, fallingPieceP1, spinDirectionP1, P1Jspin, P1Lspin, P1Sspin, P1Zspin, P1Ispin)
                            if is3ConnerRule(boardP1, fallingPieceP1):
                                P1Tspin = True
                    elif isValidPosition(boardP1, fallingPieceP1):
                        if fallingPieceP1['shape'] == 'J':
                            P1Jspin = False
                        if fallingPieceP1['shape'] == 'L':
                            P1Lspin = False
                        if fallingPieceP1['shape'] == 'S':
                            P1Sspin = False
                        if fallingPieceP1['shape'] == 'Z':
                            P1Zspin = False
                        if fallingPieceP1['shape'] == 'I':
                            P1Ispin = False
                    else:
                        P1Jspin, P1Lspin, P1Sspin, P1Zspin, P1Ispin = superRotationSystem(boardP1, fallingPieceP1, spinDirectionP1, P1Jspin, P1Lspin, P1Sspin, P1Zspin, P1Ispin)
                    if isValidPosition(boardP1, fallingPieceP1, adjY=-1):
                        if fallingPieceP1['shape'] == 'J':
                            P1Jspin = False
                        if fallingPieceP1['shape'] == 'L':
                            P1Lspin = False
                        if fallingPieceP1['shape'] == 'S':
                            P1Sspin = False
                        if fallingPieceP1['shape'] == 'Z':
                            P1Zspin = False
                        if fallingPieceP1['shape'] == 'I':
                            P1Ispin = False
                elif (event.key == K_w) and fallingPieceP1 != None and not P1Frozen: # rotate the other direction
                    P1Tspin = False
                    
                    if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                        lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    spinDirectionP1 = 'CCW'
                    fallingPieceP1['rotation'] = (fallingPieceP1['rotation'] - 1) % len(PIECES[fallingPieceP1['shape']])
                    if fallingPieceP1['shape'] == 'T':
                        if isValidPosition(boardP1, fallingPieceP1) and not isValidPosition(boardP1, fallingPieceP1, adjY=-1) and is3ConnerRule(boardP1, fallingPieceP1):
                            P1Tspin = True
                        elif not isValidPosition(boardP1, fallingPieceP1):
                            superRotationSystem(boardP1, fallingPieceP1, spinDirectionP1, P1Jspin, P1Lspin, P1Sspin, P1Zspin, P1Ispin)
                            if is3ConnerRule(boardP1, fallingPieceP1):
                                P1Tspin = True
                    elif isValidPosition(boardP1, fallingPieceP1):
                        if fallingPieceP1['shape'] == 'J':
                            P1Jspin = False
                        if fallingPieceP1['shape'] == 'L':
                            P1Lspin = False
                        if fallingPieceP1['shape'] == 'S':
                            P1Sspin = False
                        if fallingPieceP1['shape'] == 'Z':
                            P1Zspin = False
                        if fallingPieceP1['shape'] == 'I':
                            P1Ispin = False
                    else:
                        P1Jspin, P1Lspin, P1Sspin, P1Zspin, P1Ispin = superRotationSystem(boardP1, fallingPieceP1, spinDirectionP1, P1Jspin, P1Lspin, P1Sspin, P1Zspin, P1Ispin)
                    if isValidPosition(boardP1, fallingPieceP1, adjY=-1):
                        if fallingPieceP1['shape'] == 'J':
                            P1Jspin = False
                        if fallingPieceP1['shape'] == 'L':
                            P1Lspin = False
                        if fallingPieceP1['shape'] == 'S':
                            P1Sspin = False
                        if fallingPieceP1['shape'] == 'Z':
                            P1Zspin = False
                        if fallingPieceP1['shape'] == 'I':
                            P1Ispin = False
                elif (event.key == K_q) and fallingPieceP1 != None and not P1Frozen: # rotate the other direction
                    if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                        lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    fallingPieceP1['rotation'] = (fallingPieceP1['rotation'] + 2) % len(PIECES[fallingPieceP1['shape']])
                    if not isValidPosition(boardP1, fallingPieceP1):
                        fallingPieceP1['rotation'] = (fallingPieceP1['rotation'] - 2) % len(PIECES[fallingPieceP1['shape']])
                    if isValidPosition(boardP1, fallingPieceP1) and not isValidPosition(boardP1, fallingPieceP1, adjY=-1):
                        if fallingPieceP1['shape'] == 'J':
                            P1Jspin = True
                        if fallingPieceP1['shape'] == 'L':
                            P1Lspin = True
                        if fallingPieceP1['shape'] == 'S':
                            P1Sspin = True
                        if fallingPieceP1['shape'] == 'Z':
                            P1Zspin = True
                        if fallingPieceP1['shape'] == 'I':
                            P1Ispin = True
                    else:
                        if fallingPieceP1['shape'] == 'J':
                            P1Jspin = False
                        if fallingPieceP1['shape'] == 'L':
                            P1Lspin = False
                        if fallingPieceP1['shape'] == 'S':
                            P1Sspin = False
                        if fallingPieceP1['shape'] == 'Z':
                            P1Zspin = False
                        if fallingPieceP1['shape'] == 'I':
                            P1Ispin = False

                elif (event.key == K_i) and fallingPieceP2 != None and not P2Frozen:
                    P2Tspin = False
                    
                    if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                        lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    spinDirectionP2 = 'CW'
                    fallingPieceP2['rotation'] = (fallingPieceP2['rotation'] + 1) % len(PIECES[fallingPieceP2['shape']])
                    if fallingPieceP2['shape'] == 'T':
                        if isValidPosition(boardP2, fallingPieceP2) and not isValidPosition(boardP2, fallingPieceP2, adjY=-1) and is3ConnerRule(boardP2, fallingPieceP2):
                            P2Tspin = True
                        elif not isValidPosition(boardP2, fallingPieceP2):
                            superRotationSystem(boardP2, fallingPieceP2, spinDirectionP2, P2Jspin, P2Lspin, P2Sspin, P2Zspin, P2Ispin)
                            if is3ConnerRule(boardP2, fallingPieceP2):
                                P2Tspin = True
                    elif isValidPosition(boardP2, fallingPieceP2):
                        if fallingPieceP2['shape'] == 'J':
                            P2Jspin = False
                        if fallingPieceP2['shape'] == 'L':
                            P2Lspin = False
                        if fallingPieceP2['shape'] == 'S':
                            P2Sspin = False
                        if fallingPieceP2['shape'] == 'Z':
                            P2Zspin = False
                        if fallingPieceP2['shape'] == 'I':
                            P2Ispin = False
                    else:
                        P2Jspin, P2Lspin, P2Sspin, P2Zspin, P2Ispin = superRotationSystem(boardP2, fallingPieceP2, spinDirectionP2, P2Jspin, P2Lspin, P2Sspin, P2Zspin, P2Ispin)
                    if isValidPosition(boardP2, fallingPieceP2, adjY=-1):
                        if fallingPieceP2['shape'] == 'J':
                            P2Jspin = False
                        if fallingPieceP2['shape'] == 'L':
                            P2Lspin = False
                        if fallingPieceP2['shape'] == 'S':
                            P2Sspin = False
                        if fallingPieceP2['shape'] == 'Z':
                            P2Zspin = False
                        if fallingPieceP2['shape'] == 'I':
                            P2Ispin = False
                elif (event.key == K_2) and fallingPieceP2 != None and not P2Frozen: # rotate the other direction
                    P2Tspin = False
                    
                    if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                        lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    spinDirectionP2 = 'CCW'
                    fallingPieceP2['rotation'] = (fallingPieceP2['rotation'] - 1) % len(PIECES[fallingPieceP2['shape']])
                    if fallingPieceP2['shape'] == 'T':
                        if isValidPosition(boardP2, fallingPieceP2) and not isValidPosition(boardP2, fallingPieceP2, adjY=-1) and is3ConnerRule(boardP2, fallingPieceP2):
                            P2Tspin = True
                        elif not isValidPosition(boardP2, fallingPieceP2):
                            superRotationSystem(boardP2, fallingPieceP2, spinDirectionP2, P2Jspin, P2Lspin, P2Sspin, P2Zspin, P2Ispin)
                            if is3ConnerRule(boardP2, fallingPieceP2):
                                P2Tspin = True
                    elif isValidPosition(boardP2, fallingPieceP2):
                        if fallingPieceP2['shape'] == 'J':
                            P2Jspin = False
                        if fallingPieceP2['shape'] == 'L':
                            P2Lspin = False
                        if fallingPieceP2['shape'] == 'S':
                            P2Sspin = False
                        if fallingPieceP2['shape'] == 'Z':
                            P2Zspin = False
                        if fallingPieceP2['shape'] == 'I':
                            P2Ispin = False
                    else:
                        P2Jspin, P2Lspin, P2Sspin, P2Zspin, P2Ispin = superRotationSystem(boardP2, fallingPieceP2, spinDirectionP2, P2Jspin, P2Lspin, P2Sspin, P2Zspin, P2Ispin)
                    if isValidPosition(boardP2, fallingPieceP2, adjY=-1):
                        if fallingPieceP2['shape'] == 'J':
                            P2Jspin = False
                        if fallingPieceP2['shape'] == 'L':
                            P2Lspin = False
                        if fallingPieceP2['shape'] == 'S':
                            P2Sspin = False
                        if fallingPieceP2['shape'] == 'Z':
                            P2Zspin = False
                        if fallingPieceP2['shape'] == 'I':
                            P2Ispin = False
                elif (event.key == K_1) and fallingPieceP2 != None and not P2Frozen: # rotate the other direction
                    if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                        lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    fallingPieceP2['rotation'] = (fallingPieceP2['rotation'] + 2) % len(PIECES[fallingPieceP2['shape']])
                    if not isValidPosition(boardP2, fallingPieceP2):
                        fallingPieceP2['rotation'] = (fallingPieceP2['rotation'] - 2) % len(PIECES[fallingPieceP2['shape']])
                    if isValidPosition(boardP2, fallingPieceP2) and not isValidPosition(boardP2, fallingPieceP2, adjY=-1):
                        if fallingPieceP2['shape'] == 'J':
                            P2Jspin = True
                        if fallingPieceP2['shape'] == 'L':
                            P2Lspin = True
                        if fallingPieceP2['shape'] == 'S':
                            P2Sspin = True
                        if fallingPieceP2['shape'] == 'Z':
                            P2Zspin = True
                        if fallingPieceP2['shape'] == 'I':
                            P2Ispin = True
                    else:
                        if fallingPieceP2['shape'] == 'J':
                            P2Jspin = False
                        if fallingPieceP2['shape'] == 'L':
                            P2Lspin = False
                        if fallingPieceP2['shape'] == 'S':
                            P2Sspin = False
                        if fallingPieceP2['shape'] == 'Z':
                            P2Zspin = False
                        if fallingPieceP2['shape'] == 'I':
                            P2Ispin = False


                # making the piece fall faster with the down key
                elif (event.key == K_DOWN) and fallingPieceP1 != None and not P1Frozen:
                    movingDownP1 = True
                    if isValidPosition(boardP1, fallingPieceP1, adjY=2):
                        fallingPieceP1['y'] += 2
                    elif isValidPosition(boardP1, fallingPieceP1, adjY=1):
                        fallingPieceP1['y'] += 1
                    lastMoveDownTimeP1 = time.time()

                elif (event.key == K_k) and fallingPieceP2 != None and not P2Frozen:
                    movingDownP2 = True
                    if isValidPosition(boardP2, fallingPieceP2, adjY=2):
                        fallingPieceP2['y'] += 2
                    elif isValidPosition(boardP2, fallingPieceP2, adjY=1):
                        fallingPieceP2['y'] += 1
                    lastMoveDownTimeP2 = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE and fallingPieceP1 != None and not P1Frozen:
                    while isValidPosition(boardP1, fallingPieceP1, adjY=1):
                        fallingPieceP1['y'] += 1
                    addToBoard(boardP1, fallingPieceP1)
                    lineSentToP2, P1backToBack, P1ComboCounter, P1LineRemoved, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple = sendLineFromP1(boardP1, removeCompleteLines(boardP1), P1Tspin, P1backToBack, P1ComboCounter, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple)
                    if P1LineRemoved == 0:
                        for line in garbageQueueForP1:
                            reciveGarbage2P(boardP1, line)
                        garbageQueueForP1 = []
                        garbageTransferTo(boardP1, transferQueueForP1)
                        transferQueueForP1 = []
                    else:
                        if P1Sspin:
                            P1Ability['Sspin'] += P1LineRemoved
                        if P1Zspin:
                            P1Ability['Zspin'] += P1LineRemoved
                        if P1Lspin:
                            P1Ability['Lspin'] += P1LineRemoved
                        if P1Jspin:
                            P1Ability['Jspin'] += P1LineRemoved
                        if P1Ispin:
                            P1Ability['Ispin'] += P1LineRemoved
                        while lineSentToP2 > 0 and garbageQueueForP1 != []:
                            for line in garbageQueueForP1:
                                if lineSentToP2 >= line:
                                    lineSentToP2 -= line
                                    garbageQueueForP1.pop(0)
                                elif lineSentToP2 < line:
                                    garbageQueueForP1[0] -= lineSentToP2
                                    lineSentToP2 = 0
                        if lineSentToP2 > 0:
                            garbageQueueForP2.append(lineSentToP2)
                    P1Tspin = False
                    P1Jspin = False 
                    P1Lspin = False
                    P1Sspin = False
                    P1Zspin = False
                    P1Ispin = False
                    canHoldedP1 = True
                    if P1PerfectClear:
                        P1PCTimer = time.time()
                    if P1backToBackPrint:
                        P1B2BTimer = time.time()
                    if P1Tetris:
                        P1TetrisTimer = time.time()
                    if P1Combo:
                        P1ComboTimer = time.time()
                    if P1TMini:
                        P1TMiniTimer = time.time()
                    if P1TSingle:
                        P1TSingleTimer = time.time()
                    if P1TDouble:
                        P1TDoubleTimer = time.time()
                    if P1TTriple:
                        P1TTripleTimer = time.time()

                    fallingPieceP1 = nextPiece1P1
                    if len(bagP1) == 0:
                        bagP1 = list(PIECES.keys())
                    
                    nextPiece1P1 = nextPiece2P1
                    nextPiece2P1 = nextPiece3P1
                    nextPiece3P1 = nextPiece4P1
                    nextPiece4P1 = nextPiece5P1
                    nextPiece5P1 = getNewPieceP1(bagP1)
                    bagP1.remove(nextPiece5P1['shape'])

                    NEXT_PIECESP1 = [nextPiece1P1,nextPiece2P1,nextPiece3P1,nextPiece4P1,nextPiece5P1]
                    lastFallTimeP1 = time.time() # reset lastFallTime

                    if not isValidPosition(boardP1, fallingPieceP1):
                        fallingPieceP1['y'] = 18
                        if not isValidPosition(boardP1, fallingPieceP1):
                            loseP1 = True
                            for x in range(BOARDWIDTH):
                                for y in range(BOARDHEIGHT):
                                    drawBoxP1(x, y, boardP1[x][y])
                            drawHiddenBoardP1()
                            return # can't fit a new piece on the board, so game over

                elif event.key == K_v and fallingPieceP2 != None and not P2Frozen:
                    while isValidPosition(boardP2, fallingPieceP2, adjY=1):
                        fallingPieceP2['y'] += 1
                    addToBoard(boardP2, fallingPieceP2)
                    lineSentToP1, P2backToBack, P2ComboCounter, P2LineRemoved, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple = sendLineFromP2(boardP2, removeCompleteLines(boardP2), P2Tspin, P2backToBack, P2ComboCounter, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple)
                    if P2LineRemoved == 0:
                        for line in garbageQueueForP2:
                            reciveGarbage2P(boardP2, line)
                        garbageQueueForP2 = []
                        garbageTransferTo(boardP2, transferQueueForP2)
                        transferQueueForP2 = []
                    else:
                        if P2Sspin:
                            P2Ability['Sspin'] += P2LineRemoved
                        if P2Zspin:
                            P2Ability['Zspin'] += P2LineRemoved
                        if P2Lspin:
                            P2Ability['Lspin'] += P2LineRemoved
                        if P2Jspin:
                            P2Ability['Jspin'] += P2LineRemoved
                        if P2Ispin:
                            P2Ability['Ispin'] += P2LineRemoved
                        while lineSentToP1 > 0 and garbageQueueForP2 != []:
                            for line in garbageQueueForP2:
                                if lineSentToP1 >= line:
                                    lineSentToP1 -= line
                                    garbageQueueForP2.pop(0)
                                elif lineSentToP1 < line:
                                    garbageQueueForP2[0] -= lineSentToP1
                                    lineSentToP1 = 0
                        if lineSentToP1 > 0:
                            garbageQueueForP1.append(lineSentToP1)
                    P2Tspin = False
                    P2Jspin = False 
                    P2Lspin = False
                    P2Sspin = False
                    P2Zspin = False
                    P2Ispin = False
                    canHoldedP2 = True
                    if P2PerfectClear:
                        P2PCTimer = time.time()
                    if P2backToBackPrint:
                        P2B2BTimer = time.time()
                    if P2Tetris:
                        P2TetrisTimer = time.time()
                    if P2Combo:
                        P2ComboTimer = time.time()
                    if P2TMini:
                        P2TMiniTimer = time.time()
                    if P2TSingle:
                        P2TSingleTimer = time.time()
                    if P2TDouble:
                        P2TDoubleTimer = time.time()
                    if P2TTriple:
                        P2TTripleTimer = time.time()

                    fallingPieceP2 = nextPiece1P2
                    if len(bagP2) == 0:
                        bagP2 = list(PIECES.keys())
                    
                    nextPiece1P2 = nextPiece2P2
                    nextPiece2P2 = nextPiece3P2
                    nextPiece3P2 = nextPiece4P2
                    nextPiece4P2 = nextPiece5P2
                    nextPiece5P2 = getNewPieceP2(bagP2)
                    bagP2.remove(nextPiece5P2['shape'])

                    NEXT_PIECESP2 = [nextPiece1P2,nextPiece2P2,nextPiece3P2,nextPiece4P2,nextPiece5P2]
                    lastFallTimeP2 = time.time() # reset lastFallTime

                    if not isValidPosition(boardP2, fallingPieceP2):
                        fallingPieceP2['y'] = 18
                        if not isValidPosition(boardP2, fallingPieceP2):
                            loseP2 = True
                            for x in range(BOARDWIDTH):
                                for y in range(BOARDHEIGHT):
                                    drawBoxP2(x, y, boardP2[x][y])
                            drawHiddenBoardP2()
                            return # can't fit a new piece on the board, so game over 


                elif event.key == K_a and fallingPieceP1 != None and P1Ability['Jspin'] > 0 and not P1Frozen:
                    burnGarbage(boardP1, 1)
                    P1Ability['Jspin'] -= 1
                elif event.key == K_s and fallingPieceP1 != None and P1Ability['Lspin'] > 0 and not P1Frozen:
                    freezeP2 = 1
                    freezeP2Timer = time.time()
                    P1Ability['Lspin'] -= 1
                elif event.key == K_d and fallingPieceP1 != None and P1Ability['Sspin'] > 0 and not P1Frozen:
                    mixUpTop(boardP2, P1Ability['Sspin'])
                    P1Ability['Sspin'] = 0
                elif event.key == K_z and fallingPieceP1 != None and P1Ability['Zspin'] > 0 and not P1Frozen:
                    mixUpBottom(boardP2, P1Ability['Zspin'])
                    P1Ability['Zspin'] = 0
                elif event.key == K_x and fallingPieceP1 != None and P1Ability['Ispin'] > 0 and not P1Frozen:
                    if transferQueueForP2 == []:
                        transferQueueForP2 = garbageTransferFrom(boardP1, P1LineRemoved)
                    else:
                        lineTransferForP2 = garbageTransferFrom(boardP1, P1LineRemoved)
                        for x in range(BOARDWIDTH):
                            transferQueueForP2[x] += lineTransferForP2[x]
                    P1Ability['Ispin'] -= 1


                elif event.key == K_4 and fallingPieceP2 != None and P2Ability['Jspin'] > 0 and not P2Frozen:
                    burnGarbage(boardP2, 1)
                    P2Ability['Jspin'] -= 1
                elif event.key == K_5 and fallingPieceP2 != None and P2Ability['Lspin'] > 0 and not P2Frozen:
                    freezeP1 = 1
                    freezeP1Timer = time.time()
                    P2Ability['Lspin'] -= 1
                elif event.key == K_6 and fallingPieceP2 != None and P2Ability['Sspin'] > 0 and not P2Frozen:
                    mixUpTop(boardP1, P2Ability['Sspin'])
                    P2Ability['Sspin'] = 0
                elif event.key == K_7 and fallingPieceP2 != None and P2Ability['Zspin'] > 0 and not P2Frozen:
                    mixUpBottom(boardP1, P2Ability['Zspin'])
                    P2Ability['Zspin'] = 0
                elif event.key == K_8 and fallingPieceP2 != None and P2Ability['Ispin'] > 0 and not P2Frozen:
                    if transferQueueForP1 == []:
                        transferQueueForP1 = garbageTransferFrom(boardP2, P2LineRemoved)
                    else:
                        lineTransferForP1 = garbageTransferFrom(boardP2, P2LineRemoved)
                        for x in range(BOARDWIDTH):
                            transferQueueForP1[x] += lineTransferForP1[x]
                    P2Ability['Ispin'] -= 1
                

        # handle moving the piece because of user input
        if (movingLeftP1 or movingRightP1) and time.time() - lastMoveSidewaysTimeP1 > AUTOREPEATRATE and fallingPieceP1 != None and not P1Frozen:
            if movingLeftP1 and isValidPosition(boardP1, fallingPieceP1, adjX=-1):
                fallingPieceP1['x'] -= 1
            elif movingRightP1 and isValidPosition(boardP1, fallingPieceP1, adjX=1):
                fallingPieceP1['x'] += 1
            lastMoveSidewaysTimeP1 = time.time()
        
        if (movingLeftP2 or movingRightP2) and time.time() - lastMoveSidewaysTimeP2 > AUTOREPEATRATE and fallingPieceP2 != None and not P2Frozen:
            if movingLeftP2 and isValidPosition(boardP2, fallingPieceP2, adjX=-1):
                fallingPieceP2['x'] -= 1
            elif movingRightP2 and isValidPosition(boardP2, fallingPieceP2, adjX=1):
                fallingPieceP2['x'] += 1
            lastMoveSidewaysTimeP2 = time.time()

        if movingDownP1 and time.time() - lastMoveDownTimeP1 > MOVEDOWNFREQ and fallingPieceP1 != None and fallingPieceP1 != None and not P1Frozen:
            if isValidPosition(boardP1, fallingPieceP1, adjY=2) and isValidPosition(boardP1, fallingPieceP1, adjY=1):
                fallingPieceP1['y'] += 2
                lastMoveDownTimeP1 = time.time()
                lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
            elif isValidPosition(boardP1, fallingPieceP1, adjY=1):
                fallingPieceP1['y'] += 1
                lastMoveDownTimeP1 = time.time()
                lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq

        if movingDownP2 and time.time() - lastMoveDownTimeP2 > MOVEDOWNFREQ and fallingPieceP2 != None and fallingPieceP2 != None and not P2Frozen:
            if isValidPosition(boardP2, fallingPieceP2, adjY=2) and isValidPosition(boardP2, fallingPieceP2, adjY=1):
                fallingPieceP2['y'] += 2
                lastMoveDownTimeP2 = time.time()
                lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
            elif isValidPosition(boardP2, fallingPieceP2, adjY=1):
                fallingPieceP2['y'] += 1
                lastMoveDownTimeP2 = time.time()
                lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq

        # let the piece fall if it is time to fall
        if time.time() - lastFallTimeP1 > fallFreq:
            # see if the piece has landed
            if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(boardP1, fallingPieceP1)
                lineSentToP2, P1backToBack, P1ComboCounter, P1LineRemoved, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple = sendLineFromP1(boardP1, removeCompleteLines(boardP1), P1Tspin, P1backToBack, P1ComboCounter, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple)
                if P1LineRemoved == 0:
                    for line in garbageQueueForP1:
                        reciveGarbage2P(boardP1, line)
                    garbageQueueForP1 = []
                    garbageTransferTo(boardP1, transferQueueForP1)
                    transferQueueForP1 = []
                else:
                    if P1Sspin:
                        P1Ability['Sspin'] += P1LineRemoved
                    if P1Zspin:
                        P1Ability['Zspin'] += P1LineRemoved
                    if P1Lspin:
                        P1Ability['Lspin'] += P1LineRemoved
                    if P1Jspin:
                        P1Ability['Jspin'] += P1LineRemoved
                    if P1Ispin:
                        P1Ability['Ispin'] += P1LineRemoved
                    while lineSentToP2 > 0 and garbageQueueForP1 != []:
                        for line in garbageQueueForP1:
                            if lineSentToP2 >= line:
                                lineSentToP2 -= line
                                garbageQueueForP1.pop(0)
                            elif lineSentToP2 < line:
                                garbageQueueForP1[0] -= lineSentToP2
                                lineSentToP2 = 0
                    if lineSentToP2 > 0:
                        garbageQueueForP2.append(lineSentToP2)
                P1Tspin = False
                P1Jspin = False 
                P1Lspin = False
                P1Sspin = False
                P1Zspin = False
                P1Ispin = False
                canHoldedP1 = True
                if P1PerfectClear:
                    P1PCTimer = time.time()
                if P1backToBackPrint:
                    P1B2BTimer = time.time()
                if P1Tetris:
                    P1TetrisTimer = time.time()
                if P1Combo:
                    P1ComboTimer = time.time()
                if P1TMini:
                    P1TMiniTimer = time.time()
                if P1TSingle:
                    P1TSingleTimer = time.time()
                if P1TDouble:
                    P1TDoubleTimer = time.time()
                if P1TTriple:
                    P1TTripleTimer = time.time()
            
                # No falling piece in play, so start a new piece at the top
                fallingPieceP1 = nextPiece1P1
                if len(bagP1) == 0:
                    bagP1 = list(PIECES.keys())
                
                nextPiece1P1 = nextPiece2P1
                nextPiece2P1 = nextPiece3P1
                nextPiece3P1 = nextPiece4P1
                nextPiece4P1 = nextPiece5P1

                nextPiece5P1 = getNewPieceP1(bagP1)
                bagP1.remove(nextPiece5P1['shape'])
                NEXT_PIECESP1 = [nextPiece1P1,nextPiece2P1,nextPiece3P1,nextPiece4P1,nextPiece5P1]
                lastFallTime = time.time() # reset lastFallTime

                if not isValidPosition(boardP1, fallingPieceP1):
                    fallingPieceP1['y'] = 18
                    if not isValidPosition(boardP1, fallingPieceP1):
                        loseP1 = True
                        for x in range(BOARDWIDTH):
                            for y in range(BOARDHEIGHT):
                                drawBoxP1(x, y, boardP1[x][y])
                        drawHiddenBoardP1()
                        return # can't fit a new piece on the board, so game over
            else:
                # piece did not land, just move the piece down
                fallingPieceP1['y'] += 1
                if fallingPieceP1['shape'] == 'J':
                    P1Jspin = False
                if fallingPieceP1['shape'] == 'L':
                    P1Lspin = False
                if fallingPieceP1['shape'] == 'S':
                    P1Sspin = False
                if fallingPieceP1['shape'] == 'Z':
                    P1Zspin = False
                if fallingPieceP1['shape'] == 'I':
                    P1Ispin = False
                lastFallTimeP1 = time.time()

        if time.time() - lastFallTimeP2 > fallFreq:
            # see if the piece has landed
            if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(boardP2, fallingPieceP2)
                lineSentToP1, P2backToBack, P2ComboCounter, P2LineRemoved, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple = sendLineFromP2(boardP2, removeCompleteLines(boardP2), P2Tspin, P2backToBack, P2ComboCounter, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple)
                if P2LineRemoved == 0:
                    for line in garbageQueueForP2:
                        reciveGarbage2P(boardP2, line)
                    garbageQueueForP2 = []
                    garbageTransferTo(boardP2, transferQueueForP2)
                    transferQueueForP2 = []
                else:
                    if P2Sspin:
                        P2Ability['Sspin'] += P2LineRemoved
                    if P2Zspin:
                        P2Ability['Zspin'] += P2LineRemoved
                    if P2Lspin:
                        P2Ability['Lspin'] += P2LineRemoved
                    if P2Jspin:
                        P2Ability['Jspin'] += P2LineRemoved
                    if P2Ispin:
                        P2Ability['Ispin'] += P2LineRemoved
                    while lineSentToP1 > 0 and garbageQueueForP2 != []:
                        for line in garbageQueueForP2:
                            if lineSentToP1 >= line:
                                lineSentToP1 -= line
                                garbageQueueForP2.pop(0)
                            elif lineSentToP1 < line:
                                garbageQueueForP2[0] -= lineSentToP1
                                lineSentToP1 = 0
                    if lineSentToP1 > 0:
                        garbageQueueForP1.append(lineSentToP1)
                P2Tspin = False
                P2Jspin = False 
                P2Lspin = False
                P2Sspin = False
                P2Zspin = False
                P2Ispin = False
                canHoldedP2 = True
                if P2PerfectClear:
                    P2PCTimer = time.time()
                if P2backToBackPrint:
                    P2B2BTimer = time.time()
                if P2Tetris:
                    P2TetrisTimer = time.time()
                if P2Combo:
                    P2ComboTimer = time.time()
                if P2TMini:
                    P2TMiniTimer = time.time()
                if P2TSingle:
                    P2TSingleTimer = time.time()
                if P2TDouble:
                    P2TDoubleTimer = time.time()
                if P2TTriple:
                    P2TTripleTimer = time.time()

                # No falling piece in play, so start a new piece at the top
                fallingPieceP2 = nextPiece1P2
                if len(bagP2) == 0:
                    bagP2 = list(PIECES.keys())
                
                nextPiece1P2 = nextPiece2P2
                nextPiece2P2 = nextPiece3P2
                nextPiece3P2 = nextPiece4P2
                nextPiece4P2 = nextPiece5P2

                nextPiece5P2 = getNewPieceP2(bagP2)
                bagP2.remove(nextPiece5P2['shape'])
                NEXT_PIECESP2 = [nextPiece1P2,nextPiece2P2,nextPiece3P2,nextPiece4P2,nextPiece5P2]
                lastFallTime = time.time() # reset lastFallTime

                if not isValidPosition(boardP2, fallingPieceP2):
                    fallingPieceP2['y'] = 18
                    if not isValidPosition(boardP2, fallingPieceP2):
                        loseP2 = True
                        for x in range(BOARDWIDTH):
                            for y in range(BOARDHEIGHT):
                                drawBoxP2(x, y, boardP2[x][y])
                        drawHiddenBoardP2()
                        return # can't fit a new piece on the board, so game over
            else:
                # piece did not land, just move the piece down
                fallingPieceP2['y'] += 1
                if fallingPieceP2['shape'] == 'J':
                    P2Jspin = False
                if fallingPieceP2['shape'] == 'L':
                    P2Lspin = False
                if fallingPieceP2['shape'] == 'S':
                    P2Sspin = False
                if fallingPieceP2['shape'] == 'Z':
                    P2Zspin = False
                if fallingPieceP2['shape'] == 'I':
                    P2Ispin = False
                lastFallTimeP2 = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoardP1(boardP1)
        drawBoardP2(boardP2)
        drawNextPieceP1(NEXT_PIECESP1)
        drawHoldPieceP1(holdPieceP1)
        drawNextPieceP2(NEXT_PIECESP2)
        drawHoldPieceP2(holdPieceP2)
        drawText2P('Press h for help', 20, 20, WHITE)
        if fallingPieceP1 != None:
            drawPieceP1(GhostPiece(fallingPieceP1, boardP1))
            drawPieceP1(fallingPieceP1)
        if fallingPieceP2 != None:
            drawPieceP2(GhostPiece(fallingPieceP2, boardP2))
            drawPieceP2(fallingPieceP2)
        drawAleartBarP1(sum(garbageQueueForP1))
        drawAleartBarP2(sum(garbageQueueForP2))
        drawHiddenBoardP1()
        drawHiddenBoardP2()

        if P1Tspin:
            drawText2P('T-Spin: ' + str(P1Tspin),20,200, BLUE)
        else:
            drawText2P('T-Spin: ' + str(P1Tspin),20,200, WHITE)

        if P1Lspin:
            drawText2P('L-Spin: ' + str(P1Lspin),20,220, BLUE)
        else:
            drawText2P('L-Spin: ' + str(P1Lspin),20,220, WHITE)
        
        if P1Jspin:
            drawText2P('J-Spin: ' + str(P1Jspin),20,240, BLUE)
        else:
            drawText2P('J-Spin: ' + str(P1Jspin),20,240, WHITE)
            
        if P1Sspin:
            drawText2P('S-Spin: ' + str(P1Sspin),20,260, BLUE)
        else:
            drawText2P('S-Spin: ' + str(P1Sspin),20,260, WHITE)
            
        if P1Zspin:
            drawText2P('Z-Spin: ' + str(P1Zspin),20,280, BLUE)
        else:
            drawText2P('Z-Spin: ' + str(P1Zspin),20,280, WHITE)
            
        if P1Ispin:
            drawText2P('I-Spin: ' + str(P1Ispin),20,300, BLUE)
        else:    
            drawText2P('I-Spin: ' + str(P1Ispin),20,300, WHITE)

        if P2Tspin:
            drawText2P('T-Spin: ' + str(P2Tspin),620,200, BLUE)
        else:
            drawText2P('T-Spin: ' + str(P2Tspin),620,200, WHITE)
            
        if P2Jspin:
            drawText2P('J-Spin: ' + str(P2Jspin),620,220, BLUE)
        else:    
            drawText2P('J-Spin: ' + str(P2Jspin),620,220, WHITE)
            
        if P2Lspin:
            drawText2P('L-Spin: ' + str(P2Lspin),620,240, BLUE)
        else:    
            drawText2P('L-Spin: ' + str(P2Lspin),620,240, WHITE)
            
        if P2Sspin:
            drawText2P('S-Spin: ' + str(P2Sspin),620,260, BLUE)
        else:    
            drawText2P('S-Spin: ' + str(P2Sspin),620,260, WHITE)
            
        if P2Zspin:
            drawText2P('Z-Spin: ' + str(P2Zspin),620,280, BLUE)
        else:   
            drawText2P('Z-Spin: ' + str(P2Zspin),620,280, WHITE)
            
        if P2Ispin:
            drawText2P('I-Spin: ' + str(P2Ispin),620,300, BLUE)
        else:    
            drawText2P('I-Spin: ' + str(P2Ispin),620,300, WHITE)

        drawSpecialMove(60, 300, P1ComboCounter, P1Tspin, P1backToBackPrint, boardP1, P1Tetris, P1PerfectClear, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple)
        drawSpecialMove(660, 300, P2ComboCounter, P2Tspin, P2backToBackPrint, boardP2, P2Tetris, P2PerfectClear, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple)
        
        if time.time() - freezeP1Timer < freezeP1:
            P1Frozen = True
        else:
            P1Frozen = False

        if time.time() - freezeP2Timer < freezeP2:
            P2Frozen = True
        else:
            P2Frozen = False

        if P1PerfectClear:
            if time.time() - P1PCTimer > 1:
                P1PerfectClear = False

        if P2PerfectClear:
            if time.time() - P2PCTimer > 1:
                P2PerfectClear = False

        if P1backToBackPrint:
            if time.time() - P1B2BTimer > 1:
                P1backToBackPrint = False

        if P2backToBackPrint:
            if time.time() - P2B2BTimer > 1:
                P2backToBackPrint = False

        if P1Tetris:
            if time.time() - P1TetrisTimer > 1:
                P1Tetris = False

        if P2Tetris:
            if time.time() - P2TetrisTimer > 1:
                P2Tetris = False

        if P1Combo:
            if time.time() - P1ComboTimer > 1:
                P1Combo = False

        if P2Combo:
            if time.time() - P2ComboTimer > 1:
                P2Combo = False

        if P1TMini:
            if time.time() - P1TMiniTimer > 1:
                P1TMini = False

        if P2TMini:
            if time.time() - P2TMiniTimer > 1:
                P2TMini = False

        if P1TSingle:
            if time.time() - P1TSingleTimer > 1:
                P1TSingle = False

        if P2TSingle:
            if time.time() - P2TSingleTimer > 1:
                P2TSingle = False

        if P1TDouble:
            if time.time() - P1TDoubleTimer > 1:
                P1TDouble = False

        if P2TDouble:
            if time.time() - P2TDoubleTimer > 1:
                P2TDouble = False

        if P1TTriple:
            if time.time() - P1TTripleTimer > 1:
                P1TTriple = False

        if P2TTriple:
            if time.time() - P2TTripleTimer > 1:
                P2TTriple = False

        drawAbility(P1Ability, 20, 400)
        drawAbility(P2Ability, 620, 400)
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def getNewPieceP1(bag):
    # return a random new piece in a random rotation and color
    if len(bag) == 0:
        bag = list(PIECES.keys())
    shape = bag[random.randrange(len(bag))]
    newPiece = {'shape': shape,
                'rotation': 0,
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': 19, # start it above the board (i.e. less than 0)
                'color': PIECES_COLOR[shape]}
    return newPiece


def getNewPieceP2(bag):
    # return a random new piece in a random rotation and color
    if len(bag) == 0:
        bag = list(PIECES.keys())
    shape = bag[random.randrange(len(bag))]
    newPiece = {'shape': shape,
                'rotation': 0,
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': 19, # start it above the board (i.e. less than 0)
                'color': PIECES_COLOR[shape]}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if piece!=None and PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * (BOARDHEIGHT))
    return board

 
def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT
 

def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    if piece == None:
        return False
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True


def is3ConnerRule(board, piece, adjX=0, adjY=0):
    count = 0 
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if ((x==0 and y==0) or (x==0 and y==2) or (x==2 and y==0) or (x==2 and y==2)):
                if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                    count += 1
                elif board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                    count += 1
    if count >= 3:
        return True
    else:
        return False
    

def superRotationSystem(board, fallingPiece, spinDirection, Jspin, Lspin, Sspin, Zspin, Ispin):
    set1 = ['J', 'L', 'S', 'T', 'Z']
    set2 = ['I']

    rotationAndDirection = [(fallingPiece['rotation'] == 1 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 0 and spinDirection == 'CCW'),                
                            (fallingPiece['rotation'] == 2 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 1 and spinDirection == 'CCW'),
                            (fallingPiece['rotation'] == 3 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 2 and spinDirection == 'CCW'),
                            (fallingPiece['rotation'] == 0 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 3 and spinDirection == 'CCW')]

    if fallingPiece['shape'] in set1 and not isValidPosition(board, fallingPiece):
        for comindex, combination in enumerate(rotationAndDirection):
            if combination:
                for testx, testy in set1WallkickData[comindex]:
                    fallingPiece['x'] += testx 
                    fallingPiece['y'] -= testy
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['x'] -= testx 
                        fallingPiece['y'] += testy
                    else:
                        if fallingPiece['shape'] == 'J' and not isValidPosition(board, fallingPiece, adjY=-1):
                            Jspin = True
                        if fallingPiece['shape'] == 'L' and not isValidPosition(board, fallingPiece, adjY=-1):
                            Lspin = True
                        if fallingPiece['shape'] == 'S' and not isValidPosition(board, fallingPiece, adjY=-1):
                            Sspin = True
                        if fallingPiece['shape'] == 'Z' and not isValidPosition(board, fallingPiece, adjY=-1):
                            Zspin = True
                        return Jspin, Lspin, Sspin, Zspin, Ispin
    if fallingPiece['shape'] in set2 and not isValidPosition(board, fallingPiece):
        for index, combination in enumerate(rotationAndDirection):
            if combination:
                for testx, testy in set2WallkickData[index]:
                    fallingPiece['x'] += testx 
                    fallingPiece['y'] -= testy
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['x'] -= testx 
                        fallingPiece['y'] += testy
                    else:
                        if not isValidPosition(board, fallingPiece, adjY=-1):
                            Ispin = True
                        return Jspin, Lspin, Sspin, Zspin, Ispin
    if not isValidPosition(board, fallingPiece): 
        if spinDirection == 'CW':
            fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
            
        elif spinDirection == 'CCW':
            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
    if not Jspin:
        Jspin = False
    if not Lspin:
        Lspin = False
    if not Sspin:
        Sspin = False
    if not Zspin:
        Zspin = False
    if not Ispin:
        Ispin = False
         
    return Jspin, Lspin, Sspin, Zspin, Ispin


def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def isBlankLine(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] != BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    return numLinesRemoved


def reciveGarbage2P(board, line):
    y = 0
    counter = 0
    garbageHole = random.randrange(10)
    while counter < line:
        for pushUpY in range(y, BOARDHEIGHT - 1):
            for x in range(BOARDWIDTH):
                board[x][pushUpY] = board[x][pushUpY + 1]
        for x in range(BOARDWIDTH):
            if x == garbageHole:    
                board[x][BOARDHEIGHT - 1] = BLANK
            else:
                board[x][BOARDHEIGHT - 1] = 15
        counter += 1


def garbageTransferFrom(board, line):

    #take out the amount of line from the first board
    lineToSend = []
    y = BOARDHEIGHT - 1


    for x in range(BOARDWIDTH):
        lineToSend.append(board[x][-1:(-1*line) - 1:-1])

    while y >= BOARDHEIGHT - line:

        for pullDownY in range(BOARDHEIGHT - 1, 0, -1):
            for x in range(BOARDWIDTH):
                board[x][pullDownY] = board[x][pullDownY - 1]
        
        for x in range(BOARDWIDTH):
            board[x][0] = BLANK
        y -= 1
    return lineToSend


def garbageTransferTo(board, line):
    #add to the second board
    if line != []:
        y = 0
        counter = 0
        len(line[0])
        while counter < len(line[0]):
            for pushUpY in range(y, BOARDHEIGHT - 1):
                for x in range(BOARDWIDTH):
                    board[x][pushUpY] = board[x][pushUpY + 1]
            for x in range(BOARDWIDTH):
                board[x][BOARDHEIGHT - 1] = line[x][-1-counter]
            counter += 1


def burnGarbage(board, line):

    y = BOARDHEIGHT - 1 
    while y >= BOARDHEIGHT - line:

        for pullDownY in range(BOARDHEIGHT - 1, 0, -1):
            for x in range(BOARDWIDTH):
                board[x][pullDownY] = board[x][pullDownY - 1]
        
        for x in range(BOARDWIDTH):
            board[x][0] = BLANK
        y -= 1


def mixUpTop(board, line):
    y = 0
    counter = 0
    while counter < line and y < BOARDHEIGHT:
        if isBlankLine(board, y):
            y += 1
            continue
        #mix
        copyRow = []
        for x in range(BOARDWIDTH):
            copyRow.append(board[x][y])

        random.shuffle(copyRow)

        for x in range(BOARDWIDTH):
            board[x][y] = copyRow[x]

        y += 1
        counter += 1


def mixUpBottom(board, line):
    y = BOARDHEIGHT - 1
    counter = 0
    while counter < line:
        copyRow = []
        for x in range(BOARDWIDTH):
            copyRow.append(board[x][y])

        random.shuffle(copyRow)

        for x in range(BOARDWIDTH):
            board[x][y] = copyRow[x]
            
        y -= 1
        counter += 1


def sendLineFromP1(board, numLinesRemoved, P1Tspin, P1backToBack, P1ComboCounter, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple):
    blankBoard = getBlankBoard()
    lineSent = 0

    if not P1Tspin:
        if numLinesRemoved == 0:
            lineSent += ATTACKTABLE[0]
        if numLinesRemoved == 1:
            P1backToBack = False
            lineSent += ATTACKTABLE[1]
        elif numLinesRemoved == 2:
            P1backToBack = False
            lineSent += ATTACKTABLE[2]
        elif numLinesRemoved == 3:
            P1backToBack = False
            lineSent += ATTACKTABLE[3]
        elif numLinesRemoved == 4:
            P1Tetris = True
            if P1backToBack:
                P1backToBackPrint = True
                lineSent += ATTACKTABLE[10]
            lineSent += ATTACKTABLE[4]
            P1backToBack = True
    else:
        if P1backToBack:
            P1backToBackPrint = True
            lineSent += ATTACKTABLE[10]
        P1backToBack = True
        if numLinesRemoved == 0:
            P1TMini = True
            lineSent += ATTACKTABLE[8]
        elif numLinesRemoved == 1:
            P1TSingle = True
            lineSent += ATTACKTABLE[7]
        elif numLinesRemoved == 2:
            P1TDouble = True
            lineSent += ATTACKTABLE[5]
        elif numLinesRemoved == 3:
            P1TTriple = True
            lineSent += ATTACKTABLE[6]

    if blankBoard == board:
        P1PerfectClear = True
        lineSent += ATTACKTABLE[9]
        
    if numLinesRemoved > 0:
        P1Combo = True
        P1ComboCounter += 1
        if P1ComboCounter <= 12:
            lineSent += COMBOTABLE[P1ComboCounter - 1]
        else: 
            lineSent += COMBOTABLE[12]
    else:
        P1ComboCounter = 0
    
    return lineSent, P1backToBack, P1ComboCounter, numLinesRemoved, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple


def sendLineFromP2(board, numLinesRemoved, P2Tspin, P2backToBack, P2ComboCounter, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple):
    blankBoard = getBlankBoard()
    lineSent = 0

    if not P2Tspin:
        if numLinesRemoved == 0:
            lineSent += ATTACKTABLE[0]
        if numLinesRemoved == 1:
            P2backToBack = False
            lineSent += ATTACKTABLE[1]
        elif numLinesRemoved == 2:
            P2backToBack = False
            lineSent += ATTACKTABLE[2]
        elif numLinesRemoved == 3:
            P2backToBack = False
            lineSent += ATTACKTABLE[3]
        elif numLinesRemoved == 4:
            P2Tetris = True
            if P2backToBack:
                P2backToBackPrint = True
                lineSent += ATTACKTABLE[10]
            lineSent += ATTACKTABLE[4]
            P2backToBack = True
    else:
        if P2backToBack:
            P2backToBackPrint = True
            lineSent += ATTACKTABLE[10]
        P2backToBack = True
        if numLinesRemoved == 0:
            P2TMini = True
            lineSent += ATTACKTABLE[8]
        elif numLinesRemoved == 1:
            P2TSingle = True
            lineSent += ATTACKTABLE[7]
        elif numLinesRemoved == 2:
            P2TDouble = True
            lineSent += ATTACKTABLE[5]
        elif numLinesRemoved == 3:
            P2TTriple = True
            lineSent += ATTACKTABLE[6]

    if blankBoard == board:
        P2PerfectClear = True
        lineSent += ATTACKTABLE[9]

    if numLinesRemoved > 0:
        P2Combo = True
        P2ComboCounter += 1
        if P2ComboCounter <= 12:
            lineSent += COMBOTABLE[P2ComboCounter - 1]
        else: 
            lineSent += COMBOTABLE[12]
    else:
        P2ComboCounter = 0

    return lineSent, P2backToBack, P2ComboCounter, numLinesRemoved, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple


def convertToPixelCoordsP1(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN -300 + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBoxP1(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if loseP1:
        color = 14
    if P1Frozen:
        color = 16
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoordsP1(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx, pixely, BOXSIZE, BOXSIZE))


def convertToPixelCoordsP2(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN +300 + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBoxP2(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if loseP2:
        color = 14
    if P2Frozen:
        color = 16
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoordsP2(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx, pixely, BOXSIZE, BOXSIZE))    


def drawBoardP1(board):
    # fill the background of the board
    for y in range(BOARDHEIGHT - 20):
        for x in range(BOARDWIDTH):
            pygame.draw.rect(DISPLAYSURF, GRAY1, (x*BOXSIZE + XMARGIN -300 , y*BOXSIZE + TOPMARGIN + PLAYBOARD * BOXSIZE + 2, BOXSIZE, BOXSIZE), 1)
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN-302 , TOPMARGIN + PLAYBOARD * BOXSIZE + 2, (BOARDWIDTH * BOXSIZE) + 4, (PLAYBOARD * BOXSIZE)), 3)
    # draw the individual boxes on the board 
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBoxP1(x, y, board[x][y])


def drawBoardP2(board):
    # fill the background of the board
    for y in range(BOARDHEIGHT - 20):
        for x in range(BOARDWIDTH):
            pygame.draw.rect(DISPLAYSURF, GRAY1, (x*BOXSIZE + XMARGIN +300 , y*BOXSIZE + TOPMARGIN + PLAYBOARD * BOXSIZE + 2, BOXSIZE, BOXSIZE), 1)
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN+298 , TOPMARGIN + PLAYBOARD * BOXSIZE + 2, (BOARDWIDTH * BOXSIZE) + 4, (PLAYBOARD * BOXSIZE)), 3)
    # draw the individual boxes on the board 
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBoxP2(x, y, board[x][y])


def drawHiddenBoardP1():
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMARGIN-302 , TOPMARGIN +2, (BOARDWIDTH * BOXSIZE) + 10, (PLAYBOARD * BOXSIZE)))


def drawHiddenBoardP2():
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMARGIN+298 , TOPMARGIN +2, (BOARDWIDTH * BOXSIZE) + 10, (PLAYBOARD * BOXSIZE)))


def drawAleartBarP1(receivedLine):

    color = (255,0,0)

    if receivedLine == 0:
        color = BLACK

    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN-99 , TOPMARGIN + PLAYBOARD * BOXSIZE + 3, 8, (PLAYBOARD * BOXSIZE) - 1),3)

    pygame.draw.rect(DISPLAYSURF, color, (XMARGIN-97 , TOPMARGIN + PLAYBOARD * BOXSIZE + 3 + (BOXSIZE* (20 - receivedLine)), 4, BOXSIZE * receivedLine))


def drawAleartBarP2(receivedLine):

    color = (255,0,0)

    if receivedLine == 0:
        color = BLACK

    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN+501 , TOPMARGIN + PLAYBOARD * BOXSIZE + 3, 8, (PLAYBOARD * BOXSIZE) - 1),3)

    pygame.draw.rect(DISPLAYSURF, color, (XMARGIN+503 , TOPMARGIN + PLAYBOARD * BOXSIZE + 3 + (BOXSIZE* (20 - receivedLine)), 4, BOXSIZE * receivedLine))


def drawPieceP1(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoordsP1(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBoxP1(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawPieceP2(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoordsP2(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBoxP2(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

            
def drawAbility(abilities, x, y):

    for xSpace in range(5):
        for ySpace in range(5):
            if ySpace == 0:
                color = 2 
            if ySpace == 1:
                color = 3 
            if ySpace == 2:
                color = 0 
            if ySpace == 3:
                color = 1 
            if ySpace == 4:
                color = 4 
            pygame.draw.rect(DISPLAYSURF, COLORS[color], (x + xSpace * 25, y + ySpace * 25, BOXSIZE, BOXSIZE),1)

    spaces = 0
    for spin in abilities.keys():
        for count in range(abilities[spin]):
            if spin == 'Sspin':
                color = 0 
            if spin == 'Zspin':
                color = 1
            if spin == 'Jspin':
                color = 2
            if spin == 'Lspin':
                color = 3
            if spin == 'Ispin':
                color = 4
            pygame.draw.rect(DISPLAYSURF, COLORS[color], (x + count * 25, y + spaces * 25, BOXSIZE, BOXSIZE))
        spaces += 1


def GhostPiece(fallingPiece, board):
    ghostPiece = {'shape': fallingPiece['shape'],
                  'rotation': fallingPiece['rotation'],
                  'x': fallingPiece['x'],
                  'y': fallingPiece['y'],
                  'color': PIECES_COLOR[fallingPiece['shape']] + 7}

    for i in range(-1, BOARDHEIGHT):
        if not isValidPosition(board, fallingPiece, adjY=i+2):
            break
    ghostPiece['y'] += i + 1

    return ghostPiece


def drawNextPieceP1(NEXT_PIECES):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 720, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    for order, piece in enumerate(NEXT_PIECES):
        drawPieceP1(piece, pixelx=WINDOWWIDTH-740, pixely=120 + (order * 80))


def drawHoldPieceP1(piece):
    holdSurf = BASICFONT.render('Hold', True, TEXTCOLOR)
    holdRect = holdSurf.get_rect()
    holdRect.topleft = (WINDOWWIDTH - 1140, 80)
    DISPLAYSURF.blit(holdSurf, holdRect)

    if piece != None:
        drawPieceP1(piece, pixelx=WINDOWWIDTH-1140, pixely=120)


def drawNextPieceP2(NEXT_PIECES):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    for order, piece in enumerate(NEXT_PIECES):
        drawPieceP2(piece, pixelx=WINDOWWIDTH-140, pixely=120 + (order * 80))


def drawHoldPieceP2(piece):
    holdSurf = BASICFONT.render('Hold', True, TEXTCOLOR)
    holdRect = holdSurf.get_rect()
    holdRect.topleft = (WINDOWWIDTH - 540, 80)
    DISPLAYSURF.blit(holdSurf, holdRect)

    if piece != None:
        drawPieceP2(piece, pixelx=WINDOWWIDTH-540, pixely=120)


def drawText2P(text, x, y, color):
    infoSurf = BASICFONT.render(text, True, color)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (x, y)
    DISPLAYSURF.blit(infoSurf, infoRect)


def drawInstructions(x, y, color):
    drawText2P('tab: Quit', x, y, color)
    drawText2P('r: Reset', x, y + 20, color)
    drawText2P('p: Pause', x, y + 40, color)
    drawText2P('f: Fullscreen', x, y + 60, color)
    drawText2P('g: Small screen', x, y + 80, color)
    drawText2P('P1-e | P2-3: Hold', x, y + 100, color)
    drawText2P('P1-space | P2-v: Hard drop', x, y + 120, color)
    drawText2P('P1-left | P2-j: Move left', x, y + 140, color)
    drawText2P('P1-right | P2-l: Move right', x, y + 160, color)
    drawText2P('P1-down | P2-k: Soft drop', x, y + 180, color)
    drawText2P('P1-up | P2-i: Clockwise', x, y + 200, color)
    drawText2P('P1-w | P2-2: Counter clockwise', x, y + 220, color)
    drawText2P('P1-q | P2-1: Rotate 180', x, y + 240, color)


def drawSpecialMove(x, y, ComboCounter, Tspin, backToBack, board, tetris, PC, combo, mini, single, double, triple):
    if ComboCounter != 0:
        ComboCounter -= 1
     
    if PC:
        drawText2P('Perfect Clear', x, y, WHITE)
    if combo:
        drawText2P(str(ComboCounter) + ' Combo', x, y + 40, WHITE)
    if mini:
        drawText2P('T-Spin Mini', x, y + 80, WHITE)
    if single:
        drawText2P('T-Spin Single', x, y + 80, WHITE)
    if double:
        drawText2P('T-Spin Dounble', x, y + 80, WHITE)
    if triple:
        drawText2P('T-Spin Triple', x, y + 80, WHITE)
    if backToBack:
        drawText2P('BackToBack', x, y + 120, WHITE)
    if tetris:
        drawText2P('Tetris', x, y + 160, WHITE)


def fade(width, height, x, y): 
    fade = pygame.Surface((width, height))
    fade.fill((WHITE))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        DISPLAYSURF.blit(fade, (x,y))
        pygame.display.update()
        pygame.time.delay(5)



if __name__ == '__main__':
    main()