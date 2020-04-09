'''
February 9, 2020
Saima Ali
Porting the Snek API in C to Python
Tested in the ESC190 VM

In terminal, run
>>> python3 main.py

If you change the board size here,
you will have to modify snek_api.h
and recompile.
'''

from ctypes import *
BOARD_SIZE = 10
CYCLE_ALLOWANCE = 1.5
TIME_OUT = int(((BOARD_SIZE * 4) - 4) * CYCLE_ALLOWANCE)
LIMIT = min(TIME_OUT, 6)

# do not modify --------------------
x = 0
y = 1

AXIS_X = -1
AXIS_Y = 1

UP = -1
DOWN = 1
LEFT = -1
RIGHT = 1

AXIS_INIT = AXIS_Y
DIR_INIT = DOWN
# ----------------------------------

# import the library
# dependant on directory structure
snek_lib = CDLL("./libsnek_py.so")

class SnekBlock(Structure):
	# has ptr to itself, need to declare fields later
	pass

SnekBlock._fields_ = [('coord', c_int * 2), ('next', POINTER(SnekBlock))]

class Snek(Structure):
	_fields_ = [('head', POINTER(SnekBlock)), \
				('tail', POINTER(SnekBlock)), \
				('length', c_int)]
					
class GameBoard(Structure):
	_fields_ = [('cell_value', (c_int * BOARD_SIZE) * BOARD_SIZE), \
				('occupancy', (c_int * BOARD_SIZE) * BOARD_SIZE), \
				('snek', POINTER(Snek))]
	
	def __repr__(self):
		#don't need this, print(board[0]) does work though
		#left as a reference for how to access GameBoard attributes
		s = ''
		for i in range(0, BOARD_SIZE):
			for j in range(0, BOARD_SIZE):
				if self.occupancy[i][j] == 1:
					s += 'S'
				elif self.cell_value[i][j] != 0:
					s += 'X'
				else:
					s += '+'
			s += '\n'
		return s


def wrap_func(lib, funcname, restype, argtypes):
    ''' Referenced from
    https://dbader.org/blog/python-ctypes-tutorial-part-2
    '''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func

init_board = wrap_func(snek_lib, 'init_board', POINTER(GameBoard), [])
show_board = wrap_func(snek_lib, 'show_board', None, [POINTER(GameBoard)])
advance_frame = wrap_func(snek_lib, 'advance_frame', c_int, [c_int, c_int, POINTER(GameBoard)])
end_game = wrap_func(snek_lib, 'end_game', None, [POINTER(POINTER(GameBoard))])
get_score = wrap_func(snek_lib, 'get_score', c_int, [])



    
