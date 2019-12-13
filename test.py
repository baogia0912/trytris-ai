cur_x = 0
cur_y = 0
image_width = 600
for x in range(cur_x, image_width, 4):
    draw.line([(x, cur_y), (x + 2, cur_y)], fill=(170, 170, 170))