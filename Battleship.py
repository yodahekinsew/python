
from random import *

board = [['O','O','O','O','O'],['O','O','O','O','O'],['O','O','O','O','O'],['O','O','O','O','O'],['O','O','O','O','O']]
ship_row = randint(0,3)
ship_col = randint(0,3)
ship1 = [[ship_row,ship_col],[ship_row + 1, ship_col]]

def show_board(board_in):
	for i in board:
		print (i)

def check_guess(guess, ship):
	for i in ship:
		if guess == i:
			print ("HIT!")
			return True
		else:
			print ("MISS!")
			return False

def change_board(guess, ship, board_in):
	i = guess[0]
	j = guess[1]
	if check_guess(guess, ship) == True:
		board[i][j] = 'X'


def play_game(board_in, ship):
	turns = 5
	counter = 0
	guesses = []
	print ("Welcome to Battleship!")
	print ('----------------------')
	test2 = False
	while turns > 0:
		show_board(board)
		row = int(input('What row are you guessing (1-5) :'))
		col = int(input('What column are you guessing (1-5) :'))
		guess1 = [row-1,col-1]
		test = check_guess(guess1, ship)
		if guess1 in guesses:
			print ("Sorry. You already guessed that.")
		if guess1 not in guesses:
			if test == True:
				print ("Nice Shot!")
				counter += 1
				change_board(guess1, ship, board_in)
			if test == False:
				print ("You Suck!")
			guesses.append(guess1)
			turns -= 1
		for i in ship:
			if i not in guesses:
				test2 == False
			else:
				test2 == True
		if test2 == True:
			print ("Congratulations! You sunk my ship!")
			break
	if test2 == False:
		print ("Sorry! Better luck next time!")
		print ("The ship was actually here: " + str(ship))
	response = input("Would you like to play again?: ")
	if response.lower() == 'yes':
		ship_row = randint(0,3)
		ship_col = randint(0,3)
		ship1 = [[ship_row,ship_col],[ship_row + 1, ship_col]]
		play_game(board, ship1)


play_game(board, ship1)