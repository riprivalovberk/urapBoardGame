import square as sq
import player as pl
import numpy as np
import dice as d
import itertools as it
#import GUI
#from PIL import Image
import math
import pygame #used for GUI

from numpy import genfromtxt


import csv
#import position as pos


class Gameboard:

	gameName = ""
	players = []

	playerCount = None
	curentPlayersTurn = 0 #FOR NOW

	allSquares = []
	duplicateSquares = [] # Used in setup to prevent duplicate squares

	winningSquare = None
	startSquare = None

	gameOver = False

	def __init__(self, file):
		self.board = file #IMG file for board
		self.setUp() #Sets up all Squares and players and puts players to starting squares.


	def setUp(self):#Sets up all Squares and players and puts players to starting squares.
		'''
		data = genfromtxt('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', delimiter=',')
		data = np.nan_to_num(data) 
		data = np.round(data).astype(int)
		data = np.savetxt('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', data, fmt="%s")
		'''
		datafile = open('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', 'r') #Opens the csv file w/info
		data = list(csv.reader(datafile))#data = 2d array of csv file components
		self.gameName = data[1][0]
		self.playerCount = int(data[1][1])
		for i in range(1, len(data)): #Adds all the squares to allSquares, sets .nextquare, .special, and the x and y cooridantes properly. Also sets winningSquare and startSquare.

			
			square = sq.Square(data[i][2], data[i][3])
			for j in range(len(self.duplicateSquares)):
				if self.duplicateSquares[j] == square:
					square = self.duplicateSquares.pop(j)
					break

			if data[i][4]:
				if data[i][4] == "start":
					self.startSquare = square
				elif data[i][4] == "finish":
					self.winningSquare = square
				square.special = data[i][4]
			self.allSquares.append(square)

			if data[i][5]:
				nextSquare = sq.Square(data[i][5], data[i][6])
				square.nextSquare = nextSquare
				self.duplicateSquares.append(nextSquare)
		for i in range(self.playerCount): #Names each player and sets their square to the first square
			name = "test" #PROMPT TO ENTER NAME!!!!!!!!!!!!!!!!!!!
			p = pl.Player(name)
			p.setSquare(self.startSquare)
			self.players.append(p)

		self.curentPlayersTurn = it.cycle(self.players)




	def getWinningSquare(self):
		return winningSquare

	def getStartSquare(self):
		return startSquare

	def getPlayerTurn(self):
		return next(self.curentPlayersTurn)

	def wonGame(self, player):
		return player.getSquare() == self.winningSquare

	def endGame(self, player):
		print("Congrats " + player + ", you have won the game!")
		self.gameOver = True

		return #TERMINATE THE GAME!
	#Actually takes the turn for the player. 
	def takeTurn(self, player, distance):
		
		while not self.gameOver and distance > 1:
			currentSq = player.getSquare()
			if currentSq.hasNextSquare():
				player.setSquare(currentSq.getNextSquare())
				distance -= 1
				if self.wonGame(player):
					self.endGame(player)

			else:
				print("Uh oh, dead end? Something is wrong.")

		return 
	#Checks if the game has been won and if not allows a player to take his or her turn.
	def play(self,str):
		print(str)
		pygame.init() #initialize pygame
		print(self.board)
		background = pygame.image.load(self.board)
		#get the width of the board
		background_x = background.get_size()[0]
		#get the height of the board
		background_y = background.get_size()[1]
		#screen size will be the size of the board
		screen = pygame.display.set_mode((background_x,background_y))
		
		running =True
		all_sprites = pygame.sprite.Group()
		mydice = d.dice(300,300)
		all_sprites.add(mydice)
	
		
		#while not self.gameOver:
		while running:
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        running = False
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                        mydice.roll()
                                        
                        all_sprites.update()
                                        
                        screen.fill((0,0,0))
                        #all_sprites.draw(screen)
		
                        screen.blit(background,(0,0))
                        all_sprites.draw(screen)
                        pygame.display.update()
			#player = self.getPlayerTurn()
			#roll = 1 #PROMPT A ROLL!!!!!!!!!!!!!!!!!!! int(Math.random)*6 + 1 would make it play itself
			#self.takeTurn(player, roll)

		return

	'''
	Helps Debug. Prints a 2D array nicely
	'''
	def printTable(self, arr):
		for i in arr:
			print(i)
			print()
		return
