import pygame
import random
import math
from pygame import mixer


# initialization
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
done = True

# background
background = pygame.image.load('background.png')
mixer.music.load("background.mpeg")
mixer.music.play(-1)

# icon and caption
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 500


def player(x, y):
    screen.blit(playerImg, (x, y))


# ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(50)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Score Board
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 40)
scoreX = 10
scoreY = 10


def display_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# GAME OVER

gameover_font = pygame.font.Font('freesansbold.ttf', 75)


def gameover():
    gameover_text = gameover_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(gameover_text, (200, 250))


# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# collision check function
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
while done:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: playerY -= 2
    if pressed[pygame.K_DOWN]: playerY += 2
    if pressed[pygame.K_LEFT]: playerX -= 2
    if pressed[pygame.K_RIGHT]: playerX += 2
    if pressed[pygame.K_SPACE]:
        if bullet_state is "ready":
            bullet_sound = mixer.Sound("shoot.wav")
            bullet_sound.play()
            bulletX = playerX
            bulletY = playerY
            bullet(bulletX, bulletY)

    # Player movement
    if playerX >= 736:
        playerX = 736
    if playerX <= 0:
        playerX = 0
    if playerY >= 536:
        playerY = 536
    if playerY <= 0:
        playerY = 0

    # enemy movement
    for i in range(no_of_enemies):

        # conditions for game over
        if enemyY[i] > 480:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            gameover()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"
    if bullet_state is "fire":
        bullet(bulletX, bulletY)

        bulletY -= bulletY_change

    player(playerX, playerY)
    display_score(scoreX, scoreY)

    pygame.display.update()
