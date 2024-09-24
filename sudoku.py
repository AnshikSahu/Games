from typing import Tuple, List
# No other imports allowed

# PART OF THE DRIVER CODE

def input_sudoku() -> List[List[int]]:
	"""Function to take input a sudoku from stdin and return
	it as a list of lists.
	Each row of sudoku is one line.
	"""
	sudoku= list()
	for _ in range(9):
		row = list(map(int, input().rstrip(" ").split(" ")))
		sudoku.append(row)
	return sudoku

def print_sudoku(sudoku:List[List[int]]) -> None:
	"""Helper function to print sudoku to stdout
	Each row of sudoku in one line.
	"""
	for i in range(9):
		for j in range(9):
			print(sudoku[i][j], end = " ")
		print()

# You have to implement the functions below

def get_block_num(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
	"""This function takes a parameter position and returns
	the block number of the block which contains the position.
	"""
	# your code goes here
	return 3*((pos[0]-1)//3) +(pos[1]-1)//3+1

def get_position_inside_block(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
	"""This function takes parameter position
	and returns the index of the position inside the corresponding block.
	"""
	# your code goes here
	return (((pos[0]-1))%3)*3+(pos[1]-1)%3 + 1
	print(get_position_inside_block(sudoku,(4,2)))


def get_block(sudoku:List[List[int]], x: int) -> List[int]:
	"""This function takes an integer argument x and then
	returns the x^th block of the Sudoku. Note that block indexing is
	from 1 to 9 and not 0-8.
	"""
	# your code goes here
	x-=1
	L=[]
	for i in range(3*(x//3),3*(x//3)+3):
		for j in range(3*(x%3),3*(x%3)+3):
			L.append(sudoku[i][j])
	return list(L)
	

def get_row(sudoku:List[List[int]], i: int)-> List[int]:
	"""This function takes an integer argument i and then returns
	the ith row. Row indexing have been shown above.
	"""
	# your code goes here
	L=[]
	for j in range(9):
		L.append(sudoku[i-1][j])
	return list(L)

def get_column(sudoku:List[List[int]], i: int)-> List[int]:
	"""This function takes an integer argument i and then
	returns the ith column. Column indexing have been shown above.
	"""
	# your code goes here
	L=[]
	for j in range(9):
		L.append(sudoku[j][i-1])
	return L

def find_first_unassigned_position(sudoku : List[List[int]]) -> Tuple[int, int]:
	"""This function returns the first empty position in the Sudoku. 
	If there are more than 1 position which is empty then position with lesser
	row number should be returned. If two empty positions have same row number then the position
	with less column number is to be returned. If the sudoku is completely filled then return `(-1, -1)`.
	"""
	# your code goes here
	for i in range(9):
		for j in range(9):
			if sudoku[i][j]==0:
				return (i+1,j+1)
	return (-1,-1)

def valid_list(L: List[int])-> bool:
	"""This function takes a lists as an input and returns true if the given list is valid. 
	The list will be a single block , single row or single column only. 
	A valid list is defined as a list in which all non empty elements doesn't have a repeating element.
	"""
	# your code goes here
	for i in range(9):
		if L[i] != 0:
			for j in range(i+1,9):
				if L[i]==L[j]:
					return False
	return True

def valid_sudoku(sudoku:List[List[int]])-> bool:
	"""This function returns True if the whole Sudoku is valid.
	"""
	# your code goes here
	for i in range(9):
		L=get_row(sudoku,i+1)
		if not valid_list(L):
			return False
	for i in range(9):
		L=get_column(sudoku,i+1)
		if not valid_list(L):
			return False
	for i in range(9):
		L=get_block(sudoku,i+1)
		if not valid_list(L):
			return False

	return True


def get_candidates(sudoku:List[List[int]], pos:Tuple[int, int]) -> List[int]:
	"""This function takes position as argument and returns a list of all the possible values that 
	can be assigned at that position so that the sudoku remains valid at that instant.
	"""
	# your code goes here
	L=[]
	x=get_block_num(sudoku,pos)
	for i in range(1,10):
		if i not in get_row(sudoku,pos[0]):
			if i not in get_column(sudoku,pos[1]):
				if i not in get_block(sudoku,x):
					L.append(i)
	return list(L)

def make_move(sudoku:List[List[int]], pos:Tuple[int, int], num:int) -> List[List[int]]:
	"""This function fill `num` at position `pos` in the sudoku and then returns
	the modified sudoku.
	"""
	# your code goes here
	x,y = pos
	sudoku[x-1][y-1]=num
	return sudoku

def undo_move(sudoku:List[List[int]], pos:Tuple[int, int]):
	"""This function fills `0` at position `pos` in the sudoku and then returns
	the modified sudoku. In other words, it undoes any move that you 
	did on position `pos` in the sudoku.
	"""
	# your code goes here
	sudoku[pos[0]-1][pos[1]-1]=0
	return sudoku

def sudoku_solver(sudoku: List[List[int]]) -> Tuple[bool, List[List[int]]]:
	""" This is the main Sudoku solver. This function solves the given incomplete Sudoku and returns 
	true as well as the solved sudoku if the Sudoku can be solved i.e. after filling all the empty positions the Sudoku remains valid.
	It return them in a tuple i.e. `(True, solved_sudoku)`.

	However, if the sudoku cannot be solved, it returns False and the same sudoku that given to solve i.e. `(False, original_sudoku)`
	"""
	# your code goes here
	for i in range(81):
		r = i // 9
		c = i % 9
		if (sudoku[r][c] == 0):
			for e in get_candidates(sudoku, (r + 1, c + 1)):
				sudoku[r][c] = e
				x = sudoku_solver(sudoku)
				if (x[0]):
					return x
				sudoku[r][c] = 0
			return (False, [])
	return (valid_sudoku(sudoku), sudoku)

	# your code goes here

	# to complete this function, you may define any number of helper functions.
	# However, we would be only calling this function to check correctness.

	#return (False, sudoku)

# PLEASE NOTE:
# We would be importing your functions and checking the return values in the autograder.
# However, note that you must not print anything in the functions that you define above before you 
# submit your code since it may result in undefined behaviour of the autograder.

def in_lab_component(sudoku: List[List[int]]):
    print("Testcases for In Lab evaluation")
    print("Get Block Number:")
    print(get_block_num(sudoku,(4,4)))
    print(get_block_num(sudoku,(7,2)))
    print(get_block_num(sudoku,(2,6)))
    print("Get Block:")
    print(get_block(sudoku,1))
    print(get_block(sudoku,2))
    print(get_block(sudoku,3))
    print(get_block(sudoku,4))
    print(get_block(sudoku,5))
    print(get_block(sudoku,6))
    print(get_block(sudoku,7))
    print("Get Row:")
    print(get_row(sudoku,3))
    print(get_row(sudoku,5))
    print(get_row(sudoku,9))
    print("Get Column:")
    print(get_column(sudoku,7))
    print(get_column(sudoku,6))
    print("Get sudoku:")
    print(find_first_unassigned_position(sudoku))
    print(valid_list([2, 1, 3, 4, 5, 6, 7, 7, 0]))
    print(valid_sudoku([[5, 3 , 3 , 0 , 7 , 0 , 0 , 0 , 0] , [6, 0 , 0 , 1 , 9 , 5 , 0 , 0 , 0] , [0, 9 , 8 , 0 , 0 , 0 , 0 , 6 , 0] , [8, 0 , 0 , 0 , 6 , 0 , 0 , 0 , 3] , [4, 0 , 0 , 8 , 0 , 3 , 0 , 0 , 1] , [7, 0 , 0 , 0 , 2 , 0 , 0 , 0 , 6] , [0, 6 , 0 , 0 , 0 , 0 , 2 , 8 , 0] , [0, 0 , 0 , 4 , 1 , 9 , 0 , 0 , 5] , [0, 0 , 0 , 0 , 8 , 0 , 0 , 7 , 9]]))
    print(get_candidates(sudoku,(1,4)))
    print(make_move(sudoku,(1,2),8))
    print(undo_move(sudoku, (1, 2))
   	#print(sudoku_solver(sudoku))

# Following is the driver code
# you can edit the following code to check your performance.
if (_name_ == "_main_"):

	# Input the sudoku from stdin
	sudoku = input_sudoku()

	# Try to solve the sudoku
	possible, sudoku = sudoku_solver(sudoku)

	# The following line is for the in-lab component
	in_lab_component(sudoku)
	# Show the result of the same to your TA to get your code evaulated

	# Check if it could be solved
	if possible:
		print("Found a valid solution for the given sudoku :)")
		print_sudoku(sudoku)

	else:
		print("The given sudoku cannot be solved :(")
		print_sudoku(sudoku)
