import pygame 
import random
import time

# initialise the library
pygame.init()
# initialise the screen
screen = pygame.display.set_mode((800, 600))

# EVENT: Anything inside the game window is an event

# quit event
quit = False

# Title and Icon of window
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player icon
playerImg = pygame.image.load("rocket.png")
(x, y) = (370, 520)
vel = 0

# backgorund image
backImg = pygame.image.load("back.png")

# Target icon
enemyImg = pygame.image.load("evil.png")

# Bullet Icon
bulletImg = pygame.image.load("bullet.png")

# Score of the Player
score = 0

def player():
    # draw image on screen
    screen.blit(playerImg, (x, y))

# flag for direction to move 
enemy_X, enemy_Y, flag = [], [], []

def create_enemy():
    flag.append(True)
    enemy_Y.append(0)
    enemy_X.append(random.randint(20, 720))

def target():
    # draw all enemies
    for pos in zip(enemy_X, enemy_Y):
        screen.blit(enemyImg, pos)

# keep track of bullets
bullet_X, bullet_Y = [], []

def bullet():
    # draw from spaceship
    for (x, y) in zip(bullet_X, bullet_Y):
        screen.blit(bulletImg, (x+30, y-32))

# destroy enemies that have been hit
def destroy():
    global score
    i, j = 0, 0 
    while i < len(bullet_X) and j < len(enemy_X):
        if enemy_X[j]-16 <= bullet_X[i] <= enemy_X[j]+48:
                if enemy_Y[j]-16 <= bullet_Y[i] <= enemy_Y[j]+48:
                    bullet_X.pop(i), bullet_Y.pop(i)
                    enemy_X.pop(j), enemy_Y.pop(j)
                    score += 1
                    i, j = i-1, j-1
        i, j = i+1, j+1

trigger = time.time()
create_enemy()

def show_score():
    font = pygame.font.Font("freesansbold.ttf", 45)
    msg = font.render(f'{score:02d}', True, (255, 255, 255))
    screen.blit(msg, (648, 455))

# game over function
over = False
def game_over():
    enemy_X.clear(), enemy_Y.clear()
    font = pygame.font.Font("freesansbold.ttf", 80)
    msg = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(msg, (132, 179))

# the game runs inside the loop
while not quit:
    # Backgound image
    screen.blit(backImg, (0,0))
    # move enemies by horizontally
    for i, val in enumerate(enemy_X):
        # change direction when hits booundary
        if val > 720 or val < 20:
            flag[i] = not flag[i]

        v = 3 if flag[i] else -3
        enemy_X[i] += v
    
    # after 3 sec add new enemy and move vertically
    if time.time() - trigger > 3:
        enemy_Y = [32+i for i in enemy_Y]
        create_enemy()
        trigger = time.time()

    for event in pygame.event.get():
        # quit the game
        if event.type == pygame.QUIT:
            quit = True
        # move to the right or left or shoot
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vel = -6
            if event.key == pygame.K_RIGHT:
                vel = 6
            if event.key == pygame.K_SPACE:
                bullet_X.append(x)
                bullet_Y.append(y)
        # stop moving when key released        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and vel < 0:
                vel = 0
            if event.key == pygame.K_RIGHT and vel > 0:
                vel = 0
    
    #check for game over
    if enemy_Y:
        if max(enemy_Y) > 480:
            over = True
    if over:
        game_over()
    # destroy bullets that have left the window
    for i, val in enumerate(bullet_Y):
        if val < 0:
            bullet_Y.pop(i)
            bullet_X.pop(i)
    # update coordinates
    x = max(10, min(720, x+vel))
    # target icons destroyed by bullet
    destroy()
    show_score()
    # player icon loaded
    player()
    # target icon loaded
    target()
    # bullets must have vertical velocity
    bullet_Y = [i-10 for i in bullet_Y]
    # shooting icon loaded
    bullet()
    # update window
    pygame.display.update()
