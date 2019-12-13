set1 = ['J', 'L', 'S', 'T', 'Z']
set2 = ['I']

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

fallingPiece = {}

while True:
    fallingPieceShape = input(print('Please input falling peice(J,L,S,T,Z,I or O):'))
    fallingPieceRotation = int(input(print('Please input rotation(0, 1, 2, 3):')))
    spinDirection = input(print("Please input spin direction (CW/CCW):"))

    fallingPiece['shape'] = fallingPieceShape
    fallingPiece['rotation'] = fallingPieceRotation

    rotationAndDirection = [(fallingPiece['rotation'] == 1 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 0 and spinDirection == 'CCW'),                
                            (fallingPiece['rotation'] == 2 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 1 and spinDirection == 'CCW'),
                            (fallingPiece['rotation'] == 3 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 2 and spinDirection == 'CCW'),
                            (fallingPiece['rotation'] == 0 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 3 and spinDirection == 'CCW')]

    if fallingPiece['shape'] in set1:
        for comindex, combination in enumerate(rotationAndDirection):
            if combination:
                for testindex, test in set1WallkickData[comindex]:
                    print(testindex, test)
    if fallingPiece['shape'] in set2:
        for comindex, combination in enumerate(rotationAndDirection):
            if combination:
                for testindex, test in enumerate(set2WallkickData[comindex]):
                    print(testindex, test)