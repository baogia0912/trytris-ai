import random

PIECES = {  'S': 0,
            'Z': 1,
            'J': 2,
            'L': 3,
            'I': 4,
            'O': 5,
            'T': 6
            }

bag = list(PIECES.keys())

def draw_piece(bag):
    if len(bag) == 0:
        bag = list(PIECES.keys())

    current_piece = bag[random.randrange(len(bag))]

    print(current_piece)

    bag.remove(current_piece)

    return bag, current_piece
 

for i in range(20):
    bag = draw_piece(bag)[0]
    print(bag)
