import bottle
import os
import random
import json
import sys


moveUp = -1
moveDown = 1
moveLeft = -1
moveRight = 1
maxDepth = 20

def getBoardInfo(jsonBoard):

	boardWidth = jsonBoard.get('width')
	boardHeight =  jsonBoard.get('height') 

	numSnakes = len(jsonBoard.get('snakes'))
	snakeIdx = 0


	ourSnakeID = jsonBoard.get('you').get('id')
	ourSnakeIndex = 0

	allSnakes = []
	applePositions = []
	healthBars = []
	
	snakeIds = []
	snakeNames = []
	snakeTaunts = []

	for snake in jsonBoard.get('snakes').get('data'):
		currentSnake = []

		healthBars.append(snake.get('health'))

		snakeIds.append(snake.get('id'))
		snakeNames.append(snake.get('name'))
		snakeTaunts.append(snake.get('taunt'))


		if(snake.get('id') == ourSnakeID):
			ourSnakeIndex = snakeIdx


		for snakePoint in snake.get('body').get('data'):
			

			xSnake = snakePoint.get('x')
			ySnake = snakePoint.get('y')
			
			currentSnake.append([xSnake, ySnake])

		
		allSnakes.append(currentSnake)
		snakeIdx += 1


	for apple in jsonBoard.get('food').get('data'):
		applePositions.append([apple.get('x'), apple.get('y')])
	

	return [allSnakes, ourSnakeIndex, applePositions, healthBars, snakeIds, snakeNames, snakeTaunts, boardHeight, boardWidth]




####TODO
#handle legal moves -- Done
#handle deaths -- Run into walls, players, or get eaten
#handle apple eating -- 
#handle health update -- Done

#input: current board as json object, and list of moves indexed by snake
#output: the new board state
def generateBoard(currentBoard, snakeMoves):

	directions = ['up', 'down', 'left', 'right']

	boardWidth = currentBoard.get('width')
	boardHeight =  currentBoard.get('height') 

	snakeIdx = 0
	


	for snakeMove in snakeMoves:
		ateApple = False
		
		#head is always first element of the array
		currentHeadX = currentBoard['snakes']['data'][snakeIdx]['body']['data'][0]['x']
		currentHeadY = currentBoard.get('snakes').get('data')[snakeIdx].get('body').get('data')[0].get('y')

		for apple in currentBoard['food']['data']:
			appleX = apple.get('x')
			appleY = apple.get('y')

			#if apple is hit, don't remove tail, only add head
			#replenish health
			if(currentHeadX == appleX and currentHeadY == appleY):
				ateApple = True


				####TODO check if the new apple position is valid
				currentBoard['food']['data'][0]['x'] = random.randint(0, boardWidth)
				currentBoard['food']['data'][0]['y'] = random.randint(0, boardHeight)

		
		if snakeMove == 'up':
			currentBoard['snakes']['data'][snakeIdx]['body']['data'].insert(0, {"object":"point","x":currentHeadX, "y":currentHeadY+moveUp})

		elif snakeMove == 'down':
			currentBoard['snakes']['data'][snakeIdx]['body']['data'].insert(0, {"object":"point","x":currentHeadX, "y":currentHeadY+moveDown})

		elif snakeMove == 'left':
			currentBoard['snakes']['data'][snakeIdx]['body']['data'].insert(0, {"object":"point","x":currentHeadX+moveLeft, "y":currentHeadY})

		elif snakeMove == 'right':
			currentBoard['snakes']['data'][snakeIdx]['body']['data'].insert(0, {"object":"point","x":currentHeadX+moveRight, "y":currentHeadY})


		if ateApple:
			currentBoard['snakes']['data'][snakeIdx]['health'] = 100
			currentBoard['snakes']['data'][snakeIdx]['length'] += 1

		else:
			currentBoard['snakes']['data'][snakeIdx]['health'] -= 1
			#code to remove last element of a snake
			currentBoard['snakes']['data'][snakeIdx]['body']['data'] = currentBoard['snakes']['data'][snakeIdx]['body']['data'][:-1]

		snakeIdx +=1


	return currentBoard

#needs array of snakes and a position


#needs array of snakes and a position
def doesMoveHitASnake(snake, snakeHeadX, snakeHeadY):
	#snake body part is a point of a particular snake
	for snakeBodyPart in snake:
		if(snakeBodyPart[0] == snakeHeadX and snakeBodyPart[1] == snakeHeadY):
			return True
	return False


#one snake and a position 	
def doesMoveHitAnySnake(snakes, snakeHeadX, snakeHeadY):
	for snake in snakes:
		if(doesMoveHitASnake(snake, snakeHeadX, snakeHeadY)):
			return True
	return False
	

