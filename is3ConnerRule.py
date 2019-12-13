def is3ConnerRule(board, piece, adjX=0, adjY=0):
    count = 0 
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if ((x==0 and y==0) or (x==0 and y==2) or (x==2 and y==0) or (x==2 and y==2)) and board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                count += 1
    if count >= 3:
        return True
    else:
        return False

#x=0, y=0 | x=0, y=2 | x=2, y=0 | x=2, y=2