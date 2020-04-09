from collections import deque
from snek import *
from explore import is_valid, offsets


def snek_to_snake(snek):
    snake = deque()
    block = snek.head[0]

    snake.appendleft((block.coord[1], block.coord[0]))

    for i in range(snek.length - 1):
        block = block.next[0]
        snake.appendleft((block.coord[1], block.coord[0]))

    return snake


def get_target_coords(occupancy, cell_value):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if occupancy[i][j] == 0 and cell_value[i][j] != 0:
                return i, j
            
    return -1, -1


def get_axis(r1, c1, r2, c2):
    return AXIS_X if c1 != c2 else AXIS_Y


def get_direction(r1, c1, r2, c2):
    return r2 - r1 + c2 - c1
    

def get_empty_adj_coords(snake):
    blocks = set(snake)
    hr, hc = snake[-1]

    for dr, dc in offsets:
        nr = hr + dr
        nc = hc + dc

        if is_valid(nr, nc) and (nr, nc) not in blocks:
            return deque([(nr, nc)])
	
    return deque([(hr + 1, hc)])