def isSnakeBody(snakes,snake,direction):
	#move array for snakes head
	snakeHeadX = snake[0][0]
	snakeHeadY = snake[0][1]

	if(direction == 'up'):
		snakeHeadY += moveUp
		return doesMoveHitAnySnake(snakes,snakeHeadX, snakeHeadY)

	elif(direction == 'down'):
		snakeHeadY += moveDown
		return doesMoveHitAnySnake(snakes,snakeHeadX, snakeHeadY)

	elif(direction == 'left'):
		snakeHeadX += moveLeft
		return doesMoveHitAnySnake(snakes,snakeHeadX, snakeHeadY)

	elif(direction == 'right'):
		snakeHeadX += moveRight
		return doesMoveHitAnySnake(snakes,snakeHeadX, snakeHeadY)

	return False



def isSnakeDead(snake):
	if(snake.get('health') == 0):
		return True
	else:
		return False


####TODO
#find path to an apple, avoiding snakes
#
def getPathToApple(snakes, snake, apple):
	pass


#input: the position of the snake's head, and the apple's position
#outpout: the 
def getDistanceToApple(snakeHead, apple):
	pass



def isWall(snake, boardHeight, boardWidth, snakeMove):
	#first element of snake is the head of the snake
	snakeHeadX = snake[0][0]
	snakeHeadY = snake[0][1]

	isWall = False

	if(snakeMove == 'up' and snakeHeadY + moveUp < 0):
		isWall = True
	elif(snakeMove == 'down' and snakeHeadY + moveDown > boardHeight - 1):
		isWall = True
	elif(snakeMove == 'left' and snakeHeadX + moveLeft < 0):
		isWall = True
	elif(snakeMove == 'right' and snakeHeadX + moveRight > boardWidth - 1):
		isWall = True

	return isWall

	
def enemySnakeList(allSnakes, snake, ourSnakeIndex):
	enemySnakes = list(allSnakes)
	del enemySnakes[ourSnakeIndex]
	return enemySnakes
	
	
def snakeHeads(allSnakes):
	snakeHeadList = []
	for i in allSnakes:
		snakeHeadList.append(i[0])
			
	return snakeHeadList
	
def isDeathSquare(allSnakes, snake, snakeMove, ourSnakeIndex):
	print snakeMove
	enemySnakeHeads = snakeHeads(enemySnakeList(allSnakes, snake, ourSnakeIndex))

	
	for i in enemySnakeHeads:

		if (snakeMove == 'down' and (-2 == (snake[0][1] - i[1]))):
			print 'enemy near below'
			return True #down check
		if (snakeMove == 'up' and (2 == (snake[0][1] - i[1]))):
			print 'enemy near above'
			return True # up check
		if (snakeMove == 'right' and (2 == (snake[0][0] - i[0]))):
			print 'enemy near right'
			return True # right check
		if (snakeMove == 'left' and (-2 == (snake[0][0] - i[0]))):
			print 'enemy near left'
			return True # left check

		return False		

def getLegalMoves(allSnakes, boardHeight, boardWidth, ourSnakeIndex):


	snake = allSnakes[ourSnakeIndex]

	currentSnakeMoves = []
	#index 0 represents the head of the snake

	#Can the snake move up?
	if(not isWall(snake, boardHeight, boardWidth, 'up') and not isSnakeBody(allSnakes, snake, 'up') and not isDeathSquare(allSnakes, snake, 'up', ourSnakeIndex)):
		currentSnakeMoves.append('up')
		
	#can the snake move down?
	if(not isWall(snake, boardHeight, boardWidth, 'down') and not isSnakeBody(allSnakes, snake, 'down') and not isDeathSquare(allSnakes, snake, 'down', ourSnakeIndex)):
		currentSnakeMoves.append('down')

	#can the snake move left?
	if(not isWall(snake, boardHeight, boardWidth, 'left') and not isSnakeBody(allSnakes, snake, 'left') and not isDeathSquare(allSnakes, snake, 'left', ourSnakeIndex)):
		currentSnakeMoves.append('left')

	#can the snake move right?
	if(not isWall(snake, boardHeight, boardWidth, 'right') and not isSnakeBody(allSnakes,snake, 'right') and not isDeathSquare(allSnakes, snake, 'right', ourSnakeIndex)):
		currentSnakeMoves.append('right')

	print currentSnakeMoves
	return currentSnakeMoves


def getBoardInfo(jsonBoard):
	boardWidth = jsonBoard.get('width')
	boardHeight =  jsonBoard.get('height') 

	numSnakes = len(jsonBoard.get('snakes'))
	snakeIdx = 0


	ourSnakeID = jsonBoard.get('you').get('id')
	ourSnakeIndex = 0

	allSnakes = []
	applePositions = []
	healthBars = []
	
	snakeIds = []
	snakeNames = []
	snakeTaunts = []

	for snake in jsonBoard.get('snakes').get('data'):
		currentSnake = []

		healthBars.append(snake.get('health'))

		snakeIds.append(snake.get('id'))
		snakeNames.append(snake.get('name'))
		snakeTaunts.append(snake.get('taunt'))


		if(snake.get('id') == ourSnakeID):
			ourSnakeIndex = snakeIdx


		for snakePoint in snake.get('body').get('data'):
			

			xSnake = snakePoint.get('x')
			ySnake = snakePoint.get('y')
			
			currentSnake.append([xSnake, ySnake])

		
		allSnakes.append(currentSnake)
		snakeIdx += 1


	for apple in jsonBoard.get('food').get('data'):
		applePositions.append([apple.get('x'), apple.get('y')])
	

	return allSnakes, ourSnakeIndex, applePositions, healthBars, snakeIds, snakeNames, snakeTaunts, boardHeight, boardWidth






