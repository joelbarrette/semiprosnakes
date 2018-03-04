import bottle
import os
import random
import json

moveUp = -1
moveDown = 1
moveLeft = -1
moveRight = 1


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



def ateApple():
	pass


def eatenBySnake():
	pass

def determineSnakePositions():
	pass

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
	elif(snakeMove == 'down' and snakeHeadY + moveDown > boardHeight):
		isWall = True
	elif(snakeMove == 'left' and snakeHeadX + moveLeft < 0):
		isWall = True
	elif(snakeMove == 'right' and snakeHeadX + moveRight > boardWidth):
		isWall = True

	return isWall


def getLegalMoves(allSnakes, boardHeight, boardWidth):
	allLegalSnakeMoves = []

	for snake in allSnakes:

		print snake
		currentSnakeMoves = []
		#index 0 represents the head of the snake

		#Can the snake move up?
		if(not isWall(snake, boardHeight, boardWidth, 'up') and not isSnakeBody(allSnakes, snake, 'up')):
			currentSnakeMoves.append('up')
			
		#can the snake move down?
		if(not isWall(snake, boardHeight, boardWidth, 'down') and not isSnakeBody(allSnakes, snake, 'down')):
			currentSnakeMoves.append('down')
	
		#can the snake move left?
		if(not isWall(snake, boardHeight, boardWidth, 'left') and not isSnakeBody(allSnakes, snake, 'left')):
			currentSnakeMoves.append('left')

		#can the snake move right?
		if(not isWall(snake, boardHeight, boardWidth, 'right') and not isSnakeBody(allSnakes,snake, 'right')):
			currentSnakeMoves.append('right')

		allLegalSnakeMoves.append(currentSnakeMoves)

	return allLegalSnakeMoves




def getMove(jsonBoard):

	#get raw details about the board
	[allSnakes, ourSnakeIndex, applePositions, healthBars, snakeIds, snakeNames, snakeTaunts, boardHeight, boardWidth] = getBoardInfo(jsonBoard)

	#get legal moves for the snake at the index
	allLegalSnakeMoves = getLegalMoves(allSnakes, boardHeight, boardWidth)
	
	#randomly select a move
	snakeMove = random.choice(allLegalSnakeMoves[ourSnakeIndex])
	
	return snakeMove


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
        port=os.getenv('PORT', '8080'),
debug = True)