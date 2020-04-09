from snek import *
from time import sleep
from util import *
from collections import deque
from explore import explore


if __name__ == "__main__":
	#ptr to board
	board = init_board()
	
	play_on = 1
	show_board(board)
	axis = AXIS_INIT
	direction = DIR_INIT
	moves = deque()
	tr, tc = -2, -2
			
	while (play_on):
		r, c = get_target_coords(board[0].occupancy, board[0].cell_value)
		flag = False		

		if (tr, tc) != (r, c) or len(moves) == 0:
			flag = True
			tr, tc = r, c
			snake = snek_to_snake(board[0].snek[0])
			moves = explore(snake, tr, tc).moves
			if len(moves) > 1:
				moves.popleft()
			else:
				moves = get_empty_adj_coords(snake)

		#indexing at 0 dereferences the pointer
		hc, hr = board[0].snek[0].head[0].coord[x], \
						   board[0].snek[0].head[0].coord[y]

		axis = get_axis(hr, hc, *moves[0])
		direction = get_direction(hr, hc, *moves[0])
		move_to = moves.popleft()
			
		play_on = advance_frame(axis, direction, board)
		show_board(board)

		sleep(0.65)
	
	#pass by reference to clean memory	
	end_game(byref(board))