def createGraphSpace(boardHeight, boardWidth):
	return np.zeros((boardHeight,boardWidth))

def getAllSnakeSquares(allSnakes):
	allSquares = []
	for snake in allSnakes:
		for snakePart in snake:
			allSquares.append(snakePart)
	return allSquares

def fiilSnakeSquares(snakeBoard, snakesSquare):
	for filledSquare in snakesSquare:
		snakeBoard[filledSquare[0], filledSquare[1]] = 1
	return snakeBoard


def getAllApplesSquares(applePositions):
	allApples = []
	for apple in applePositions:
		allApples.append(apple)
	return allApples

def fillAppleSquares(appleBoard, appleSquares):
	for applePosition in appleSquares:
		appleBoard[applePosition[0], applePosition[1]] = 1
	return appleBoard



def shortestPathToApple(currentPosition, appleBoard,snakeBoard, lastMove, seenPositions, boardHeight, boardWidth, depth):
	
	X = currentPosition[0]
	Y = currentPosition[1]

	seenPositions.append(currentPosition)

	#loops on itself
	if currentPosition in seenPositions:
		return 10000
	elif depth > maxDepth:
		return 10000
	#a snake is there
	elif [X,Y] in snakeBoard:
		return 10000

	#hit a random ass wall
	elif(X < 0 or X > boardWidth - 1 or Y < 0 or Y > boardHeight - 1):
		return 10000

	#found an apple
	elif [X,Y]  in appleBoard:
		return depth
	else:
		return min(shortestPathToApple([X,Y-1], appleBoard, snakeBoard, 'up', seenPositions, boardHeight, boardWidth, depth+1),
			shortestPathToApple([X,Y+1], appleBoard, snakeBoard, 'down', seenPositions, boardHeight, boardWidth, depth+1),
			shortestPathToApple([X+1,Y], appleBoard, snakeBoard, 'right', seenPositions, boardHeight, boardWidth, depth+1),
			shortestPathToApple([X-1,Y], appleBoard, snakeBoard, 'left', seenPositions, boardHeight, boardWidth, depth+1))







#takes in the board state, our snake, the snake move, apples, and board limits, returns a positive numeric value for that position
def getValueOfMove(allSnakes, ourSnake, snakeMove, healthBars, applePositions, boardHeight, boardWidth):
	moveValue = 0

	X = ourSnake[0][0]
	Y = ourSnake[0][1]

	if snakeMove == 'up':
		Y += moveUp
	elif snakeMove == 'down':
		Y += moveDown
	elif snakeMove == 'right':
		X += moveRight
	elif snakeMove == 'left':
		X += moveLeft


	snakeBoard = getAllSnakeSquares(allSnakes)
	appleBoard = getAllApplesSquares(applePositions)

	################################
	#####	TODO	################
	################################

	#functions to add to the value of the position
	#
	for apple in applePositions:
		moveValue += shortestPathToApple([X,Y], appleBoard, snakeBoard, snakeMove, [[X,Y]], boardHeight, boardWidth, 1)


	###############################
	###############################
	###############################


	return moveValue

#input: arrary of our available moves
#output: the index of the highest value move
def getBestMove(allLegalSnakeMoves, allSnakes, ourSnake, healthBars, applePositions,  boardHeight, boardWidth):
	moveValues = []
	for snakeMove in allLegalSnakeMoves:
		moveValues.append(getValueOfMove(allSnakes, ourSnake, snakeMove, healthBars, applePositions,  boardHeight, boardWidth))
	return moveValues.index(max(moveValues))



def getMove(jsonBoard):

	#get raw details about the board
	[allSnakes, ourSnakeIndex, applePositions, healthBars, snakeIds, snakeNames, snakeTaunts, boardHeight, boardWidth] = getBoardInfo(jsonBoard)
	ourSnake = allSnakes[ourSnakeIndex]

	#get legal moves for the snake at the index
	allLegalSnakeMoves = getLegalMoves(allSnakes, boardHeight, boardWidth, ourSnakeIndex)
	
	snakeMove = random.choice(allLegalSnakeMoves)
	
	#snakeMove = getBestMove(allLegalSnakeMoves, allSnakes, ourSnake, healthBars, applePositions,  boardHeight, boardWidth)

	return snakeMove




@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():

    boardData = bottle.request.json

    # TODO: Do things with data

    snakeMove = getMove(boardData)

    
    return {
        'move': snakeMove,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', sys.argv[1]),
debug = True)