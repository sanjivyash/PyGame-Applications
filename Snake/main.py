import pygame
from pygame.draw import rect
import random
from time import time, sleep
from copy import deepcopy

pygame.init()

# size of one unit in the game
box = 32

screen = pygame.display.set_mode((24 * box, 20 * box))
quit = False

# snake head in middle of the screen 
snake = [{
		'x': 12 * box, 
		'y': 9 * box
	}]

# food appears at random position
food = {
		'x': random.randint(0, 23) * box,
		'y': random.randint(2, 19) * box
	}

# score to e displayed 
score = 0

# different colors used in the game
black = (0, 0, 0)
gray = (100, 100, 100)
white = (255, 255, 255)
cyan = (0, 255, 255)

# direction of movement 
vertical = False
direction = 1


# create new food
def update_food():
	global food, score
	score +=1

	while food in snake:
		food = {
				'x': random.randint(0, 23) * box,
				'y': random.randint(2, 19) * box
			}


# display the score
def show_score():
	rect(screen, black, (0, 0, 24 * box, 2 * box))
	font = pygame.font.Font("freesansbold.ttf", box)
	msg = font.render(f'Score : {score}', True, (255, 255, 255))
	screen.blit(msg, (0.5 * box, 0.5 * box))


# move the snake
def move_snake():
	global snake, vertical
	head = deepcopy(snake[0])

	if vertical:
		head['y'] += box * direction
	else:
		head['x'] += box * direction

	snake.insert(0, head)

	if head == food:	
		update_food()
	else:
		snake.pop()


# check for game over
over = False

def game_over():
	global over
	head = deepcopy(snake[0])

	if head in snake[1:]:
		over = True

	if head['x'] < 0 or head['x'] > 24 * box:
		over = True

	if head['y'] < 2 * box or head['y'] > 20 * box:
		over = True

	if over:
		font = pygame.font.Font("freesansbold.ttf", 80)
		msg = font.render("GAME OVER", True, (255, 0, 0))
		screen.blit(msg, (132, 300)) 


# start the game 
start = time()

while not quit:
	# give color to screen
	screen.fill(gray)

	for event in pygame.event.get():
		# quit the game
		if event.type == pygame.QUIT:
			quit = True

		# user inputs for snake
		if event.type == pygame.KEYDOWN:

			if vertical:
				if event.key == pygame.K_LEFT:
					direction = -1
					vertical = False
					start = time()

				if event.key == pygame.K_RIGHT:
					direction = 1
					vertical = False
					start = time()

			else:
				if event.key == pygame.K_UP:
					direction = -1
					vertical = True
					start = time()

				if event.key == pygame.K_DOWN:
					direction = 1
					vertical = True
					start = time()

			if not over:
				move_snake()

	# give color to snake
	for val in snake:
		rect(screen, white, (val['x'], val['y'], box, box))

	# give color to food
	rect(screen, cyan, (food['x'], food['y'], box, box))

	# move the snake
	if time() > start + 0.2:
		start = time()

		if not over:
			move_snake()

	# check if game over
	game_over()

	# display the score
	show_score()

	pygame.display.update()